from jinja2 import environmentfilter, Markup, escape, evalcontextfilter

"""
@evalcontextfilter
def hl_url(eval_ctx, url):
    import web
    hl=web.input(hl="").hl
    if hl=="":
        result=url
    else:
        if url.find("?")!=-1:
            url_path, url_query =url.split("?", 2)
            url_queries=url_query.split("&")
            has_hl=False
            
            for query in url_queries:
                if query.split("=", 2)[0]=="hl":
                    query="hl=" + hl
                    has_hl=True
                    
            if has_hl==False:
                url_queries.append("hl=" + hl)
            result= url_path + "?" + "&".join(url_queries)
        else:
            result=url + "?hl=" + hl
    #result=url + "&hl="
    if eval_ctx.autoescape:
        result = Markup(result)
    return result
"""

"""
def pathname2url(value):
    value=value.encode('utf-8')
    import urllib
    return urllib.pathname2url(value)
"""

def linebreaks(value):
    return value.replace("\r\n","\n").replace("\r","\n").replace("\n","<br/>")

def urlencode(s):
    s=s.encode('utf-8')
    from urllib import urlencode
    s=urlencode({'v':s})
    return s[2:]

