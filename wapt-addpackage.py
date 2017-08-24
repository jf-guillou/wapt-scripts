#!/usr/bin/python
# -*- coding: utf-8 -*-

import waptpackage
from argparse import ArgumentParser

repos = {
  'tis': {'url': 'https://wapt.tranquil.it/wapt', 'repo': None},
  'smp': {'url': 'https://wapt.lesfourmisduweb.org/wapt', 'repo': None}
}

def get_local_repo():
  repo = waptpackage.WaptLocalRepo()
  repo._load_packages_index()
  return repo

def get_remote_repos():
  for name, r in repos.items():
    r['repo'] = waptpackage.WaptRemoteRepo(name=name, url=r['url'], timeout=4)
    r['repo'].verify_cert = True
  return repos

def search_package(remotes, name):
  print 'Searching for', name
  packages = []
  for _, r in remotes.items():
    packages.extend(r['repo'].search(name, None, True))
  if not len(packages):
    return None
  return packages

def pick_package(packages):
  print 'Matching packages:'
  for (i, p) in enumerate(packages, start=1):
    print i, p.package, p.version
  idx = input('Pick package: ')
  if not isinstance(idx, int):
    return None
  if idx < 1 or idx > len(packages):
    return None
  return list(packages)[idx-1]

def add_package(remote, local, p):
  if not p.package:
    return
  print 'Downloading', p.package, p.version
  remote.download_packages(p.package, local.localpath)
  local.update_packages_index()
  print 'Added', p.package, 'to local repository'

def run():
  parser = ArgumentParser()
  parser.add_argument('name', metavar='name', nargs='+', help='Package name')
  args = parser.parse_args()
  if not args.name:
    parser.print_help()
    return

  remotes = get_remote_repos()
  local = get_local_repo()
  for packageName in args.name:
    packages = search_package(remotes, packageName)
    if not packages:
      print 'No results for', packageName
      continue
    p = pick_package(packages)
    if not p:
      print 'Invalid choice, skipping', packageName
      continue
    add_package(remotes[p['repo']]['repo'], local, p)

if __name__ == '__main__':
  run()
