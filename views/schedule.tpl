% rebase('base.tpl', title='schedule')
		    <script src="/static/js/later.js" type="text/javascript"></script>
		    <script src="/static/js/moment.min.js" type="text/javascript"></script>
		    <script src="/static/js/prettycron.js" type="text/javascript"></script>
			    <form role="form">
	   			    <table id="datatable" class="table" data-toggle="table" data-url="json/schedule" data-sort-name="nextrun" data-sort-order="asc"
	   			    	data-show-refresh="true" data-show-toggle="true" data-show-columns="true" data-search="true" data-id-field="id"
	   			    	data-row-style="rowStyle"> 
					    <thead>
					        <tr>
					            <th data-field="id" data-align="right" data-sortable="true" data-visible="false">ID</th>
					            <th data-field="when" data-align="center" data-sortable="true" data-formatter="whenFormatter">when</th>
					            <th data-field="iprange" data-sortable="true">IP Range</th>
					            <th data-field="sensor" data-sortable="true" data-visible="false">Sensor</th>
					            <th data-field="lastrun" data-sortable="true">Last Run</th>
					            <th data-field="nextrun" data-sortable="true">Next Run</th>
					            <th data-field="laststate" data-sortable="true">Last Status</th>
					            <th data-field="params" data-visible="false">extra Parameters</th>
					            <th data-field="ports" data-visible="false">Port range</th>
								<th data-field="operate" data-formatter="operateFormatterSchedule" data-events="operateEvents"
									data-switchable="false" data-align="center" data-width="80" ></th>
					        </tr>
					    </thead>
					</table>
					<button class="btn btn-primary" id="addjob" type="button">Add new...</button>
    			</form>
    			<hr>
    			<div class="jumbotron">
				   <h2>About this view</h2>
					  <p>In the schedule, you define which network ranges should be checked, and when they should be checked.</p>
					  <p class="moretolearn">You can change the settings of each job by clicking the edit button <i class="glyphicon glyphicon-edit"></i>.
						You can also run each scan right now by clicking the magnifying glass <i class="glyphicon glyphicon-search"></i>.
						When you delete <i class="glyphicon glyphicon-remove"></i> a job in this interface, asprom will comment it out in the users' crontab.</p>
					  <p><a class="btn btn-primary btn-lg" role="button" id="learnmore">Learn more</a></p>
				</div>
			<script>
			// Button Events
			$('#addjob').on('click', function(event) {
			  BootstrapDialog.show({
		    	message: $('<div></div>').load('/dia/addjob')
	  		  });
			});
			</script>