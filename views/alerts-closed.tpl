% rebase('base.tpl', title='alerts-closed')
			    <form role="form">
	   			    <table id="datatable" class="table" data-toggle="table" data-url="json/alerts-closed" data-sort-name="id" data-sort-order="asc"
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
					            <th data-field="date" data-sortable="true">date of approval</th>
					            <th data-field="justification" data-switchable="true">business justification</th>
								<th data-field="operate" data-formatter="operateFormatterClosed" data-events="operateEvents"
									data-switchable="false" data-align="center" data-width="80" ></th>
					        </tr>
					    </thead>
					    <tbody id='dataform'></tbody>
					</table>
    			</form>
    			<hr>
    			<div class="jumbotron">
				   <h2>About this view</h2>
					  <p>These Ports are closed, but the "neat line" specifies a business justification for them to be open.</p>
					  <p><a class="btn btn-primary btn-lg" role="button">Learn more</a></p>
				</div>
				