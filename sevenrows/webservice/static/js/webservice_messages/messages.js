$(document).ready(function () {
    $("#draggable").animate({
        opacity: 0.5,
    }, 500, function () {
    });

    $('#link_to_messages').click(function () {
        friend = $(this).attr('title');
        $("#chat_div").load('/messages/' + friend);
        $('#send_message_form_div').css("display", "block");
    });

    $( "#send_message_button").click(function () {
        console.log(friend);

        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        var text = $("#id_messages_toFriend_text").val();
        console.log(text);
        console.log(csrf);

        $.ajax({
            url: "/messages/" + friend + "/",
            type: "POST",
            data: {
                text: text,
                csrfmiddlewaretoken: csrf
            },
            cache: false,
            success: function (response) {
                if (response != 'NO') {
                    //редирект при удачном логине
                    $("#chat_div").load('/messages/' + friend);
                } else {
                    alert('smth wrong');
                }
            }
        });
    });
});