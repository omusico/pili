print " Content-Type: text/html; charset=utf-8"
print ""
print """
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
<script type="text/javascript" src="http://yui.yahooapis.com/combo?3.3.0/build/yui/yui-min.js&3.3.0/build/loader/loader-min.js"></script>
</head>
<body class="yui3-skin-sam  yui-skin-sam">
<h1>Test pili.lite in real case</h1>
<div id="testLogger"></div>
<script type='text/javascript'>
%s
</script>
</body>
</html>
""" % open("lite_real.js").read()
