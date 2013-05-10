var count=0;
var images = ['abutton.png', 'bbutton.png', 'downarrow.png', 'leftarrow.png', 'rightarrow.png', 'uparrow.png', 'shakeit.png'];

function getSequence(donefunc){
      var post = $.ajax({
      type: 'GET',
      url: 'game/test/sequence',
      timeout: '10000',
      });

      post.done(function(d){
          if(donefunc){
               donefunc(d);
	  }
	  else{
               getSequenceSuccess(d);
	  }
      });

      post.fail(function(request, status, err) {
         console.log(request);
	 console.log(status);
         console.log(err);			
      });
}

function getSequenceSuccess(d)
{
	 var data = JSON.parse(d);	 

	 var display = $("#imageBox");
	 var num = data.array[count];
	 count++;
 	 display.attr('src', 'css/'+images[num]);
	 display.attr('value', num);
	 display.css('display', 'block');
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
}

function hideImage(){
	var image = $("#imageBox");
	image.css('display', 'none');
	return image.css('display');
}

function updateSequence(num, funcdone){
	 lastPressed = null;
	 var dataObject = {
		"num": num
	 };

	 $.ajax({
      		type: 'GET',
      		url: 'game/test/update',
      		timeout: '10000',
	 	data: dataObject,
	 	success: function(data){
			if(funcdone){
				funcdone(data);
			}
		},
	 	error: function(request, status, err) {
         		console.log(request);
	 		console.log(status);
         		console.log(err);			
      		} 
	 });
}

var balloonSize = 0;
var lastPressed =null;

function sendButtonPress(letter, funcdone){
   var dataObject = {
      "button": letter
   }
   if (letter != lastPressed){
      $.ajax({
         type: 'POST',
         url: 'game/test/controls',
         data: dataObject,
         timeout: '10000',
         success: function(d)
         {
            if (funcdone){
		funcdone(d);
	    }
	    else{
               var jsonObj = JSON.parse(d);
	       if (jsonObj.stat == "true" && balloonSize < 9){
	   	      balloonSize++;
		      updateBalloon();
	       } 
	       else if (jsonObj.stat == "false" && balloonSize > 0){
		      balloonSize--;
	   	      updateBalloon();
	       }
      	       lastPressed = letter;
	    }
         },
         error: function(request, status, err) {
            console.log(request);
	    console.log(status);
            console.log(err);			
         } 
      });
   }
}

function updateBalloon(){
	var bal = $('#imageBalloon');
	bal.attr('src', 'css/balloon'+balloonSize+'.png');
	if (balloonSize == 9){
		alert("you win");
	}
}

function win(){
	$.ajax({
		type: 'POST',
		url: '',
		timeout: '10000',
		success: function(d){
			alert("You won");
		},
		error: function(request, status, err){
			console.log(request);
			console.log(status);
			console.log(err);
		}
	});
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

/**
 * code borrowed from https://developer.mozilla.org/en-US/docs/DOM/Mozilla_event_reference/devicemotion
 */
function handleMotionEvent(event) {
 
    var x = event.accelerationIncludingGravity.x;
    var y = event.accelerationIncludingGravity.y;
    var z = event.accelerationIncludingGravity.z;
 
    if (x > 1.0 && y > 1.0 && z > 1.0){
	sendButtonPress('s');
    }
}
 
window.addEventListener("devicemotion", handleMotionEvent, true);

