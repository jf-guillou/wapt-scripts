# -*- coding: utf-8 -*-

import os
import waptpackage
from waptcrypto import SSLCABundle,SSLCertificate,SSLPrivateKey

def download(remote, path, pkg):
    """Downloads package"""
    if not pkg.package:
        return False

    res = remote.download_packages(pkg, path)
    if res['errors']:
        return False

    pkg_path = res['downloaded'] and res['downloaded'][0] or res['skipped'][0]
    if not pkg_path:
        return False

    return pkg_path

def check_signature(pkg):
    """Check package signature if /etc/ssl/certs exists"""
    if not os.path.exists('/etc/ssl/certs'):
        return True

    if not waptpackage.PackageEntry(waptfile=pkg.localpath).check_control_signature(SSLCABundle('/etc/ssl/certs')):
        return False

    return True

def overwrite_signature(pkg):
    """Overwrite imported package signature"""
    cert_file = os.environ.get('WAPT_CERT')
    key_file = os.environ.get('WAPT_KEY')
    password = os.environ.get('WAPT_PASSWD')
    if not (cert_file and key_file and pwd):
        return False

    crt = SSLCertificate(cert_file)
    key = SSLPrivateKey(key_file, password=password)
    
    return pkg.sign_package(crt, key)
