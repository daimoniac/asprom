asprom - assault profile monitor
================================

asprom is a firewall compliance scanner. You define a profile of which services your network(s) should offer to users.
The scanner automatically and regularly portscans your networks using nmap and reports any aberrations from the defined profile.

This functionality can be used to ascertain PCI-DSS, BSI-Grundschutz or DIN 27001 compliance of stateful firewalls.

Don't be afraid - it is easily installed, very user-friendly and doesn't require any knowledge besides basic tcp/ip concepts :-)


How to install
--------------

## docker
this includes everything.

```
cp env.example .env
docker-compose up -d
```

## Running the GUI

You are done! Open the GUI:

[http://localhost:8100](http://localhost:8100).

## prometheus metrics
[http://localhost:5000](http://localhost:5000).


### First steps

Select the tab "Schedule" and define a host name, ip or ip range to scan. You could scan "localhost", for example, your web site, or your local network.
Leave the fields "port range" and "extra parameters" empty for now.
After clicking "add job", you should see a new line in the table.
Click the magnifying glass icon to run the scan right now.
Asprom will notify you when the scan is done.

You should then see some alerts in the tab "alerts: exposed".
Try mitigating these alerts by clicking the "star" icon.

You can accept these alerts to the baseline by clicking the "approve" icon and entering a business justification.
This way, you tell asprom: It's okay, I want that port to be open.

When you have done this with all the IP Ranges you are interested in, you have finished your initial configuration and the bulk of the work.

In the future, you will be alerted if there are any new services appearing in the defined IP ranges on the website.

### deleting machines and services from inventory
currently the UI is missing for deleting old machines and services from inventory.
in the meantime, use the following queries:

```
IP=1.2.3.4
delete from servicelog where serviceId in (select id from services where machineId = (select id from machines m where m.ip='$IP'));
delete from changelog where serviceId in (select id from services where machineId = (select id from machines m where m.ip='$IP'));
delete from services where machineId = (select id from machines m where m.ip='$IP');
delete from machinelog where machineId = (select id from machines m where m.ip='$IP');
delete from machines where ip='$IP';
```

### Nagios

To be alerted actively with the monitoring tool of your choice, please use the script aspromNagiosCheck.py as standard nagios plugin.
It will say CRITICAL if there is any unknown service present.

