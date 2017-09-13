# -*- coding: utf-8 -*-

from zipfile import ZipFile
import os

REQ_SIG_SHA1 = True
REQ_SIG_SHA256 = False

def check(path):
    """Inspect package contents for required signatures"""
    print('Check package integrity %s' % path)
    with ZipFile(path) as zipf:
        files_list = zipf.namelist()

        if REQ_SIG_SHA1 and not has_sha1_signature(files_list):
            print('Missing SHA1 signature / manifest')
            os.remove(path)
            return False

        if REQ_SIG_SHA256 and not has_sha256_signature(files_list):
            print('Missing SHA256 signature / manifest')
            os.remove(path)
            return False

    return True

def has_sha1_signature(files_list):
    """Check for SHA1 signature and manifest in file list"""
    return 'WAPT/signature' in files_list and 'WAPT/manifest.sha1' in files_list

def has_sha256_signature(files_list):
    """Check for SHA256 signature and manifest in file list"""
    return 'WAPT/signature.sha256' in files_list and 'WAPT/manifest.sha256' in files_list
