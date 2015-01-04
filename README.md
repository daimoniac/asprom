asprom - assault profile monitor
================================

asprom is a firewall compliance scanner. You define a profile of which services your network(s) should offer to users.
The scanner automatically and regularly portscans your networks using nmap and reports any aberrations from the defined profile.

This functionality can be used to ascertain PCI-DSS, BSI-Grundschutz or DIN 27001 compliance of stateful firewalls.

Don't be afraid - it is easily installed, very user-friendly and doesn't require any knowledge besides basic tcp/ip concepts :-)


How to install
--------------

### Runtime

I am using asprom on debian wheezy, so this install guide references apt-get. I'm sure you can translate that to the package manager of your choice distribution.

`apt-get install cron python python-pip git mysql-server nmap python-mysqldb`

install the remaining python dependencies directly from pypi.

`pip install crontab netaddr python-nmap paste bottle config croniter`

su to an unprivileged user, then clone the git repository.

```bash
cd ~
git clone https://github.com/daimoniac/asprom.git
cd asprom
```


### Database

edit etc/asprom.cfg and set your database parameters.

create an empty database and grant the user you just specified all rights to it.

```sql
mysql -uroot -p
> create database asprom;
> grant all privileges on asprom.* to asprom@localhost identified by '<arbitrarypassword>';
> exit;
```

import the ddl structure from the ddl.sql file:

`mysql -uroot -p asprom < db/ddl.sql`

### Running the GUI

You are done! Start the GUI:

`python aspromGUI.py`

and navigate to [http://localhost:8080](http://localhost:8080).
