$(document).ready(function(){
	//popover for vk & twitter
	$('#vk_facebook_twitter').popover({animation:true, placement:'right', trigger:'click', content:"Скоро будет ;)"});
	//registration and description fileds must have equal heights
	var regHeight = $('#registrationField').height();
	$('#rightField').height(regHeight);
	var neededMarginHeigh = regHeight - ($('#descriptionField').height() + $('#qrField').height());
	//$('#qrField').css("margin-top", neededMarginHeigh);
	//$('#qrImage').animate({ boxShadow : "0 0 0 15px #0099CC" });
	$('#qrImage').hover(function() {
 			$('#qrImage').css("box-shadow", "0 0 15px #0099CC");
 		},function(){
 			$('#qrImage').css("box-shadow", "");
 	});
 	$('#qrImage').click(function() {
 		$('#popup').bPopup({
            content:'iframe', //'ajax', 'iframe' or 'image'
            contentContainer:'.content',
            loadUrl:'http://dinbror.dk/search' //Uses jQuery.load()
        });
 	});
});