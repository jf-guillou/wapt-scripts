# -*- coding: utf-8 -*-

import os
import waptpackage
from waptcrypto import SSLCABundle

def download(remote, path, pkg):
    """Downloads package"""
    if not pkg.package:
        return False

    res = remote.download_packages(pkg, path)
    if res['errors']:
        return False

    path = res['downloaded'] and res['downloaded'][0] or res['skipped'][0]
    if not path:
        return False

    return True

def check_signature(pkg):
    if not os.path.exists('/etc/ssl/certs'):
        return True

    if not waptpackage.PackageEntry(waptfile=path).check_control_signature(SSLCABundle('/etc/ssl/certs')):
        return False

    return True
