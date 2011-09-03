# -*- coding: utf-8 -*-
from pili import lite

def main():
    lite.init(globals())

    if _ENV['QUERY_STRING'] == '':
        return testEcho()

    if _GET['testCookie'] is not None:
        return testCookie()
    
    if _GET['testSetCookie'] is not None:
        return testSetCookie()

    if _GET['testPost'] is not None:
        return testPOST()

    if _GET['testPosts'] is not None:
        return testPOSTS()

    if _GET['testGet'] is not None:
        return testGET()
    
    if _GET['testGets'] is not None:
        return testGETS()

def testSetCookie():
    key = _GET['testSetCookie']
    value = _GET['value']
    _type = _GET['type']
    #setcookie('testmultiple','cookie', path='/')
    if _type == 'httponly':
        setcookie(key, value, path='/', httponly=True)
    else: #session
        setcookie(key, value, path='/')
    flush()

def testCookie():
    key = _GET['testCookie']
    echo(_COOKIE[key])

def testPOST():
    key = _GET['testPost']
    echo(_POST[key])

def testPOSTS():
    key = _GET['testPosts']
    # join the list, or it will return weird string in chinese
    echo("##".join(_POSTS[key]))

def testGETS():
    key = _GET['testGets']
    echo(_GETS[key])

def testGET():
    key = _GET['testGet']
    echo(_GET[key])

def testEcho():

    echo("hello")
    echo(" ", "world")
    
    echo("##");

    echo("你好",u"嗎？")

    echo("##");

    echo({'key':'value'})

    echo("##");

    echo(None)

    echo("##");

    ob_start();
    echo("a@b")
    content = ob_get_clean()
    echo(content.replace("@", "$"))

    echo("##");
    ob_start()
    echo("a@@b", u"a@@@b", 12345)
    echo(ob_get_clean().replace("@", "$"))

if __name__ == '__main__': main()
