#!/usr/bin/python
# -*- coding: utf-8 -*-

import waptpackage
from argparse import ArgumentParser

def get_local_repo():
  repo = waptpackage.WaptLocalRepo()
  repo._load_packages_index()
  return repo

def get_remote_repo():
  repo = waptpackage.WaptRemoteRepo(name='tqit',url='https://wapt.tranquil.it/wapt',timeout=4)
  repo.verify_cert = True
  return repo

def search_package(remote, name):
  print 'Searching for', name
  packages = remote.search(name, None, True)
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

  remote = get_remote_repo()
  local = get_local_repo()
  for packageName in args.name:
    packages = search_package(remote, packageName)
    if not packages:
      print 'No results for', packageName
      continue
    p = pick_package(packages)
    if not p:
      print 'Invalid choice, skipping', packageName
      continue
    add_package(remote, local, p)

if __name__ == '__main__':
  run()
