<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>asprom: {{title}}</title>
    
    <script src="static/js/jquery.min.js"></script>
    <script src="static/js/bootstrap.min.js"></script>
    <script src="static/js/bootstrap-table.min.js"></script>
    <script src="static/js/bootstrap-editable.min.js"></script>
    <script src="static/js/bootstrap-dialog.min.js"></script>
    <script src="static/js/jquery-cron-min.js"></script>
    <script src="static/js/asprom.js"></script>
    <link href="static/css/bootstrap.min.css" rel="stylesheet" media="screen">
    <link href="static/css/bootstrap-table.min.css" rel="stylesheet" media="screen">
    <link href="static/css/bootstrap-theme.min.css" rel="stylesheet" media="screen">
    <link href="static/css/bootstrap-editable.css" rel="stylesheet" media="screen">
    <link href="static/css/bootstrap-dialog.min.css" rel="stylesheet" media="screen">
    <link href="static/css/jquery-cron.css" rel="stylesheet" media="screen">
    <link href="static/css/asprom.css" rel="stylesheet" media="screen">
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <div class="container-fluid">
	    <div class="row">
		    <section class="col col-md-11">
		    	<header class="clearfix">
		    		<h1>asprom   <small>assault profile monitor</small></h1>
					<ul class="nav nav-tabs nav-fixed-top" role="tablist">
					  <li {{! 'class="active"' if title == "alerts-exposed" else "" }}><a href="alerts-exposed">alerts: exposed</a></li>
					  <li {{! 'class="active"' if title == "alerts-closed" else "" }}><a href="alerts-closed">alerts: closed</a></li>
					  <li {{! 'class="active"' if title == "baseline" else "" }}><a href="baseline">baseline</a></li>
					  <li {{! 'class="active"' if title == "posture" else "" }}><a href="posture">posture</a></li>
					  <li {{! 'class="active"' if title == "schedule" else "" }}><a href="schedule">schedule</a></li>
					</ul>
		    	</header>
		    </section>
		    <section class="col col-md-1 text-center">
		    	<br/>
		    	<h1><i class="glyphicon glyphicon-tower xlarge"></i></h1>
		    </section>
		</div>
		<div class="row">
		    <section class="col col-md-12">
		    	<header class="clearfix">
		    	<div id="notification-area" class="alert-block"></div>
		    	{{!base}}
		    	<div class="well well-sm"><h4>last changes</h4>
			    	<p id="log"></p>
			    </div>
		    	</header>
			</section>
	    </div>
    </div>
  </body>
</html>