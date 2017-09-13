#!/usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import waptpackage

REPOS = {
    'tis': {'url': 'https://wapt.tranquil.it/wapt', 'repo': None},
    'smp': {'url': 'https://wapt.lesfourmisduweb.org/wapt', 'repo': None}
}

def get_local_repo():
    """Get local package repository and load index"""
    repo = waptpackage.WaptLocalRepo()
    repo.update()
    return repo

def get_remote_repos():
    """Get remote package repositories and init connection"""
    for name, rep in REPOS.items():
        rep['repo'] = waptpackage.WaptRemoteRepo(name=name, url=rep['url'], timeout=4)
        rep['repo'].verify_cert = True
    return REPOS

def search_package(remotes, name, new_only):
    """Search for package name in remote repository"""
    print('Searching for %s' % name)
    packages = []
    for _, rep in remotes.items():
        packages.extend(rep['repo'].search(name, None, new_only))
    if not packages:
        return None
    return packages

def pick_package(packages):
    """List matching packages and wait for user to pick one"""
    print('Matching packages:')
    for (i, pack) in enumerate(packages, start=1):
        print('%s %s %s' % (i, pack.package, pack.version))
    idx = input('Pick package: ')
    if not isinstance(idx, int):
        return None
    if idx < 1 or idx > len(packages):
        return None
    return list(packages)[idx-1]

def add_package(remote, local, pack):
    """Add remote package to local repository"""
    if not pack.package:
        return
    print('Downloading %s %s' % (pack.package, pack.version))
    remote.download_packages(pack, local.localpath)
    local.update_packages_index()
    print('Added %s to local repository' % pack.package)

def run():
    """Parse arguments, fetch a list a matching packages from remote repo and install if picked"""
    parser = ArgumentParser()
    parser.add_argument('name', metavar='name', nargs='+', help='Package name')
    parser.add_argument('-a', dest='allversions', action='store_true', help='Display all versions')
    args = parser.parse_args()
    if not args.name:
        parser.print_help()
        return

    remotes = get_remote_repos()
    local = get_local_repo()
    for package_name in args.name:
        packages = search_package(remotes, package_name, not args.allversions)
        if not packages:
            print('No results for %s' % package_name)
            continue
        pack = pick_package(packages)
        if not pack:
            print('Invalid choice, skipping %s' % package_name)
            continue
        add_package(remotes[pack['repo']]['repo'], local, pack)

if __name__ == '__main__':
    run()
