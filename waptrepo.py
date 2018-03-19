# -*- coding: utf-8 -*-

import waptpackage
import os

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
        rep['repo'] = waptpackage.WaptRemoteRepo(name=name, url=rep['url'], timeout=4, http_proxy=os.environ.get('https_proxy'))
        rep['repo'].verify_cert = True
    return REPOS
