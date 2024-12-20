'''
Created on Oct 19, 2014

@author stefankn
@namespace asprom.aspromGUI
Main Script for the asprom GUI. This script presents a webserver socket to
which client browsers can connect to.
Also, it orchestrates URL calls between the model, view and controller classes.
'''
from bottle import (route, run, static_file, abort, redirect, template,
                        post, request, hook, response)
from inc.asprom import (AspromModel, AspromScheduleModel, Controller, Machine, initDB,
                        closeDB, Cfg)

# Variable definitions

## relative path to static files
sr = 'static/'

## main model
M = None

## schedule model
SM = None

localconf = Cfg()

#
# hooks
#


@hook('before_request')
def before_request():
    '''
    before each dynamic request, create DB connection and Model instances.
    '''
    username = None
    try:
        username = request.get_header("X-Forwarded-User", request.auth[0])
    except:
        pass

    p = request.path
    if p.startswith('/' + sr):
        return
    global M, SM
    try:
        initDB(localconf)
        M = AspromModel(username=username)
        SM = AspromScheduleModel(user=True)
    except:
        raise

#
# routes
#


@route('/')
def serve_homepage():
    '''
    HTTP Redirect to http:///alerts-exposed.
    '''
    redirect('/alerts-exposed')

# main views


@route('/alerts-exposed')
def serve_alertsexposed():
    '''
    Presents view: http:///alerts-exposed.
    '''
    return template('views/alerts-exposed')


@route('/alerts-closed')
def serve_alertsclosed():
    '''
    Presents view: http:///alerts-closed.
    '''
    return template('views/alerts-closed')


@route('/baseline')
def serve_baseline():
    '''
    Presents view: http:///baseline.
    '''
    return template('views/baseline')


@route('/posture')
def serve_forensic():
    '''
    Presents view: http:///posture.
    '''
    return template('views/posture')


@route('/schedule')
def serve_schedule():
    '''
    Presents view: http:///schedule.
    '''
    return template('views/schedule')


@route('/log')
def serve_log():
    '''
    Presents view: http:///log.
    '''
    return M.getLastLog(10)


# dialog views
@route('/dia/editjob/<jobid:re:[0-9a-f]{8}-[0-9a-f]{4}-\
[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}>')
def serve_editjob_view(jobid):
    '''
    Presents view: http:///dia/editjob.
    This is meant to be used as a dialog popup in the schedule view.
    On this dialog, the parameters of an existing job can be edited.

    @param    jobid    the job ID to be edited.
    '''

    j = SM.getScheduleEntryByID(jobid)
    return template('views/editjob', jobid=jobid, initial=j['when'], iprange=j
                    ['iprange'], portrange=j['ports'], extraparams=j['params'])


@route('/dia/addjob')
def serve_addjob_view():
    '''
    Presents view: http:///dia/addjob.
    This is meant to be used as a dialog popup in the schedule view.
    On this dialog, the parameters of a new job can be entered.
    '''
    from uuid import uuid4
    return template('views/addjob', jobid=str(uuid4()), initial='0 1 * * *',
                    iprange='192.168.0.0/24', portrange='0-1024',
                    extraparams='-sV')


# JSON Views
@route('/json/<filename:path>')
def returnjson(filename):
    '''
    Presents all json views: http:///json/*.
    These are used by the tables embedded in the main html views.
    The data is aquired using ajax calls.
    The data is pulled from the model in dict format and then converted
    to json.

    @param    filename    the json view to be shown. can be any of
        alerts-exposed, alerts-closed, baseline, posture or schedule.
    '''
    if filename == 'alerts-exposed':
        return M.tojson(M.getAlertsExposed())
    elif filename == 'alerts-closed':
        return M.tojson(M.getAlertsClosed())
    elif filename == 'baseline':
        return M.tojson(M.getNeatline())
    elif filename == 'posture':
        return M.tojson(M.getForensic())
    elif filename == 'schedule':
        return M.tojson(SM.getSchedule())
    else:
        abort(404, "undefined json")
    closeDB()


# JSON Views
@route('/plain/<filename:path>')
def returnplain(filename):
    '''
    Presents all plaintext views: http:///plain/*.
    These are used by other scripts, like markusk's openvas-config-script

    @param    filename    the plaintext view to be shown.
    '''
    response.content_type = 'text/plain'
    if filename == 'scanned-ranges':
        return SM.getScannedRanges()
    else:
        abort(404, "undefined url")
    closeDB()


# controller
# rescan
@route('/controller/rescanjob/<jobid:re:[0-9a-f]{8}-[0-9a-f]{4}-\
[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}>')
def serve_rescanController(jobid):
    '''
    Activates controller: http:///controller/rescanjob/<jobid>.
    Instructs the controller to perform a forensic rescan of
    the job with id <jobid> now.

    @param    jobid    the job ID to be scanned.
    '''
    rv = Controller.rescanJob(jobid)
    closeDB()
    return rv


@route('/controller/rescanmachine/<host:re:[0-9]+>')
@route('/controller/rescanmachine/<host:re:[0-9]+>/<port:re:[0-9]+>')
def serve_rescanMachine(host, port=None):
    '''
    Activates controller: http:///controller/rescanmachine/<hostid>[/<portid>].
    Instructs the controller to perform a forensic rescan of the machine
    with id <hostid> now.
    If <portid> is present, only this single port is being rescanned.

    @param    host    the host ID to be scanned.
    @param    port    the port to be rescanned on the specified machine.
    '''
    assert host.isdigit()
    rv = Controller.rescanMachine(int(host), int(port) if port else None)
    closeDB()
    return rv


@route('/controller/rescanservice/<serviceid:re:[0-9]+>')
def serve_rescanService(serviceid):
    '''
    Activates controller: http:///controller/rescanservice/<serviceid>.
    Instructs the controller to perform a forensic rescan of the service
    with id <serviceid> now.

    @param    serviceid    The Service ID to be scanned.
    '''
    assert serviceid.isdigit()
    rv = Controller.rescanService(int(serviceid))
    closeDB()
    return rv

@route('/controller/deletemachine/<machineid:re:[0-9]+>')
def serve_deleteMachine(machineid):
    '''
    Activates controller: http:///controller/deletemachine/<machineid>.
    Deletes the machine and all its associated services from inventory.

    @param    machineid    The Machine ID to be deleted.
    '''
    assert machineid.isdigit()
    machine = Machine(int(machineid))
    
    # Delete all services first
    for service in machine.getServices():
        service.delete()
        
    # Then delete the machine
    machine.delete()
    
    closeDB()
    return "ok"

@route('/controller/deletejob/<jobid:re:[0-9a-f]{8}-[0-9a-f]{4}-\
[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}>')
def serve_deleteJob(jobid):
    '''
    Activates controller: http:///controller/deletejob/<jobid>.
    Instructs the controller to delete the job with id <jobid>.

    @param    jobid    The Job ID to be scanned.
    '''
    rv = SM.deleteJob(jobid)
    closeDB()
    return rv


# flipcrit
@route('/controller/flipcrit/<page:re:(exposed|closed)>/<serviceid:re:[0-9]+>')
def serve_flipCrit(page, serviceid):
    '''
    Activates controller:
     http:///controller/flipcrit/<exposed|closed>/<serviceid>.
    Instructs the controller to flip the criticality of service <serviceid> on
    the alerts-<exposed|closed> view.
    Flipping sets the service criticality to WARNING if it was CRITICAL before
    and the other way round.

    @param    page         Either "exposed" or "closed". Denominates the view
     on which the criticality of the service should be flipped.
    @param    serviceid    The Service whose criticality should be flipped.
    '''
    exposed = True if page == "exposed" else False
    Controller.flipCrit(serviceid, exposed)
    closeDB()

# approve


@post('/controller/approve')
def serve_approve():
    '''
    Activates controller: http:///controller/approve.
    The arguments are to be passed by using the HTTP POST method.
    Using this method, a service can be approved to the baseline.

    @param    pk    The Service ID to be approved.
    @param    value a business justification for the service to be approved.
    '''
    serviceid = request.forms.get('pk')
    justification = request.forms.get('value')
    Controller.approve(int(serviceid), justification, M.username)
    closeDB()

# remove


@post('/controller/remove')
def serve_remove():
    '''
    Activates controller: http:///controller/remove.
    The arguments are to be passed by using the HTTP POST method.
    Using this method, a service can be removed from the baseline.

    @param    pk    The Service ID to be removed.
    @param    value a business justification for the service to be removed.
    '''
    serviceid = request.forms.get('pk')
    justification = request.forms.get('value')
    Controller.remove(int(serviceid), justification, M.username)
    closeDB()

# edit job


@post('/controller/editjob/<jobid:re:[0-9a-f]{8}-[0-9a-f]{4}-\
[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}>')
def serve_changejob(jobid):
    '''
    Activates controller: http:///controller/editjob/<jobid>.
    This method tells the controller to set or change the parameters
    of the specified job.

    @param    jobid the job to be edited.

    The following arguments are to be passed by using the HTTP POST method.

    @param    cronval      the cron schedule string.
    @param    iprange      a CIDR range, single IP or hostname.
    @param    portrange    a single port or port range in the format
     <startport>-<endport> to be scanned.
    @param    extraparams  extra command line parameters for nmap.
    '''
    rv = SM.changeJob(jobid=jobid,
                      cronval=request.forms.get('cronval'),
                      iprange=request.forms.get('iprange'),
                      portrange=request.forms.get('portrange'),
                      extraparams=request.forms.get('extraparams')
                      )
    closeDB()
    return rv

# edit job


@post('/controller/addjob/<jobid:re:[0-9a-f]{8}-[0-9a-f]{4}-\
[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}>')
def serve_addjob(jobid):
    '''
    Activates controller: http:///controller/addjob/<jobid>.
    This method tells the controller to set the parameters of the specified job
    and add it to crontab.

    @param    jobid the job to be edited.

    The following arguments are to be passed by using the HTTP POST method.

    @param    cronval      the cron schedule string.
    @param    iprange      a CIDR range, single IP or hostname.
    @param    portrange    a single port or port range in the format
     <startport>-<endport> to be scanned.
    @param    extraparams  extra command line parameters for nmap.
    '''
    rv = SM.addJob(jobid=jobid,
                   cronval=request.forms.get('cronval'),
                   iprange=request.forms.get('iprange'),
                   portrange=request.forms.get('portrange'),
                   extraparams=request.forms.get('extraparams')
                   )
    closeDB()
    return rv


# static files
@route('/' + sr + '<filename:path>')
def static(filename):
    '''
    returns static files from the path defined by variable SR.

    @param    filename    path to the static file relative to the SR directory.
    '''
    return static_file(filename, root=sr)


# run the service!
run(host=localconf['server']['listen'], port=localconf['server']['port'],
    debug=localconf['server']['debug'], server='paste')
