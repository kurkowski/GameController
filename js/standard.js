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


