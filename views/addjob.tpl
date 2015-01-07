<h2>Add Schedule</h2>

<script type="text/javascript">
$(document).ready(function() {
    $('#selector').cron({
	    initial: "{{initial}}",
	    customValues: {
	        "15 Minutes" : "*/15 * * * *",
	    },
	    onChange: function() {
	        $('#cronval').val($(this).cron("value"));
    	
    	}
	}); 
	$('#cronval').change(function() {
		$('#selector').cron("value", this.value);
	});
    $(".dropdown-menu li a").click(function(){
	  $(this).parents(".input-group-btn").find('.btn').text($(this).text());
	  $(this).parents(".input-group-btn").find('.btn').val($(this).text());
	});
	$('#submitt').click(function() {
		// validate and process form here
		var cronval = $("input#cronval").val();
		var iprange = $("input#iprange").val();
		var portrange = $("input#portrange").val();
		var extraparams = $("input#extraparams").val();
		var dataVal = 'cronval='+ cronval + '&iprange=' + iprange + '&portrange=' + portrange + '&extraparams=' + extraparams;

		// submit to controller by ajax call
		$.ajax({
			url: "/controller/addjob/{{jobid}}",
			type: "POST",
			cache: false,
			data: dataVal,
			success: function( json ) {
				addAlert("Added new Job ID {{jobid}}", 'success', true);
				$('#datatable').bootstrapTable('refresh');
				BootstrapDialog.closeAll();
			},
			error: function( xhr, status, errorThrown ) {
				addAlert("Error adding Job ID {{jobid}}", 'danger');
			},
		});
	});
	
});
</script>

<div class="input-group">
	<span class="input-group-addon">Schedule</span>
	<input type="text" id='cronval' class="form-control"/>
	<div id='selector'></div>
</div>
<br/>
<div class="input-group">
  <span class="input-group-addon">IP Range</span>
  <input type="text" class="form-control" id="iprange" placeholder="{{iprange}}">
</div>
<br/>
<div class="input-group">
  <span class="input-group-addon">Port Range</span>
  <input type="text" class="form-control" id="portrange" placeholder="{{portrange}}">
</div>
<br/>
<div class="input-group">
  <span class="input-group-addon">extra Parameters</span>
  <input type="text" class="form-control" id="extraparams" placeholder="{{extraparams}}">
</div>
<br/>
<!---
<div class="input-group">
	<span class="input-group-addon">Sensor</span>
	<div class="input-group-btn">
      <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
          localhost
         <span class="caret"></span>
      </button>
      <ul class="dropdown-menu">
         <li><a>localhost</a></li>
      </ul>
   </div><br/>
</div>
--->
<br>

<button id="submitt" class="btn btn-default">Add Job</button>
