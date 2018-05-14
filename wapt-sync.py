#!/usr/bin/python
# -*- coding: utf-8 -*-

import waptrepo
import waptpkg

def check_new_packages(local, remote):
    """Check remote repository for updates"""
    local_date = local.is_available()
    if not local_date:
        raise FileNotFoundError('Missing local Packages file')

    remote_date = remote.is_available()
    if not remote_date:
        raise FileNotFoundError('Missing remote Packages file')

    print('Local %s' % local_date)
    print('Remote %s' % remote_date)
    return local_date < remote_date

def get_newest(package_list, name):
    """Iterate through package_list and return newest one"""
    newest = None
    for pack in package_list:
        if pack.package == name and (not newest or pack > newest):
            newest = pack

    return newest

def update_local(local, remote):
    """Iterate through local packages and updates them if necessary"""
    done = []
    for l_pack in local.packages:
        if done.count(l_pack.package):
            continue
        done.append(l_pack.package)

        l_pack = get_newest(local.packages, l_pack.package)
        print('Checking %s %s' % (l_pack.package, l_pack.version))

        r_pack = get_newest(remote.packages, l_pack.package)
        if not r_pack:
            continue

        print('Found %s %s' % (r_pack.package, r_pack.version))
        if r_pack > l_pack:
            print('Newer version %s %s - %s' % (l_pack.package, l_pack.version, r_pack.version))
            add_package(remote, local, r_pack)

def add_package(remote, local, pack):
    """Add remote package to local repository"""
    print('Downloading %s %s' % (pack.package, pack.version))

    if not download_pkg(remote, local.localpath, pack):
        print('Download failure')
        return False

    if not check_pkg_signature(pack):
        print('Signature checks failure')
        return False

    print('Added %s to local repository' % pack.package)
    return True

def run():
    """Loop through remote repositories and check for any package updates"""
    local = waptrepo.get_local_repo()
    remotes = waptrepo.get_remote_repos()
    for name, remote in remotes.items():
        print('Remote %s %s' % (name, remote['url']))
        if check_new_packages(local, remote['repo']):
            print('Scan remote Packages for updates')
            update_local(local, remote['repo'])
            print('Done')
        else:
            print('Nothing to do')

    local.update_packages_index()

if __name__ == '__main__':
    run()
