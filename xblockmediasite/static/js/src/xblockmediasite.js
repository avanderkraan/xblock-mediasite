/* Javascript for MediasiteXBlock. */
function MediasiteXBlock(runtime, element) {

    var handlerUrlMediasiteLink = runtime.handlerUrl(element, 'set_mediasite_url');
    var handlerUrlPresentationName = runtime.handlerUrl(element, 'set_presentation_name');
    var handlerUrlPresentationDescription = runtime.handlerUrl(element, 'set_presentation_description');
    var handlerUrlDuration = runtime.handlerUrl(element, 'duration');
    var handlerUrlPeriodFilter = runtime.handlerUrl(element, 'set_presentation_period_filter');
    var handlerUrlCourseCode = runtime.handlerUrl(element, 'get_course_code');
    
    function updateMediamissionLink(result) {
    	$('form[name="sendpreview"]', element).get(0).setAttribute('action', result.mediasite_preview_action_link);
     	$('[name="sendpreview"]', element).submit();
    }
    
    function updatePresentationName(result) {
    	// necessary to send data to the xblock python code
		//$('[name="presentation-options"]', element).html(result.presentation_options);
    }

    function updatePresentationDescription(result) {
    	// necessary to send data to the xblock python code
    }

    function updatePresentationTable(result) {
    	$('.warning', element).hide();
    	if (result.warning != '') {
    		$('.warning-message', element).html(result.warning);
    		$('.warning', element).show();
    		if (result.warning.indexOf('No result found') > -1) {
    			$('#presentation-selector', element).html('');    			
    	    	$('.save-button', element).hide();
    			$('.preview-button', element).hide();
    		}
    	}
    	$('#presentation-cells', element).html(result.presentation_cells);
    	//$('#course_code_input', element).val(result.course_code);
    	// trick to scroll table up   	

    	
    	$('#presentation-table-anchor', element).show();
        var focusElement = $('#presentation-table-anchor', element);
        if (focusElement != null) {
        	var listtop = $('.list-input', element).offset().top;
        	//var focustop = $(focusElement, element).offset().top;
            $('.list-input', element).animate({ scrollTop: listtop + 150}, 'slow');
        	focusElement.focus();
        }
    	$('#presentation-table-anchor', element).hide();

    }

    function updateDuration(result) {
    	// show save button if a presentation is selected and times are set
    	var presentationSelection = $('#presentation-selector', element).attr('selection-id');
		if ((presentationSelection) && (presentationSelection != result.def_presentation)) {
        	$('.preview-button', element).show();
        	$('.save-button', element).show();
		}
    }

    function updateMediamissionLinkNoPreview(result) {
    }
    
    function updatePeriodFilter(result) {
    	//$('[name="presentation-options"]', element).html(result.presentation_options);
    }

    //$('#presentation-selector', element).change(function(eventObject) {
    
    function presentationNoPreviewSelection(id, title) {
    	//var selected_presentation = $('#presentation-selector', element).val();
    	$('#presentation-selector', element).attr('selection-id', id).html('<label class="label setting-label">Your choice:</label><span>' + title + '</span>');

    	var selected_presentation = id;
    	$.ajax({
    		type: 'POST',
    		url: handlerUrlMediasiteLink,
    		data: JSON.stringify({'check': 'mediasite_url', 'presentation': selected_presentation}),
    		success: updateMediamissionLinkNoPreview
    	});
    };
    

    function refreshRuntimeClass() {
    	// listen to these events every time the code is generated
    	// within the code the class= is defined and will be only be available
    	// after a reload of these events

	    $(".select-presentation-id", element).off('click').on('click', function(eventObject) {
	    	//console.log($(this).parent());
	    	// clear background-color
	    	$(".select-presentation-id", element).removeClass('select-presentation-id-selected');
	    	$(this).addClass('select-presentation-id-selected');
	    	//alert($(this).attr('id'));
	    	id = $(this).attr('id');
	    	// show title nearby the preview button
	    	title = $(this).find('td.title').text();
	    	$('.preview-button', element).show();
	    	// show save button when a time is set
	    	if ($('#c-end-time', element).val() != '00:00:00') {	    		
	       		$('.save-button', element).show();
	    	}

	    	// scroll to button preview       	
        	var listHeight = $('.list-input', element)[0].scrollHeight;
        	$('.list-input', element).animate({scrollTop: listHeight + 150}, 'slow');
        	$('.preview-button', element).focus();
 
	    	// show the preview of the selected presentation
	    	presentationNoPreviewSelection(id, title);
	    });
    }

    /* start check oude tijd invoer
    function timesOk(starttime, endtime) {
		var starttimeArray = starttime.split(/\:/);
		var endtimeArray = endtime.split(/\:/);
		var startsec = parseInt(starttimeArray[0]) * 3600 + parseInt(starttimeArray[1]) * 60 + parseInt(starttimeArray[2]);
		var endsec = parseInt(endtimeArray[0]) * 3600 + parseInt(endtimeArray[1]) * 60 + parseInt(endtimeArray[2]);
		if (startsec <= endsec) {
			return true;
		}
		return false;
    }

    function isFormatTimeOk(time) {
    	var h = -1;
    	var m = -1;
    	var s = -1;
		var timeArray = time.split(':',3);
		if ($.isNumeric(timeArray[0])) {
			h = parseInt(timeArray[0]);
		}
		if ($.isNumeric(timeArray[1])) {
			m = parseInt(timeArray[1]);
		}
		if ($.isNumeric(timeArray[2])) {
			s = parseInt(timeArray[2]);
		}
		if ((h >= 0) && (h <=23) && (m >= 0) && (m <= 59) && (s >= 0) && (s <= 59)) {
			return true;
		}
		return false;
    }
    end check oude tijd invoer
    */ 

    // event handling
    $('.save-button', element).on('click', function() {
        var data = {'check': 'save'};
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        $.post(handlerUrl, JSON.stringify(data)).complete(function() {event
            window.location.reload(false);
        });
    });

    $('.cancel-button', element).on('click', function() {
        var data = {'check': 'cancel'};
        var handlerUrl = runtime.handlerUrl(element, 'studio_cancel');
        $.post(handlerUrl, JSON.stringify(data)).complete(function() {
            window.location.reload(false);
        });
    });    

    // start input fields
    $('input[name="presentation-name"]', element).on('keyup', function(eventObject) {
    	if (eventObject.keyCode == 13) {
    		$('input[name="presentation-description"]', element).focus();
    	}
    });

    $('input[name="presentation-name"]', element).on('blur', function(eventObject) {
    	var presentation_name = $('input[name="presentation-name"]', element).val()
        $.ajax({
            type: "POST",
            url: handlerUrlPresentationName,
            data: JSON.stringify({'check': 'presentation_name', 
            	                  'presentation_name': presentation_name
            	                  }),
            success: updatePresentationName
    	});
    });

    $('input[name="presentation-description"]', element).on('keyup', function(eventObject) {
    	if (eventObject.keyCode == 13) {
    		$('#course-code-input', element).focus();
    	}
    });

    $('input[name="presentation-description"]', element).on('blur', function(eventObject) {
    	var presentation_description = $('input[name="presentation-description"]', element).val()
        $.ajax({
            type: "POST",
            url: handlerUrlPresentationDescription,
            data: JSON.stringify({'check': 'presentation_description', 
            	                  'presentation_description': presentation_description
            	                  }),
            success: updatePresentationDescription
    	});
    });

    $('#search-course-code', element).on('click', function(eventObject) {
    	var course_code = $('#course-code-input', element).val();
    	var orderby = $('#ordered', element).attr('orderby');
    	var ordertype = $('#ordered', element).attr('ordertype');
        $.ajax({
            type: "POST",
            url: handlerUrlCourseCode,
            data: JSON.stringify({'check': 'course_code', 
            	                  'course_code': course_code,
            	                  'orderby': orderby,
            	                  'ordertype': ordertype
            	                  }),
            success: updatePresentationTable
    	});
    });

    $('#course-code-input', element).on('keyup', function(eventObject) {
    	if (eventObject.keyCode == 13) {
    		$('#search-course-code', element).click();
    	}
    });
    
    $('#search-course-code', element).ajaxStart(function() {
    	$('body').addClass('wait');
    });
    
    $('#search-course-code', element).ajaxStop(function() {
    	refreshRuntimeClass();
    	$('body').removeClass('wait');
    });
    // end input fields
    
    $('.preview-button', element).on('click', function(eventObject) {
    	var selected_presentation = $('#presentation-selector', element).attr('selection-id');
    	$.ajax({
    		type: 'POST',
    		url: handlerUrlMediasiteLink,
    		data: JSON.stringify({'check': 'mediasite_url', 'presentation': selected_presentation}),
    		success: updateMediamissionLink
    	});
    });
    
    $('.presentation-order-selector', element).on('click', function(eventObject) {
    	$('.presentation-order-selector', element).removeClass('fa-lg');
    	$(this).addClass('fa-lg');
    	$('#ordered').attr('orderby', $(this).attr('orderby'));
    	$('#ordered').attr('ordertype', $(this).attr('ordertype'));
    	$('#search-course-code', element).click();
    });        
   // end event handling
    
    (function ($) {
        /* Here's where you'd do things on page load. */
    	
   		$('.save-button', element).hide();
    	$('.preview-button', element).hide();
		$('.warning', element).hide();
    	// trick to scroll table up   	
		$('#presentation-table-anchor', element).hide();

		if ($('#c-start-time', element).val() == '') {
			$('#c-start-time', element).val('00:00:00');
	    };
	  
	    if ($('#c-end-time', element).val() == '') {
	    	$('#c-end-time', element).val('00:00:00');
	    };
	
	    // 'element' is missing on purpose, with 'element' an error occurs (but only on the newest edx)
	    // not sure though if this may cause conflict in other parts of the website
	    // Testing resulted in correct behaviour of the module
	    $('#c-start-time').datetimeEntry({initialField: 2, 
	                             datetimeFormat: 'H:M:S', 
	                             show24Hours: true, 
	                             showSeconds: true, 
	                             spinnerImage: ''
	                             //spinnerImage: element + '../images/spinnerUpDown.png',
	                             //spinnerBigImage: '/button/static/js/jquery.datetimeentry.package-2.0.0/spinnerUpDownBig.png',
	                             //spinnerSize: [15, 16, 0],
	                             //spinnerBigSize: [30, 32, 0],
	  	                         //spinnerIncDecOnly: true
	  	                         });
	
	    // 'element' is missing on purpose, with 'element' an error occurs (but only on the newest edx)
	    // not sure though if this may cause conflict in other parts of the website
	    // Testing resulted in correct behaviour of the module
	    $('#c-end-time').datetimeEntry({initialField: 2, 
	                             datetimeFormat: 'H:M:S', 
	                             show24Hours: true, 
	                             showSeconds: true, 
	                             spinnerImage: ''
	                             //spinnerImage: 'images/spinnerUpDown.png',
	                             //spinnerBigImage: '/button/static/js/jquery.datetimeentry.package-2.0.0/spinnerUpDownBig.png',
	                             //spinnerSize: [15, 16, 0],
	                             //spinnerBigSize: [30, 32, 0],
	  	                         //spinnerIncDecOnly: true
	  	                         });
	
	    
	    $('#c-start-time', element).change(function() {
	    	sString = '1970-01-01 ' + $('#c-start-time', element).val(); 
	    	eString = '1970-01-01 ' + $('#c-end-time', element).val(); 
	    	var s = Date.parse(sString, "yyyy-MM-dd HH:mm:ss");  	
	    	var e = Date.parse(eString, "yyyy-MM-dd HH:mm:ss");  	
	
	    	var difference = e - s;
	    	if (difference < 0) {
	    		$('#c-end-time', element).val($('#c-start-time', element).val());
	    	}
	    });
	    
	    $('#c-end-time', element).keyup(function(e) {
    		e.preventDefault();
	    	if (e.keyCode == 13) {
	    		$('#c-end-time', element).trigger('blur');
	    	}
	    });

	    $('#c-end-time', element).blur(function() {
	    	sString = '1970-01-01 ' + $('#c-start-time', element).val(); 
	    	eString = '1970-01-01 ' + $('#c-end-time', element).val(); 
	    	var s = Date.parse(sString, "yyyy-MM-dd HH:mm:ss");  	
	    	var e = Date.parse(eString, "yyyy-MM-dd HH:mm:ss");  	
	
	    	var difference = e - s;
	    	if (difference < 0) {
	    		$('.save-button', element).hide();
	    		alert('The end time comes before the start time, please enter another end time');
	    		$('#c-end-time', element).focus();
	    		//$('#c-start-time').val($('#c-end-time').val());
	    	}
	    	else {
	    		var starttime = $('#c-start-time', element).val();
	    		var endtime = $('#c-end-time', element).val();
		        $.ajax({
		            type: "POST",
		            url: handlerUrlDuration,
		            data: JSON.stringify({'check': 'duration', 
		            	                  'start-time': starttime,
		            	                  'end-time': endtime
		            	                  }),
		            success: updateDuration
		        });
	    	}
	    });

		
		//jQuery(function($){
			   // oude tijdinvoer met mask $("#c-start-time", element).mask("99:99:99");
			   // oude tijdinvoer met mask $("#c-end-time", element).mask("99:99:99");
		//});
    })(jQuery);
}
