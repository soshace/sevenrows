$(document).ready(function () {
    $("#userDataChange").click(function () {
        console.log('start_change_user_data');

        jQuery(".userDataDiv").fadeIn('normal');
        jQuery(".userDataDiv").css('display', 'none');
        jQuery(".userDataForms").css('display', 'block');

    });

    $("#id_change_all_button").click(function () {
        var username =          $("#id_account_username").val();
        var first_name =        $("#id_account_first_name").val();
        var second_name =       $("#id_account_second_name").val();
        var eye_color =         $("#id_account_eye_color").val();
        var birthday =          $("#id_account_date_of_birth").val();
        var growth =            $("#id_account_growth").val();
        var about =             $("#id_account_about").val();
        var personal_field =    $("#id_account_personal_field").val();
        var csrf =              $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: "/ajax/account/change_all/",
            type: "POST",
            data: {
                username:           username,
                first_name:         first_name,
                second_name:        second_name,
                eye_color:          eye_color,
                date_of_birth:      birthday,
                growth:             growth,
                about:              about,
                personal_field:     personal_field,
                csrfmiddlewaretoken: csrf
            },
            cache: false,
            success: function(response){
                if (response == 'OK'){
                    //редирект при удачном логине
                    alert(response);
                } else {
                    alert(response)
                }
            }
        });
        
    });
});