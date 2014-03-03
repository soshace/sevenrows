$(document).ready(function(){
	$('#login-trigger').click(function(){
		$(this).next('#login-content').slideToggle();
		$(this).toggleClass('active');					
		
		if ($(this).hasClass('active'))
			$(this).find('span').html('&#x25B2;')
		else
			$(this).find('span').html('&#x25BC;')
		});
	$("#id_login_submit").click(function(){
            console.log('start_login');
                    $.ajax({
                            url: "/ajax/login/",
                            type: "POST",
                            data: {
                                email: $("#id_login_email").val(),
                                password: $("#id_login_password").val(),
                                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                            },
                            cache: false,
                            success: function(response){
                                if (response == 'OK'){
                                    //редирект при удачном логине
                                    alert(response);
                                    document.location.href = '/my/';
                                } else {
                                    $("#info_label_login").text("Incorrect email or password");
                                }
                            }
                    });
        });

    $("#id_reg_submit").click(function(){
        console.log('start_sign_up');
        var email = $("#id_reg_email").val();
        var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
        console.log('Registration email: ', email, ', csrf: ', csrfmiddlewaretoken);
                    $.ajax({
                            url: "/ajax/reg/",
                            type: "POST",
                            data: {
                                email: email,
                                csrfmiddlewaretoken: csrfmiddlewaretoken
                            },
                            cache: false,
                            success: function(response){
                                if (response == 'OK'){
                                    alert(response);
                                    document.location.href = '/my/';
                                } else {
                                    $("#info_label_login").text(response);
                                }
                            }
                    });
        });
});