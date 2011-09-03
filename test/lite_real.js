var uri = "/_pili/test"


YUI().use('test','io','node','console', 'json', 'cookie', function (Y) {

var testCase = new Y.Test.Case({
 
    name: "TestCase Name",
    setUp: function(){
    },

    testCookie : function(){
	    var id_base = 'c' + parseInt((new Date()).getTime()/1000);
	    var id_1 = id_base + '1';
	    var id_2 = id_base + '2';
	    var id_3 = id_base + '3';
	    var id_4 = id_base + '4';

	    // test get cookie
	    Y.Cookie.set(id_1, "value with white space", { expires: new Date((new Date()).getTime()+5*60*1000), path:'/' });
	    Y.Cookie.set(id_2, "你 好", { expires: new Date((new Date()).getTime()+5*60*1000), path:'/' });
	    //alert(this.get('testCookie='+id_2));
	    Y.assert(this.get('testCookie='+id_1) == 'value with white space', 'test cookie with white space');
	    Y.assert(this.get('testCookie='+id_2) == '你 好', 'test cookie with white space');


	    this.get('testSetCookie='+id_3 + '&value=' + encodeURIComponent("你 好"));
	    this.get('testSetCookie='+id_4 + '&type=httponly&&value=' + encodeURIComponent("你 好 嗎？"));
	    // it might be YUI bug, ' ' should not be '+'
	    Y.assert(Y.Cookie.get(id_3)=='你+好', 'test set cookie on server side');
	    Y.assert(Y.Cookie.get(id_4)===null, 'test set cookie with httponly on server side');

    },
 
    testEcho : function () {
	var methods = new Array('GET', 'POST');
	for(var i in methods){
		Y.log("test:" + methods[i]);
		var actual = "";
		Y.io(uri + "/case-lite-real/", 
			{
			method: methods[i],
			sync:true,on:{
				complete:function(id,r){
				actual = r.responseText;
				}
				}
			}
		);
		var r = actual.split("##");
		Y.assert(r[0]=='hello world', "multiple args in echo");
		Y.assert(r[1]=='你好嗎？', "Chinese test");
		Y.assert(r[2]=="{'key': 'value'}", "dict type test error");
		Y.assert(r[3]=='None', "None type test error");
		Y.assert(r[4]=='a$b', "ob test error");
		Y.assert(r[5]=='a$$ba$$$b12345', 'ob second test error');
	}
    },

    get: function(qs){
		 var html = '';
		 Y.io(uri + "/case-lite-real/?" + qs ,{sync:true, on:{complete:function(id,r){ html=r.responseText; }}});
		 return html;
    },

    post: function(param, data){
	    var html = '';
	    Y.io(uri + "/case-lite-real/?" + param, {method:"POST", sync:true, data:data, on:{complete:function(id,r){ html=r.responseText; }}});
	    return html;
    },
    testPOSTS: function(){
	    Y.assert(this.post("testPosts=a","a=1&b=2")=="1", 'test single POSTs');
	    Y.assert(this.post("testPosts=a","a=1&a=2")=="1##2", 'test multiple POSTs');
	    Y.assert(this.post("testPosts=a","a=" + encodeURIComponent("你好")+ "&a=2")==
	    	'你好##2', "test multiple param with Chinese");
	    Y.assert(this.post("testGet=a&a=123", "a=456")=='123', 'test get should prior than post');
    },

    testPOST: function(){
	    Y.assert(this.post("testPost=a","a=1&b=2")=='1', 'test POST');
	    Y.assert(this.post("testPost=a","a=&b=2")=='None', 'default value should be None in POST');
	    Y.assert(this.post("testPost=a","a="+encodeURIComponent("你好嗎？")+"&b=2")=='你好嗎？', 'double byte in POST');
	    Y.assert(this.post("testPost=a357","a357="+encodeURIComponent("許功蓋")+"&a357=2")=='許功蓋', 'double byte and in POST, it should get first argument');
    },
 
    testGET : function () {
		Y.assert(this.get("testGet=a&a=1234+5")=="1234 5", "+ in GET");
		Y.assert(this.get("testGet=a&a=a=b")=="a=b", "= in GET");
		Y.assert(this.get("testGet=a&&a=%E8%A8%B1%E5%8A%9F%E8%93%8B")=="許功蓋", "double byte in GET");
		Y.assert(this.get("testGet=a&&a=%20")==" ", "empty result in GET");
		Y.assert(this.get("testGet=a_b&&a_b=Hello World")=="Hello World", "empty result in GET");
		Y.assert(this.get("testGet=a_b&&a_b=")=="", "key name test");
		Y.assert(this.get("testGet=a_b&&no_result=")=="None", "no result");
		Y.assert(this.get("testGet=a&a=1&a=2&a=3")=='1', "should get first result");
    },
    testGETS: function(){
	Y.assert(this.get("testGets=a&a=1")=="['1']", '1 gets');
	Y.assert(this.get("testGets=a&a=")=="['']", 'empty gets');
	Y.assert(this.get("testGets=a")=="[]", "no result in gets");
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
