$(document).ready(function () {
    $("#draggable").animate({
        opacity: 0.5,
    }, 500, function () {

    });

    $('#id_button_order_cards').click(function () {
        var str = $('#order_card_form').serialize();

        $.post('/cards/',
              str,
              function (data) {
                  alert('saved')
              });
    });

    /*
    var frm = $('#order_card_form');
    frm.submit(function () {
        $.ajax({
            type: frm.attr('POST'),
            url: frm.attr('/cards/'),
            data: frm.serialize(),
            success: function (data) {
                alert('saved')
            },
            error: function (data) {
                alert('saved')
            }
        });
    });
    */
});