$(document).ready(function(){
	$('#changeBackground').click(function(){
		$('body').css('background-image', 'url(/static/images/isaak.jpg)')
		});

	$.ajax({
                            url: "/ajax/get_label_coords/",
                            type: "POST",
                            data: {
                                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                            },
                            cache: false,
                            success: function(response){
                                if (response){
                                    //редирект при удачном логине
                                    $( "#draggable" ).offset({ top: response.y, left: response.x });
                                    //alert('SET');
                                } else {
                                    alert('NO');
                                }
                            }
            });

	$( "#draggable" ).animate({
		opacity: 0.5,
		}, 500, function() {
    		
	});

	$('#draggable').draggable({
        stop: function(event, ui) {
            console.log($(this).offset().left);
            console.log($(this).offset().top);
        	console.log($('input[name="csrfmiddlewaretoken"]').val());
        	$.ajax({
                            url: "/ajax/set_label_coords/",
                            type: "POST",
                            data: {
                                x: $(this).offset().left,
                                y: $(this).offset().top,
                                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                            },
                            cache: false,
                            success: function(response){
                                if (response == 'OK'){
                                    //редирект при удачном логине
                                    //alert('SAVED');
                                } else {
                                    alert(response)
                                }
                            }
                    });
            //alert('Left:' + $(this).offset().left + ' Top:' + $(this).offset().top);
        }
    }).resizable({
        stop: function(event,ui){}
    });
});