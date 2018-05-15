# wapt-scripts
Collection of scripts used with wapt server

These scripts are compatible with WAPT 1.5 and should be ran user the `/var/www/wapt` owner user account and prefixed with proper PYTHONHOME & PYTHONPATH.

## Installation
Exemples below assume default installation in `/opt/wapt`:

    cd /opt/wapt && git clone https://github.com/jf-guillou/wapt-scripts.git

Optional bash aliases:

    echo "alias wapt-addpackage='sudo -u wapt PYTHONHOME=/opt/wapt PYTHONPATH=/opt/wapt WAPT_CERT=/opt/wapt/wapt-script/certs/wapt.crt WAPT_KEY=/opt/wapt/wapt-scripts/certs/key.pem WAPT_PASSWD=key_password /opt/wapt/wapt-scripts/wapt-addpackage.py'" >> ~/.bash_aliases
    echo "alias wapt-sync='sudo -u wapt PYTHONHOME=/opt/wapt PYTHONPATH=/opt/wapt WAPT_CERT=/opt/wapt/wapt-script/certs/wapt.crt WAPT_KEY=/opt/wapt/wapt-scripts/certs/key.pem WAPT_PASSWD=key_password /opt/wapt/wapt-scripts/wapt-sync.py'" >> ~/.bash_aliases

### wapt-addpackage.py

Search in known repositories ([TIS](https://store.wapt.fr/)/[SMP](https://wapt.lesfourmisduweb.org/tous-les-packages)) for packages, pick best match and copy it in local repository.

Differs from Import function by keeping package and overwriting signature, allowing automatic updates from remote repository.

    sudo -u wapt PYTHONHOME=/opt/wapt PYTHONPATH=/opt/wapt WAPT_CERT=/opt/wapt/wapt-script/certs/wapt.crt WAPT_KEY=/opt/wapt/wapt-scripts/certs/key.pem WAPT_PASSWD=key_password /opt/wapt/wapt-scripts/wapt-addpackage.py vlc

### wapt-sync.py

Synchronize local Packages repository with official remote repository.
The main goal is to update packages imported with wapt-addpackage.py.

Can also be used in a daily cron task, if you trust the remote repository.

    echo "0 3 * * * wapt PYTHONPATH=/opt/wapt PYTHONHOME=/opt/wapt WAPT_CERT=/opt/wapt/wapt-script/certs/wapt.crt WAPT_KEY=/opt/wapt/wapt-scripts/certs/key.pem WAPT_PASSWD=key_password /opt/wapt/wapt-scripts/wapt-sync.py --quiet" >> /etc/crontab
