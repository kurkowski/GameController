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
         window.setInterval(function(){
		if (count < data.array.length){
			var display = $("#imageBox");
			var num = data.array[count];
			count++;
			display.attr('src', 'css/'+images[num]);
			display.attr('value', num);
			updateSequence(num);

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
   var buttonInSequence = images[$("#imageBox").attr('value')].charAt(0);
   var dataObject = {
      "button": letter,
      "sequence": buttonInSequence
   }
   $.ajax({
      type: 'POST',
      url: 'game/test/controls',
      data: dataObject,
      timeout: '10000',
      success: function(d)
      {
         console.log(d);
      },
      error: function(request, status, err) {
         console.log(request);
	 console.log(status);
         console.log(err);			
      } 
   });
}


