#!/usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import sys
import logging
import waptrepo
import waptpkg

log = logging.getLogger(__name__)

def check_new_packages(local, remote):
    """Check remote repository for updates"""
    local_date = local.is_available()
    if not local_date:
        raise FileNotFoundError('Missing local Packages file')

    remote_date = remote.is_available()
    if not remote_date:
        raise FileNotFoundError('Missing remote Packages file')

    log.debug('Local %s' % local_date)
    log.debug('Remote %s' % remote_date)
    return local_date < remote_date

def get_newest(package_list, name):
    """Iterate through package_list and return newest one"""
    newest = None
    for pack in package_list:
        if pack.package == name and (not newest or pack > newest):
            newest = pack

    return newest

def update_local(local, remote, dryrun):
    """Iterate through local packages and updates them if necessary"""
    done = []
    local_packages = local.packages()
    remote_packages = remote.packages()
    
    for l_pack in local_packages:
        if done.count(l_pack.package):
            continue
        done.append(l_pack.package)

        l_pack = get_newest(local_packages, l_pack.package)
        log.debug('Checking %s %s' % (l_pack.package, l_pack.version))

        r_pack = get_newest(remote_packages, l_pack.package)
        if not r_pack:
            continue

        log.debug('Found %s %s' % (r_pack.package, r_pack.version))
        if r_pack > l_pack:
            log.debug('Newer version %s %s - %s' % (l_pack.package, l_pack.version, r_pack.version))
            if not dryrun:
                add_package(remote, local, r_pack)

def add_package(remote, local, pack):
    """Add remote package to local repository"""
    log.info('Downloading %s %s' % (pack.package, pack.version))

    if not waptpkg.download(remote, local.localpath, pack):
        log.error('Download failure')
        return False

    if not waptpkg.check_signature(pack):
        log.error('Original signature checks failure')
        return False

    waptpkg.overwrite_signature(pack)

    log.debug('Added %s to local repository' % pack.package)
    return True

def run():
    """Loop through remote repositories and check for any package updates"""
    parser = ArgumentParser()
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='Silent')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Verbose')
    parser.add_argument('--dryrun', dest='dryrun', action='store_true', help='Do not download, only check for updates')
    parser.add_argument('--force', dest='force', action='store_true', help='Force check remote repo')
    args = parser.parse_args()

    hdlr = logging.StreamHandler(sys.stdout)
    hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    log.addHandler(hdlr)

    if args.quiet:
        log.setLevel(logging.CRITICAL)
    elif args.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    local = waptrepo.get_local_repo()
    remotes = waptrepo.get_remote_repos()
    for name, remote in remotes.items():
        log.info('Remote %s %s' % (name, remote['url']))
        if check_new_packages(local, remote['repo']) or args.force:
            log.debug('Scan remote Packages for updates')
            update_local(local, remote['repo'], args.dryrun)
            log.debug('Done')
        else:
            log.info('Nothing to do')

    local.update_packages_index()

if __name__ == '__main__':
    run()
