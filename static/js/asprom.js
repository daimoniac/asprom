function operateFormatterExposed(value, row, index) {
    return [
        '<toggle class="approve" title="Add to neat line">',
            '<i data-type="text" data-pk="' + row.id + '" data-name="ap' + row.id + '" data-title="Enter business justification" data-value="" class="glyphicon glyphicon-ok"></i>',
        '</toggle>',
        '<toggle class="rescan ml10" title="Rescan">',
            '<i class="glyphicon glyphicon-search"></i>',
        '</toggle>',
        '<toggle class="critEx ml10" title="Flip criticality">',
            '<i class="glyphicon glyphicon-star"></i>',
        '</toggle>'
    ].join('');
}

function operateFormatterClosed(value, row, index) {
    return [
        '<toggle class="remove" title="Remove from neat line">',
        	'<i data-type="text" data-pk="' + row.id + '" data-name="rm' + row.id + '" data-title="Enter business justification" data-value="" class="glyphicon glyphicon-remove"></i>',
	    '</toggle>',
	    '<toggle class="rescan ml10" title="Rescan">',
	        '<i class="glyphicon glyphicon-search"></i>',
	    '</toggle>',
	    '<toggle class="critCl ml10" title="Flip criticality">',
	        '<i class="glyphicon glyphicon-star"></i>',
	    '</toggle>'
   ].join('');
}

function operateFormatterNeatline(value, row, index) {
    return [
        '<toggle class="remove" title="Remove from neat line">',
        '<i data-type="text" data-pk="' + row.id + '" data-name="rm' + row.id + '" data-title="Enter business justification" data-value="" class="glyphicon glyphicon-remove"></i>',
	    '</toggle>',
	    '<toggle class="rescan ml10" title="Rescan">',
	        '<i class="glyphicon glyphicon-search"></i>',
	    '</toggle>'
   ].join('');
}


function operateFormatterSchedule(value, row, index) {
    return [
        '<toggle class="editjob" title="Edit">',
        	'<i class="glyphicon glyphicon-edit"></i>',
        '</toggle>',
        '<toggle class="rescanjob ml10" title="Rescan">',
            '<i class="glyphicon glyphicon-search"></i>',
        '</toggle>',
        '<toggle class="deletejob ml10" title="Delete">',
            '<i class="glyphicon glyphicon-remove"></i>',
        '</toggle>'
    ].join('');
}

function operateFormatterForensic(value, row, index) {
    return [
	    '<toggle class="rescan ml10" title="Rescan">',
	        '<i class="glyphicon glyphicon-search"></i>',
	    '</toggle>',
    ].join('');
}


function whenFormatter(value, row) {
    return '<span class="tthost" title="' + prettyCron.toString(value) + '" data-toggle="tooltip" data-placement="left" onload="this.tooltip()">' + value + '</span>';
}


function rowStyle(row, index) {
	if ((typeof(row.crit) !== 'undefined') && (row.crit !== null)) {
	    if ( row.crit ) {
	    	if (index % 2) {
	    		return {classes:'alert-danger'};
	    	} else {
	    		return {classes:'alert-danger danger-2'}
    		}
	    } else {
	    	if (index % 2) {
	    		return {classes:'alert-warning'};
	    	} else {
	    		return {classes:'alert-warning warning-2'}
    		}
	    }
	}
	else {
    	if (index % 2) {
    		return {classes:'alert-info aspinfo'};
    	} else {
    		return {classes:'alert-info aspinfo-2'};
    	}
	}
	return{classes:''};
}

window.operateEvents = {
    'click .rescanjob': function (e, value, row, index) {
        subRescan("job", row.id);
        console.log("rescan scheduled for" + row.id);
    },
    'click .rescan': function (e, value, row, index) {
        subRescan("service", row.id);
        console.log("rescan scheduled for" + row.id);
    },
    'click .critEx': function (e, value, row, index) {
        subFlipCrit('exposed', row.id)
        console.log(value, row, index);
    },
    'click .critCl': function (e, value, row, index) {
        subFlipCrit('closed', row.id)
        console.log(value, row, index);
    },
    'click .editjob': function (e, value, row, index) {
        subEditJob(row.id);
        console.log(value, row, index);
    },
    'click .deletejob': function (e, value, row, index) {
        subDeleteJob(row.id);
        console.log(value, row, index);
    },
};

// Button events

function subEditJob(argId)
BootstrapDialog.show({
    message: $('<div></div>').load('/dia/editjob/' + argId)
});

function subDeleteJob(argId)
$.ajax({
	url: "/controller/deletejob/" + argId,
	type: "GET",
	success: function( json ) {
		$('#datatable').bootstrapTable('refresh');
	},
	error: function( xhr, status, errorThrown ) {
		addAlert("Error deleting job " + argId + ".", 'danger');
	},
});


// AJAX Stuff
function subRescan(type, argId)
//Using the core $.ajax() method
$.ajax({
// the URL for the request
url: "/controller/rescan" + type + "/" + argId,
type: "GET",
// the type of data we expect back
//dataType : "json",
beforeSend: function () {
	addAlert("Commencing rescan of " + type + " " + argId + ".", 'info', true);
},
// code to run if the request succeeds;
// the response is passed to the function
success: function( json ) {
	$('#datatable').bootstrapTable('refresh');
	addAlert("Successfully rescanned " + type + " " + argId + ".", 'success', true);
},
// code to run if the request fails; the raw request and
// status codes are passed to the function
error: function( xhr, status, errorThrown ) {
	addAlert("Error rescanning " + type + " " + argId + ".", 'danger');
},
// code to run regardless of success or failure
//always: function( xhr, status ) {
//alert( "The request is complete!" );
//}
});


function subFlipCrit(page, argId)
$.ajax({
	url: "/controller/flipcrit/" + page + "/" + argId,
	type: "GET",
	success: function( json ) {
		$('#datatable').bootstrapTable('refresh');
	},
	error: function( xhr, status, errorThrown ) {
		addAlert("Error flipping criticality of ID " + argId + ".", 'danger');
	},
});


function alertTimeout(wait){
    setTimeout(function(){
        $('#notification-area').children('.autoclose:first-child').fadeTo(500, 0).slideUp(500, function(){
            $(this).remove(); 
        });
    }, wait);
}


function addAlert(message, clas, autoclose) {
	if (autoclose == true) {
		clas = clas + " autoclose";
	} 
    $('#notification-area').append(
        '<div class="alert alert-dismissable infobox fade in alert-' + clas + '" role="alert">' +
            '<button type="button" class="close" data-dismiss="alert">' +
            '&times;</button>' + message + '</div>');
	if (autoclose == true) {
		alertTimeout(12000);
	} 
}



$(document).ready(function() {
	//x-editable settings
    $.fn.editable.defaults.mode = 'popup';    
    
    $('#dataform').editable({
    	selector: '.approve i',
    	url: '/controller/approve',
    	type: 'text',
    	emptytext: '',
    	
        ajaxOptions: {
        	success: function( json ) {
        		$('#datatable').bootstrapTable('refresh');
        	}
        }
    	
    });
    $('#dataform').editable({
    	selector: '.remove i',
    	url: '/controller/remove',
    	type: 'text',
    	emptytext: '',
    	
        ajaxOptions: {
        	success: function( json ) {
        		$('#datatable').bootstrapTable('refresh');
        	}
        }
    	
    });

    $('#learnmore').click(function() {
    	$('#learnmore').fadeOut('slow');
    	$('.moretolearn').fadeIn('slow');
		});
    
    $('#log').load('/log');
    
});

