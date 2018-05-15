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
    crt = SSLCertificate('certs/import_cert.crt')
    key = SSLPrivateKey('certs/import_cert.pem', password=os.environ.get('CERT_PASSWD', ''))
    
    return pkg.sign_package(crt, key)
