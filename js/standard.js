var count=0;
var images = ['abutton.png', 'bbutton.png', 'downarrow.png', 'leftarrow.png', 'rightarrow.png', 'uparrow.png'];

function getSequence(){
      $.ajax({
      type: 'GET',
      url: 'game/test/sequence',
      timeout: '10000',
      success: function(d)
      {
	 var data = JSON.parse(d);	 

	 var display = $("#imageBox");
	 var num = data.array[count];
	 count++;
 	 display.attr('src', 'css/'+images[num]);
	 display.attr('value', num);
	 updateSequence(num);
	 window.setTimeout(hideImage, 1500);	 
         window.setInterval(function(){
		if (count < data.array.length){
			var display = $("#imageBox");
			display.css('display', 'block');
			var num = data.array[count];
			count++;
			display.attr('src', 'css/'+images[num]);
			display.attr('value', num);
			updateSequence(num);
			window.setTimeout(hideImage, 1500);
		}
	}, 2000);
      },
      error: function(request, status, err) {
         console.log(request);
	 console.log(status);
         console.log(err);			
      } 
      });
}

function hideImage(){
	var image = $("#imageBox");
	image.css('display', 'none');
}

function updateSequence(num){
	 var dataObject = {
		"num": num
	 };

	 $.ajax({
      		type: 'GET',
      		url: 'game/test/update',
      		timeout: '10000',
	 	data: dataObject,
	 	success: function(data){
			
		},
	 	error: function(request, status, err) {
         		console.log(request);
	 		console.log(status);
         		console.log(err);			
      		} 
	 });
}

var balloonSize = 0;

function sendButtonPress(letter){
   var dataObject = {
      "button": letter
   }
   $.ajax({
      type: 'POST',
      url: 'room/play/controls',
      data: dataObject,
      timeout: '10000',
      success: function(d)
      {
         var jsonObj = JSON.parse(d);
	 console.log(jsonObj);
	 if (jsonObj.stat == "true" && balloonSize < 9){
		balloonSize++;
		updateBalloon();
	 } 
	 else if (jsonObj.stat == "false" && balloonSize > 0){
		balloonSize--;
		updateBalloon();
	 }
      },
      error: function(request, status, err) {
         console.log(request);
	 console.log(status);
         console.log(err);			
      } 
   });
}

function updateBalloon(){
	var bal = $('#imageBalloon');
	bal.attr('src', 'css/balloon'+balloonSize+'.png');
}

function onOpened() {
	console.log("opened");
};

function onMessage(data) {
	console.log("received msg");
	var message = JSON.parse(data.data).message;
	var letter = JSON.parse(data.data).button;
	if (message == 'monitor')
	{
		document.location.href = '/room/play/monitor';
	}
	if (message == 'controller')
	{
		document.location.href = '/room/play/controller';
	}
	if (button)
	{
		$('#letter').append(letter);
	}

}
