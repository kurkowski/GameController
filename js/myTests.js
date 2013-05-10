function isEven(val) {  
    return val % 2 === 0;  
}  
test('isEven() making sure qunit is working', function() { 
    ok(isEven(0), 'Zero is an even number'); 
    ok(isEven(2), 'So is two'); 
    ok(isEven(-4), 'So is negative four'); 
    ok(!isEven(1), 'One is not an even number'); 
    ok(!isEven(-7), 'Neither is negative seven');  
})

asyncTest('getSequence()',1, function(){
    getSequence(function(result){
        var data = JSON.parse(result);
	ok( data.array.length, 200, "array is at least length 200");
	setTimeout(function(){
	     start();
	}, 1000);
    });
})

test('hideImage()', function(){
    var display = hideImage();
    equal(display, 'none', "display is none");
})

asyncTest('updateSequence', function(){
    updateSequence('4', function(data){
	var retval = JSON.parse(data);
	equal(retval.sequence, 4, "current sequence num in server is 4");
    	setTimeout(function(){
		start();
   	}, 1000);		    
    });
})

asyncTest('sendButtonPress() correct', function(){
	updateSequence('4');
	setTimeout(function(){
	    sendButtonPress('r', function(data){
    	        var retval = JSON.parse(data);
	        equal(retval.stat, "true");
                setTimeout(function(){
	            start();
	        }, 1000);	
	    })
	}, 1000);
})

asyncTest('sendButtonPress() wrong', function(){
	updateSequence('4');
	setTimeout(function(){
	    sendButtonPress('u', function(data){
    	        var retval = JSON.parse(data);
	        equal(retval.stat, "false");
                setTimeout(function(){
	            start();
	        }, 1000);	
	    })
	}, 1000);
})
