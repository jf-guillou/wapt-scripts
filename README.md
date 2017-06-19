# wapt-scripts
Collection of scripts used with wapt server

## wapt-addpackage.py

Search in official repository for packages, pick best match and copy it in local repository.

Differs from Import function by keeping package and TIS signature intact, allowing simpler updates.

## wapt-sync.py

Synchronize local Packages repository with official remote repository.
The main goal is to auto-update packages imported with wapt-addpackage.py.

Should be used in a daily cron task.
