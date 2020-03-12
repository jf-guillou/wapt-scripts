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

def get_latest_version(package_list, pkg_hash):
    """Iterate through package_list and return newest one"""
    newest = None
    for pkg in package_list:
        if waptpkg.hash(pkg) == pkg_hash and (not newest or pkg > newest):
            newest = pkg

    return newest

def update_local(local, remote, dryrun, nocheckcert):
    """Iterate through local packages and updates them if necessary"""
    done = []
    local_packages = local.packages()
    remote_packages = remote.packages()

    # Iterate all local packages
    for local_pkg in local_packages:
        local_pkg_hash = waptpkg.hash(local_pkg)
        if local_pkg_hash in done:
            continue
        done.append(local_pkg_hash)

        local_pkg = get_latest_version(local_packages, local_pkg_hash)
        log.debug('Checking %s (%s) @ %s' % (local_pkg.package, local_pkg_hash, local_pkg.version))

        remote_pkg = get_latest_version(remote_packages, local_pkg_hash)
        if not remote_pkg:
            continue

        log.debug('Found %s %s' % (remote_pkg.package, remote_pkg.version))
        if remote_pkg > local_pkg:
            log.debug('Newer version %s (%s) @ %s -> %s' % (local_pkg.package, local_pkg_hash, local_pkg.version, remote_pkg.version))
            if not dryrun:
                add_package(remote, local, remote_pkg, nocheckcert)

def add_package(remote, local, pkg, nocheckcert):
    """Add remote package to local repository"""
    log.info('Downloading %s %s' % (pkg.package, pkg.version))

    if not waptpkg.download(remote, local.localpath, pkg):
        log.error('Download failure')
        return False

    if not nocheckcert and not waptpkg.check_signature(pkg):
        log.error('Original signature checks failure')
        return False

    signature = waptpkg.overwrite_signature(pkg)
    if signature:
        log.debug('Signature overwrite : %s ' % pkg.filename)
        filename = waptpkg.recalc_md5(pkg)
        log.debug('New filename : %s' % filename)
    else:
        log.debug('Package signature untouched')

    log.debug('Added %s to local repository' % pkg.package)
    return True

def run():
    """Loop through remote repositories and check for any package updates"""
    parser = ArgumentParser()
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='Silent')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Verbose')
    parser.add_argument('--dryrun', dest='dryrun', action='store_true', help='Do not download, only check for updates')
    parser.add_argument('--nocheckcert', dest='nocheckcert', action='store_true', help='Do not check remote certificates - This may be dangerous')
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
            update_local(local, remote['repo'], args.dryrun, args.nocheckcert)
            log.debug('Done')
        else:
            log.info('Nothing to do')

    local.update_packages_index()

if __name__ == '__main__':
    run()
