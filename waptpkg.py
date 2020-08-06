# -*- coding: utf-8 -*-

import os
import shutil
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
    if not (cert_file and key_file and password):
        return False

    crt = SSLCertificate(cert_file)
    key = SSLPrivateKey(key_file, password=password)

    # Force unzip and rebuild to ensure filelist integrity
    pkg.unzip_package()
    previous_localpath = pkg.localpath
    pkg.localpath = None
    pkg.build_package(target_directory=os.path.dirname(previous_localpath))
    shutil.rmtree(pkg.sourcespath)
    pkg.sourcespath = None

    return pkg.sign_package(certificate=crt, private_key=key)

def recalc_md5(pkg):
    """Recalc MD5 sum in filename after changes in package contents"""
    pkg.md5sum = waptpackage.md5_for_file(pkg.localpath)

    filename = pkg.make_package_filename()
    if filename != pkg.filename:
        new_localpath = os.path.join(os.path.dirname(os.path.abspath(pkg.localpath)), filename)
        shutil.move(pkg.localpath, new_localpath)
        pkg.localpath = new_localpath
        pkg.load_control_from_wapt()

    return pkg.filename

def hash(pkg):
    """Creates a hash based on package properties"""

    return "%s:%s:%s:%s" % (pkg.package, pkg.target_os, pkg.architecture, pkg.locale)
