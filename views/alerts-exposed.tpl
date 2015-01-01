% rebase('base.tpl', title='alerts-exposed')
			    <form role="form">
	   			    <table id="datatable" class="table" data-toggle="table" data-url="json/alerts-exposed" data-sort-name="ip" data-sort-order="asc"
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
								<th data-field="operate" data-formatter="operateFormatterExposed" data-events="operateEvents"
									data-switchable="false" data-align="center" data-width="80" ></th>
					        </tr>
					    </thead>
					    <tbody id='dataform'></tbody>
					</table>
    			</form>
    			<hr>
    			<div class="jumbotron">
				   <h2>About this view</h2>
					  <p>These Ports are unintentionally open and therefore to be checked with the highest priority.</p>
					  <p><a class="btn btn-primary btn-lg" role="button">Learn more</a></p>
				</div>
				