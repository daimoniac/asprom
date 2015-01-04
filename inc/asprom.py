'''
Created on Oct 22, 2014

@author: daimon
\namespace asprom.inc.asprom
'''

import MySQLdb as mdb
from datetime import datetime
from inc.config import Config
from os import path
from bottle import response
from json import dumps
from crontab import CronTab
import re, socket, traceback, copy
from netaddr import IPAddress, IPNetwork, AddrFormatError
from pprint import pprint
from nmap import nmap


global cfg 
global db


class NoJoibIDException(Exception):
    """
    Exception raised for crontab entries not concerning asprom.
    """

    def __init__(self, job):
        self.job = job


class Cfg(Config):
    '''
    Configuration in dict form from the config file etc/asprom.cfg.
    '''
    maindir=None

    def __init__(self):
        '''
        expanded constructor, calls the super constructor of Config with the path to asprom.cfg
        '''
        maindir = path.normpath(path.join(path.dirname(path.realpath(__file__)), path.pardir))
        # read config file
        super(Cfg, self).__init__(maindir + '/etc/asprom.cfg')
        self.maindir = maindir



class AspromModel(object):
    '''
    This Model abstracts calls to the database. It returns rows of data for the views in the GUI.
    Using the toJSON static method, they can be easily converted to the json format used by bootstrap-table AJAX calls.
    '''

    def __init__(self, *args, **kwargs):
        '''
        standard constructor
        '''
        super(AspromModel, self).__init__(*args, **kwargs)
        
    def getProfilingURL(self):
        '''
        @return: the URL for the GUI.
        '''
        return cfg.misc['url']
        
    def getAlertsExposed(self):
        '''
        returns row data for the alerts-exposed view.
        '''
        #db connection
        cur = db.cursor(mdb.cursors.DictCursor)
        q= """SELECT id, hostname, ip, port, product service, version,
            extrainfo, ffdate date, crit
            FROM exposed"""
        cur.execute(q)

        rows = cur.fetchall()
        
        for row in rows:
            row['date'] = datetime.strftime(row['date'],"%Y-%m-%d %H:%M")
            row['crit'] = False if 'crit' in row and row['crit'] else True

            if len(row['version']):
                row['service'] = "%s (%s)" % (row['service'], row['version'])
         
        return rows

    def getAlertsClosed(self):
        '''
        returns row data for the alerts-closed view.
        '''
        #db connection
        cur = db.cursor(mdb.cursors.DictCursor)
        q= """SELECT id, hostname, ip, port, product service, version,
            extrainfo, approvaldate date, justification, crit
            FROM closed"""
        cur.execute(q)

        rows = cur.fetchall()
        
        for row in rows:
            row['date'] = datetime.strftime(row['date'],"%Y-%m-%d %H:%M")
            row['crit'] = False if 'crit' in row and row['crit'] else True

            if len(row['version']):
                row['service'] = "%s (%s)" % (row['service'], row['version'])
            
        return rows
    
    def getNeatline(self):
        '''
        returns row data for the neatline view.
        '''
        cur = db.cursor(mdb.cursors.DictCursor)
        q= """select m.ip, m.hostname, s.id, s.port, s.machineId, 
            s.product service, s.version, s.extrainfo, n.justification, n.date
            from services s
            inner join neatline n on s.id = n.serviceId
            inner join machines m on s.machineId = m.id
            where n.neat=1
            """
        cur.execute(q)

        rows = cur.fetchall()
        
        for row in rows:
            row['date'] = datetime.strftime(row['date'],"%Y-%m-%d %H:%M")

            if len(row['version']):
                row['service'] = "%s (%s)" % (row['service'], row['version'])
            
        return rows
    
    def getForensic(self):
        '''
        returns row data for the forensic view.
        '''
        cur = db.cursor(mdb.cursors.DictCursor)
        q= """select m.ip, m.hostname, s.id, s.port, s.machineId,
            s.product service, s.version, s.extrainfo, s.ffdate date
            from services s
            inner join servicelogCur l on s.id = l.serviceId
            inner join machines m on s.machineId = m.id
            where l.openp=1
            """
        cur.execute(q)

        rows = cur.fetchall()
        
        for row in rows:
            row['date'] = datetime.strftime(row['date'],"%Y-%m-%d %H:%M")
            
            if len(row['version']):
                row['service'] = "%s (%s)" % (row['service'], row['version'])

        return rows
    
    @staticmethod
    def tojson(someDict):
        '''
        converts row data to json format.
        '''
        response.content_type = 'application/json'
        return dumps(someDict)



class AspromScheduleModel(CronTab):
    '''
    This model abstracts access to the schedule, which consists of the users crontab and log data in the mysql DB.
    Both components are joined together using an UUID, the jobID.
    '''
    
    ## schedule log from database
    scheduleLog = None
    
    ## schedule data from crontab
    schedule = None
    
    ## dictionary of jobs indexed by id
    jobsByID = dict()
    
    
    def __init__(self, *args, **kwargs):
        '''
        standard Constructor
        '''
        super(AspromScheduleModel, self).__init__(*args, **kwargs)
        self.read()


    def read(self, filename=None):
        super(AspromScheduleModel, self).read(filename=filename)
        self.scheduleLog = self.fetchScheduleLog()
        self.schedule = self.fetchSchedule()


    @staticmethod
    def promoteToIndex(dici,valueKey):
        '''
        index the dic by valueKey.
        promotes the element on position <valueKey> from each sublist to an index in a dictionary.

        @param dic        a list of lists or a list of dictionaries, e.g. a database result set.
        @param valueKey   position or name of the value to be promoted to an index
        
>       example:

        >>> d = [[1,2,3,4,5], [6,7], [8,9], [9,10]]
        >>> e=AspromScheduleModel.promoteToIndex(d,1)
        >>> print e
        {9: [8], 2: [1, 3, 4, 5], 10: [9], 7: [6]}
        '''
        dic=copy.deepcopy(dici)
        rv={}
        for row in dic:
            rv[row.pop(valueKey)]=row
        
        return rv
 

    def fetchScheduleLog(self):
        '''
        returns last log entry of past runs for every defined job from the database.
        '''
        dbc = db.cursor(mdb.cursors.DictCursor)
        
        # get last log entry for each job
        q = '''select s.jobid, state, startdate, enddate, output from scanlog s
            inner join (
            select jobid, max(startdate) as maxstartdate from scanlog group by jobid
            ) gs
            on s.jobid = gs.jobid and gs.maxstartdate = s.startdate
            order by id asc'''
        dbc.execute(q)
        rows = dbc.fetchall()
 
        #index the result by jobid
        return self.promoteToIndex(rows, 'jobid')


    def getJobByID(self, jobid):
        '''
        returns the job with id <jobid>.
        
        @param jobid: the job's id.
        @return: a job object.
        '''
        
        #todo
        #return self.getScheduleI()[jobid]
        return self.jobsByID[jobid]
    

    
    def changeJob(self, jobid, cronval, iprange, portrange, extraparams, job = None):
        '''
        changes the parameters of the Job with UUID <jobid> in the crontab.
        @param    jobid:        the job to be edited.
        @param    cronval:      the cron schedule string.
        @param    iprange:      a CIDR range, single IP or hostname.
        @param    portrange:    a single port or port range in the format <startport>-<endport> to be scanned.
        @param    extraparams:  extra command line parameters for nmap.
        '''
        
        print "Controller.changeJob Input: "
        print "jobid: " + jobid
        print "cronval: " + cronval
        print "iprange: " + iprange
        print "portrange: " + portrange
        print "extraparams: " + extraparams
        
        # parameter assertions
        assert re.match('^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', jobid)
        assert len(cronval) > 5
        assert re.match('^([^-][^\s]+)$', iprange)
        assert re.match('^[\d-]*$', portrange)
        assert not re.match('["]', extraparams)

        if not job:
            job = self.getJobByID(jobid)
        
        job.setall(cronval)
        job.set_command('python %s/aspromScan.py -j %s %s%s%s' % 
                        (cfg.maindir, jobid, 
                         '-o="%s" ' % extraparams if extraparams else "",
                         "-p %s " % portrange if portrange else "",
                         iprange))
        job.set_comment('asprom %s' % datetime.now().strftime("%Y-%m-%d %H:%M"))

        job.enable()
        self.render()
        print "job enabled: " + str(job.is_enabled())
        self.write()
        self.read()

    def addJob(self, jobid, cronval, iprange, portrange, extraparams):
        '''
        adds a Job to the crontab.
        @param    jobid:        the job id to be added.
        @param    cronval:      the cron schedule string.
        @param    iprange:      a CIDR range, single IP or hostname.
        @param    portrange:    a single port or port range in the format <startport>-<endport> to be scanned.
        @param    extraparams:  extra command line parameters for nmap.
        '''
        
        print "Controller.addJob Input: "
        print "jobid: " + jobid
        print "cronval: " + cronval
        print "iprange: " + iprange
        print "portrange: " + portrange
        print "extraparams: " + extraparams

        job=self.new("/bin/true")
        try:
            self.changeJob(jobid, cronval, iprange, portrange, extraparams, job)
        except AssertionError:
            job.clear()
            raise                    

    
    def deleteJob(self, jobid):
        '''
        deactivates the job with id <jobid> and refreshes the model.
        
        @param jobid: the job's id.
        '''
        job=self.getJobByID(jobid)
        job.enable(False)
        job.set_comment('asprom %s' % datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.write()
        self.read()
    
    
    def getScheduleEntryByID(self, jobid):
        '''
        returns the job specifics for the job with id <jobid>.
        
        @param jobid: the job's id.
        @return: a dictionary with job parameters.
        '''
        
        return self.getScheduleI()[jobid]

 
    def __fetchJob(self, job):
        '''
        fetches the job specifics from crontab and database.
        
        @param job: the job to be parsed.
        @return: a dictionary with the following fields: id,when,iprange,sensor,lastrun,nextrun,laststate,params,ports.
        @raise NoJobIDException: will be raised if a job is encountered which has no job id, e.g. a non-asprom crontab entry.
        '''
        # get id
        m = re.search(r'-j[= ]([^\s]+) ', job.command)
        if (m and job.is_enabled()):
            uuidx = m.group(1)
                
            # get sensor
            m = re.search(r'-s[= ]([^\s]+) ', job.command)
            if m:
                sensor = m.group(1)
            else:
                sensor = "localhost"
            
            # get ip range
            m = re.search(r'[^-][^\s]+ ([^-][^\s]+)$', job.command)
            if m:
                iprange = m.group(1)
            else:
                iprange = "invalid"
            
            # port range
            m = re.search(r'-p[= ]([^\s]+) ', job.command)
            if m:
                ports = m.group(1)
            else:
                ports = ""

            # extra arguments
            m = re.search(r'-o=["\']([^"\']+)["\']', job.command)
            if m:
                params = m.group(1)
            else:
                params = ""
            
            ##############################
            # last log from database
            if uuidx in self.scheduleLog:
                lastLog=self.scheduleLog[uuidx]
                
                # last state
                if 'enddate' in lastLog and lastLog['enddate'] is not None:
                    laststate = lastLog['state'] + '(' + (lastLog['enddate'] - lastLog['startdate']).__str__() + ('h)')
                else:
                    laststate=lastLog['state']
                
                # start date
                if 'startdate' in lastLog or lastLog['startdate'] is not None:
                    startdate = datetime.strftime(lastLog['startdate'],"%Y-%m-%d %H:%M")
                else:
                    startdate = "-"
                    
            else:
                laststate="-"
                startdate="-"
                
            
            return ({ "id": uuidx, #uuid().__str__()
                 "when":job.slices.render(),
                 "iprange": iprange,
                 "sensor": sensor,
                 "lastrun": startdate,
                 "nextrun": datetime.strftime(job.schedule().get_next(),"%Y-%m-%d %H:%M"),
                 "laststate": laststate,
                 "params": params,
                 "ports": ports
               })
        else:
            # this is no crontab entry for asprom.
            raise NoJoibIDException('not a crontab entry for asprom, no jobid found: %s' % (job))


    def getSchedule(self):
        '''
        returns the schedule (crontab) in flat (unindexed) form, e.g. for GUI table data.
        '''
        return self.schedule
 
 
    def getScheduleI(self):
        '''
        returns the schedule (crontab) indexed by jobid.
        '''
        return self.promoteToIndex(self.schedule, 'id')

        
    def fetchSchedule(self):
        '''
        returns row data for the schedule view.
        '''
        rv = []
        
        #reread crontab from disk
        #self.read()
        
        # extract nmap arguments from crontab definition by regular expressions
        for job in self:
            try:
                #get the job specifics
                jobSpec = self.__fetchJob(job)
                pprint(jobSpec)
                rv.append(jobSpec)
                
                # also fill up the jobsByID attribute
                jobid=jobSpec['id']
                self.jobsByID[jobid]=job
                
            except NoJoibIDException:
                pass
        return rv


class Controller(object):
    '''
    The Controller defines all actions that are possible from within the GUI.
    '''

    @staticmethod
    def rescanJob(jobid):
        '''
        run the scheduled job with id <jobid> right now.
        
        @param jobid:    the UUID of the job to be run
        '''
        # get job schedule from cron
        SM = AspromScheduleModel(user=True)
        jobs = SM.promoteToIndex(SM.getSchedule(), 'id')
        
        if jobs[jobid]:
            j = jobs[jobid]
            print j
            ps = scan(j['iprange'], j['ports'], j['params'], jobid)
            
        return ps
    
            
    @staticmethod
    def rescanMachine(machineid, port=None):
        '''
        rescan the machine.
        this method finds the task in the schedule to which the machine belongs and takes its additional arguments from there.
        
        @param machineid: ID of the machine to be rescanned.
        @param port: port of the machine to be rescanned.
        '''

        # get job schedule from cron
        sm = AspromScheduleModel(user=True)
        jobs = sm.getSchedule()
        
        # get machine details from database
        machine = Machine(machineid)
        jobid = None

        for job in jobs:
            # first, check if iprange is an actual ip range and ip is in that range.
            try:
                if machine.ip in IPNetwork(job['iprange']):
                    jobid=job['id']
                    print "IP %s in range %s - jobid %s" % (machine.ip, job['iprange'], job['id'])
                    break
            except AddrFormatError, e:
                print "%s - trying by name resolution" % e
                # if not, check if iprange resolves to the given machine
                try:
                    if str(machine.ip) == socket.gethostbyname(job['iprange']):
                        jobid=job['id']
                        print "IP %s == %s - jobid %s" % (machine.ip, job['iprange'], job['id'])
                        break
                except Exception, e:
                    print "shit happened : %s" % e
                
        if jobid:
            ps = scan(str(machine.ip), str(port) if port else job['ports'], job['params'], jobid)
            
            return ps

    @staticmethod
    def rescanService(serviceid):
        '''
        rescans the service.
        
        @param serviceid: ID of the service to be rescanned.
        '''
        # get machine details from database
        serv = Service(serviceid)
        machine = serv.getMachine()

        return Controller.rescanMachine(machine.id, serv.port)

    @staticmethod
    def flipCrit(serviceid, exposed=True):
        '''
        flips the criticality of the service.
        Flipping sets the service criticality to WARNING if it was CRITICAL before and the other way round. 
        
        @param    serviceid    The Service whose criticality should be flipped.
        @param    page         Denominates the view on which the criticality of the service should be flipped. If true, "alerts-exposed" is flipped. Else, "alerts-closed".
        '''
        s=Service(int(serviceid))
        s.flipCrit(exposed)


    @staticmethod
    def approve(serviceid, justification):
        '''
        Using this method, a service can be approved to the neatline.
        
        @param    serviceid:        The Service ID to be approved.
        @param    justification:    a business justification for the service to be approved.
        '''
        s=Service(int(serviceid))
        s.approve(justification)
        
        
    @staticmethod
    def remove(serviceid, justification):
        '''
        Using this method, a service can be removed from the neatline.
        
        @param    serviceid:       The Service ID to be removed.
        @param    justification:   a business justification for the service to be removed.
        '''
        s=Service(int(serviceid))
        s.remove(justification)


class Service(object):
    '''
    This class represents a single Service, that is a port on a machine.
    '''
    
    ##attributes
    
    ## service id
    id = None
    
    ## machine object to which this service is associated
    machine = None
    
    ## port number of this service
    port = None
    
    ## additional product information gleaned by nmap
    product = None

    ## additional version information gleaned by nmap
    version = None
    
    ## additional extra information gleaned by nmap
    extrainfo = None
    
    ## datetime, when this service was last seen
    lsdate = None
    
    ## datetime, when this service was first seen
    ffdate = None
    
    ## flag: does this service raise a critical alert when exposed and not approved?
    critExposed = True

    ## flag: does this service raise a critical alert when closed and approved?
    critClosed = False


    def __init__(self, serviceid):
        '''
        Constructor.
        Loads all information about the service from the database.
        
        @param serviceid: Database id of the service.
        '''
        cur = db.cursor(mdb.cursors.DictCursor)
        q="""SELECT s.id id, m.id mid, port, s.ffdate, s.lsdate, s.product, s.version, s.extrainfo,
            c.flipExposed, c.flipClosed
            from machines m inner join services s
            on m.id = s.machineId
            left join criticality c
            on s.id = c.serviceId
            WHERE s.id=%d""" % serviceid
        cur.execute(q)
        row=cur.fetchone()
    
        self.id = row['id']
        self.machine = Machine(row['mid'])
        self.port = row['port']
        self.product = row['product']
        self.version = row['version']
        self.extrainfo = row['extrainfo']
        self.lsdate = row['lsdate']
        self.ffdate = row['ffdate']
        self.critExposed = True if 'flipExposed' in row and row['flipExposed'] == 1 else False
        self.critClosed = True if 'flipClosed' in row and row['flipClosed'] == 1 else False


    @staticmethod
    def create(mach, portno, product='', version='', extrainfo=''):
        '''
        create new service and return self
        
        @param mach: Machine object to which the service belongs
        @param portno: Port number of this service
        @param product: additional product information gleaned by nmap. if not defined, get generic information about port from /etc/services.
        @param version: additional version information gleaned by nmap
        @param extrainfo: additional extra information gleaned by nmap
        @return: self
        '''

        cur = db.cursor()
        
        # if product not defined, get generic information about port from /etc/services.
        if not product:
            try:
                product=socket.getservbyport(portno, 'tcp')
            except:
                pass

        pprint("creating service: %s:%s:%s:%s:%s" % (mach, portno, product, version, extrainfo))
        q="""INSERT INTO services (port, protocolId, machineId, product, extrainfo, version, lsdate, ffdate) 
            VALUES (%d, %d, %d, "%s", "%s", "%s", NOW(), NOW())
            ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id), lsdate=NOW(); """ % (portno, 1, mach.id, product, extrainfo, version) 
        print q
        cur.execute(q)
       
        mid=cur.lastrowid
        print "Service ID inserted: %s" % mid
        
        ## check if last log entry is negative
        q="""select openp from servicelog where serviceid=%d order by id desc limit 1""" % mid
        cur.execute(q)
        try:
            rv = cur.fetchone()[0]
        except (TypeError, KeyError):
            rv = False
        # if it is negative, insert a positive log entry
        if not rv:
            q="""INSERT INTO servicelog (serviceId, openp, date) values (%d, %d, NOW()) """ % (mid, 1) 
            cur.execute(q)

        db.commit()
        return Service(mid)

    
    def delete(self):
        '''
        deletes this service.
        '''
        cur = db.cursor()
        q="""DELETE FROM criticality WHERE serviceId = %d""" % (self.id)
        cur.execute(q)
        ## check if last log entry is positive
        q="""SELECT openp FROM servicelog WHERE serviceid=%d order by id desc limit 1""" % self.id
        cur.execute(q)
        try:
            rv = cur.fetchone()[0]
        except (TypeError, KeyError):
            rv = False
        # if it is positve, insert a negative log entry
        if rv:
            q="""INSERT INTO servicelog (serviceId, openp, date) values (%d, %d, NOW())""" % (self.id, 0)
            cur.execute(q)
        db.commit()
        

    def getMachine(self):
        '''
        returns the machine object associated with this service.
        '''
        return self.machine


    def inRange(self, r):
        '''
        tells if a service is in a specific port range.
        
        @param r: single port number or range, e.g. "1024-65535"
        '''
        #single port?
        if (isinstance(r, int) or r.isdigit()):
            return int(r) == self.port
        
        #range as string?
        m = re.search(r'^(\d+)-(\d+)$', r)
        if m:
            startr=m.group(1)
            endr=m.group(2)
            return int(startr) <= self.port <= int(endr)
        else:
            raise Exception('cannot determine if %s is in range %s' % (self.port, r))

    def flipCrit(self, exposed=True):
        '''
        Flip criticality of "exposed" view if exposed = true, else of the "closed" view
        '''
        if exposed:
            col = 'flipExposed'
            self.critExposed = not self.critExposed
            val=self.critExposed 
        else:
            col = 'flipClosed'
            self.critClosed = not self.critClosed
            val=self.critClosed

        cur = db.cursor()
        q="""INSERT INTO criticality (serviceId, %s)
            VALUES (%d, %d)
            ON DUPLICATE KEY UPDATE %s=%d""" % (col, self.id, val, col, val)
        print q
        cur.execute(q)
        db.commit()
    
    def approve(self, justification, neat=True):
        '''
        approve this service and add it to the neat line
        
        @param justification: a business justification.
        @param neat: true for approval. if false, remove from neat line. this is used by the method remove().
        '''
            
        cur = db.cursor()
        q="""INSERT INTO changelog (serviceId, neat, justification, date)
            VALUES (%d, %d, "%s", NOW())""" % (self.id, 1 if neat else 0, justification)
        cur.execute(q)
        q="UPDATE criticality SET flipExposed=0, flipClosed=0 WHERE serviceId = %d" % self.id
        cur.execute(q)
        db.commit()
        
    def remove(self, justification):
        '''
        remove this service from the neat line.

        @param justification: a business justification.
        '''
        self.approve(justification, False)    


class Machine(object):
    '''
    represents a machine, that is a singular IP adress.
    '''
    id = None
    hostname = None
    ip = None
    lsdate = None
    ffdate = None

    def __init__(self, machineid):
        '''
        Constructor
        Loads all information about the machine from the database.     
           
        @param machineid: Database id of the machine.
        '''
        cur = db.cursor(mdb.cursors.DictCursor)
        q="SELECT id, ip, hostname, lsdate, ffdate FROM machines WHERE id='%d'" % machineid
        cur.execute(q)
        row=cur.fetchone()
    
        self.id = int(row['id'])
        self.ip = IPAddress(row['ip'])
        self.hostname = row['hostname']
        self.lsdate = row['lsdate']
        self.ffdate = row['ffdate']
        
    @staticmethod
    def create(name, ip):
        '''
        create new Machine and return self.
        
        @param name: hostname
        @param ip: ip address
        @return: self
        '''
        cur = db.cursor(mdb.cursors.DictCursor)
        q="""INSERT INTO machines (hostname, ip, rangeId, lsdate, ffdate) 
            VALUES ("%s", "%s", %d, NOW(), NOW())
            ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id), hostname="%s", lsdate=NOW(); """ % (name, ip, 1, name) 

        print q
        cur.execute(q)


        mid=cur.lastrowid
        print "Machine ID inserted: %s" % mid

        ## check if last log entry is negative
        q="""select exposed from machinelog where machineId=%d order by id desc limit 1""" % mid
        cur.execute(q)
        try:
            rv = cur.fetchone()['exposed']
        except (TypeError):
            rv = False
        # if it is negative, insert a positive log entry
        if not rv:
            q="""INSERT INTO machinelog (machineId, exposed, date) values (%d, %d, NOW()) """ % (mid, 1) 
            cur.execute(q)

        
        
        db.commit()
        return Machine(mid)

    def getServices(self, exposedOnly=False):
        '''
        return list of services associated with this machine.
        
        @param exposedOnly: if true, only return currently exposed services.
        '''
        cur = db.cursor()
        q="""select id from services s inner join servicelogCur l on s.id=l.serviceId where machineId = %d %s""" % ( 
            self.id, "AND openp=1" if exposedOnly else "")
        
        cur.execute(q)
        rows = cur.fetchall()
        services=[]

        print 'ho:'
        print rows

        for row in rows:
            s=Service(int(row[0]))
            services.append(s)
        
        return services


    def delete(self):
        '''
        delete self.
        '''
        print "deleting machine %s" % self.id
        cur = db.cursor()
        ## check if last log entry is positive
        q="""select exposed from machinelog where machineId=%d order by id desc limit 1""" % self.id
        cur.execute(q)
        try:
            rv = cur.fetchone()[0]
        except (TypeError, KeyError):
            rv = False
        # if it is positive, insert a negative log entry
        if not rv:
            q="""INSERT INTO machinelog (machineId, exposed, date) values (%d, %d, NOW())""" % (self.id, 0)
            cur.execute(q)

        cur.execute(q)
        db.commit()


    @staticmethod
    def inRange(r, ip):
        '''
        returns true if ip is in range r, false otherwise.
        
        @param r: range
        @param ip: ip address
        @return: true if ip is in range r, false otherwise.
        '''
        #single ip?
        m = re.search(r'^[\d]{1-3}\.[\d]{1-3}\.[\d]{1-3}\.[\d]{1-3}$', r)
        if m:
            ri = IPAddress(r)
            return ri == r
        
        #hostname?
        m = re.search(r'^[^\d][^ ]+$', r)
        if m:
            return socket.gethostbyname(r) == str(ip)

        #cidr range as string?
        try:
            rn = IPNetwork(r)
            return ip in rn
        except:
            pass
        #    raise Exception('cannot determine if %s is in range %s' % (self.ip, r))
        
        raise Exception('cannot determine if %s is in range %s' % (ip, r))
    
    @staticmethod
    def getIPsInRange(r, exposedOnly=False):
        '''
        return a dictionary of IPs to IDs for all known hosts in the defined range.
        
        @param r: ip range
        @return: dictionary IPs/Machine IDs in that range
        '''
        
        cur = db.cursor()
        q="""select id, ip from machines"""
        
        cur.execute(q)
        rows = cur.fetchall()
        cur.close()
        
        inRangeIPs = {}
        
        for row in rows:
            if Machine.inRange(r, row[1]):
                inRangeIPs[row[1]] = row[0]
        
        return inRangeIPs


def scan(target, port_range, extra_options, job_id, sensor='localhost'):
    '''
    Scans the port range on the target IP/IP Range with nmap.
    extra_options are passed as CLI arguments to nmap.
    The job_id will be saved to the changelog entry in the database for reference to the actual job.
    
    @param    target           CIDR Range, singular IP or hostname
    @param    port_range       range of ports to be scanned
    @param    extra_options    extra CLI arguments to be passed to nmap
    @param    job_id           job UUID as used by the schedule model
    @param    sensor           In future versions, you may specify a sensor to be used for scanning (not implemented yet).
    '''
    #get db
    cur = db.cursor()

    #set all IN PROGRESS log entries older than one day to TIMEOUT
    q="update scanlog set state='TIMEOUT' where state='IN PROGRESS' and datediff(now(), startdate) > 1"
    cur.execute(q)

    #log start of scan
    q="""INSERT INTO scanlog (jobid, state, startdate, iprange, portrange, extraoptions) 
        VALUES ("%s", "%s", NOW(), "%s", %s, %s)""" % (
        "%s" % job_id if job_id else "Null", "IN PROGRESS",
        target,
        "%s" % port_range if port_range else "Null",
        "'%s'" % extra_options if extra_options else "Null") 
    
    cur.execute(q)
    logid=cur.lastrowid
    db.commit()
    cur.close()
            
    try:

        #start port scanner
        ps = nmap.PortScanner()
        #recode to ascii - utf not allowed
        ps.scan(target.encode('ascii'), port_range.encode('ascii') if port_range else None, extra_options.encode('ascii'))

        cur = db.cursor()
    
        #machines
        #remove old machines
        oldmachs=Machine.getIPsInRange(target.encode('ascii'), exposedOnly=True)
        print "known machines in range %s: %s" % (target, oldmachs)
        print "machines found by scan: %s" % ps.all_hosts()
        for hostip in filter(lambda x:False if x in ps.all_hosts() else True, oldmachs.keys()):
            #print "deleting %s" % hostip
            mach=Machine(oldmachs[hostip])
            for svc in mach.getServices(exposedOnly=True):
                print "deleting service %s on %s" % (svc.port, hostip)
                svc.delete()            
        
        #create new machines, add/remove services
        for hostip in ps.all_hosts():
            host=ps[hostip]

            
            #if nmap did not determine hostname, try be reverse name resolution
            if not (host['hostname'] and len(host['hostname'])):
                    from socket import gethostbyaddr, herror
                    try:
                        host['hostname'] = gethostbyaddr(hostip)[0]
                    except herror:
                        host['hostname'] = ''


            #create new machines             
            mach = Machine.create(host['hostname'], hostip)
            #open ports
            if 'tcp' in host:
                portnumbers = filter(lambda x:True if host['tcp'][x]['state'] == 'open' else False, host['tcp'].keys())
                #delete old services
                for svc in mach.getServices(exposedOnly=True):
                    print "STK: %s" % svc.port
                    # if port not detected anymore and in scanned range, delete it
                    if not svc.port in portnumbers and (svc.inRange(port_range) if port_range else True):
                        print "deleting %s" % svc.port
                        svc.delete()
                    
                #create new services
                for portno in portnumbers:
                    port=host['tcp'][portno]
                    if port['state'] == 'open':
                        print "creating %s" % portno
                        Service.create(mach, portno, port['product'], port['version'], port['extrainfo'])
        
        #log
        state="OK"
        message=None
        
    except:
        state="FAILED"
        message=traceback.format_exc()
        print message
        
    finally:
        #log
        cur=db.cursor()
        q="""UPDATE scanlog SET state="%s", enddate=NOW(), output=%s 
            WHERE ID=%d""" % ( state, "'%s'" % db.escape_string(message) if message else "NULL", logid) 

        cur.execute(q)    
        #print message
                
        db.commit()
        return state

def initDB():
    global db
    global cfg
    cfg = Cfg()
    db = mdb.connect(**cfg.db)


def closeDB():
    global db
    try:
        db.commit()
        db.close()
    except mdb.OperationalError:
        pass
    
    
