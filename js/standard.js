
function sendButtonPress(letter){
   var dataObject = {
      "button": letter
   }
   $.ajax({
      type: 'POST',
      url: 'something',
      data: dataObject,
      timeout: '10000',
      success: function(d)
      {
         console.log('success'); 
      },
      error: function(request, status, err) {
         console.log(request);
	 console.log(status);
         console.log(err);			
      } 
   });
}
