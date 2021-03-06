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

`apt-get install cron python python-pip git mysql-server nmap python-mysqldb python-nmap`

install the remaining python dependencies directly from pypi.

`pip install python-crontab netaddr paste bottle config croniter`

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


### First steps

Select the tab "Schedule" and define a host name, ip or ip range to scan. You could scan "localhost", for example, your web site, or your local network.
Leave the fields "port range" and "extra parameters" empty for now.
After clicking "add job", you should see a new line in the table.
Click the magnifying glass icon to run the scan right now.
Asprom will notify you when the scan is done.

You should then see some alerts in the tab "alerts: exposed".
Try mitigating these alerts by clicking the "star" icon.

You can accept these alerts to the neat line by clicking the "approve" icon and entering a business justification.
This way, you tell asprom: It's okay, I want that port to be open.

When you have done this with all the IP Ranges you are interested in, you have finished your initial configuration and the bulk of the work.

In the future, you will be alerted if there are any new services appearing in the defined IP ranges on the website.

### Nagios

To be alerted actively with the monitoring tool of your choice, please use the script aspromNagiosCheck.py as standard nagios plugin.
It will say CRITICAL if there is any unknown service present.

