% rebase('base.tpl', title='posture')
			    <form role="form">
	   			    <table id="datatable" class="table" data-toggle="table" data-url="json/posture" data-sort-name="ip" data-sort-order="asc"
	   			    	data-show-refresh="true" data-show-toggle="true" data-show-columns="true" data-search="true" data-id-field="id"
	   			    	data-row-style="rowStyle"> 
					    <thead>
					        <tr>
					            <th data-field="id" data-align="right" data-sortable="true" data-visible="false">ID</th>
					            <th data-field="ip" data-align="center" data-sortable="true">IP</th>
					            <th data-field="hostname" data-sortable="true">Hostname</th>
					            <th data-field="port" data-sortable="true">Port</th>
					            <th data-field="service" data-sortable="true">Service</th>
					            <th data-field="extrainfo" data-sortable="true" data-visible="false">extra info</th>
					            <th data-field="date" data-sortable="true">first found</th>
								<th data-field="operate" data-formatter="operateFormatterForensic" data-events="operateEvents"
									data-switchable="false" data-align="center" data-width="80" ></th>
					        </tr>
					    </thead>
					    <tbody id='dataform'></tbody>
					</table>
    			</form>
    			<hr>
    			<div class="jumbotron">
				   <h2>About this view</h2>
					  <p>The security posture is the actual profile of your networks found by forensic means.</p>
					  <p class="moretolearn">You may rescan single ports by clicking the "rescan" button <i class="glyphicon glyphicon-search"></i>.</p>
					  <p><a class="btn btn-primary btn-lg" role="button" id="learnmore">Learn more</a></p>
				</div>
				