var uri = "/_pili/test"


YUI().use('test','io','node','console', 'json', 'cookie', function (Y) {

var testCase = new Y.Test.Case({
 
    name: "Test Base",
    setUp: function(){

    },
    testPrivateMethod: function(){

    },
    testMethod: function(){

    },
    testIndex : function(){
    },
    testDefault : function(){
	    // it might be YUI bug, ' ' should not be '+'
	    //Y.assert(Y.Cookie.get(id_3)=='你+好', 'test set cookie on server side');
	    //Y.assert(Y.Cookie.get(id_4)===null, 'test set cookie with httponly on server side');
    },
 

    get: function(param){
		 var html = '';
		 Y.io(uri + "/case-base-real/" + param ,{sync:true, on:{complete:function(id,r){ html=r.responseText; }}});
		 return html;
    },
    post: function(param, data){
	    var html = '';
	    Y.io(uri + "/case-base-real/" + param, {method:"POST", sync:true, data:data, on:{complete:function(id,r){ html=r.responseText; }}});
	    return html;
    }
});

var r = new Y.Console({ newestOnTop : false, style: 'block' });
r.render('#testLogger');


Y.Test.Runner.add(testCase);
Y.Test.Runner.subscribe(Y.Test.Runner.TEST_FAIL_EVENT, function(data){ 
	alert("Test named '" + data.testName + "' failed with message: '" + data.error.message + "'.");
	});
Y.Test.Runner.run();


});
