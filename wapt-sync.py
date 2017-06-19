#!/usr/bin/python
# -*- coding: utf-8 -*-

import waptpackage

def get_local_repo():
  repo = waptpackage.WaptLocalRepo()
  repo._load_packages_index()
  return repo

def get_remote_repo():
  repo = waptpackage.WaptRemoteRepo(name='tqit',url='https://wapt.tranquil.it/wapt',timeout=4)
  repo.verify_cert = True
  return repo

def check_new_packages(local, remote):
  localDate = local.is_available()
  if not localDate:
    raise FileNotFoundError('Missing local Packages file')
  remoteDate = remote.is_available()
  if not remoteDate:
    raise FileNotFoundError('Missing remote Packages file')
  print 'Local', localDate
  print 'Remote', remoteDate
  return localDate < remoteDate

def get_newest(list, name):
  n = None
  for p in list:
    if p.package == name and (not n or p > n):
      n = p
  return n

def update_local(local, remote):
  done = []
  for lp in local.packages:
    if done.count(lp.package):
      continue
    done.append(lp.package)

    lp = get_newest(local.packages, lp.package)
    print 'Checking', lp.package, lp.version

    ep = get_newest(remote.packages, lp.package)
    if not ep:
      continue

    print 'Found', ep.package, ep.version
    if ep > lp:
      print lp.package, lp.version, 'has a newer version', ep.version
      remote.download_packages(lp.package, local.localpath)

def run():
  local = get_local_repo()
  remote = get_remote_repo()
  if check_new_packages(local, remote):
    print 'Scan remote Packages for updates'
    update_local(local, remote)
    print 'Done'
  else:
    print 'Nothing to do'
  local.update_packages_index()

if __name__ == '__main__':
  run()
