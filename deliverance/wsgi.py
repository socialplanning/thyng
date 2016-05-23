import lxml.html
from paste.httpserver import serve
import sys
from webob import Request
from wsgifilter import proxyapp

import rewritelinks


class ProxyApp(object):

    def __init__(self):
        self.proxies = {
            'thyng': proxyapp.ForcedProxy(remote="http://django:8000/",
                                          force_host=True),
            'trac': proxyapp.ForcedProxy(remote="http://trac:8001/",
                                         force_host=True)
        }


    def __call__(self, environ, start_response):
        req = Request(environ).copy()
        req.path_info = req.path_info.lstrip("/")
        resp = req.get_response(self.proxies['thyng'])

        if resp.status_code != 305:
            return resp(environ, start_response)

        subreq = Request(dict(environ)).copy()
        container = resp.headers['X-Thyng-Container-Url'].lstrip("/")
        featurelet = resp.headers['X-Thyng-Featurelet-Slug'].lstrip("/")
        instance = resp.headers['X-Thyng-Featurelet-Instance'].rstrip("/")
        theme = resp.body
        
        path_info = (
            instance + "/" +
            resp.headers['X-Thyng-Path-Info'].lstrip("/")).lstrip("/")
        subreq.path_info = path_info
        proxy = resp.headers['Location']
        resp = subreq.get_response(self.proxies[proxy])
        resp = rewritelinks.rewrite_links(resp,
            'http://trac:8001/' + instance,
            'http://192.168.99.101/' + container.strip('/') + '/' + featurelet,
            'http://trac:8001/' + subreq.path_info)

        if resp.content_type != "text/html":
            return resp(environ, start_response)

        content = lxml.html.fromstring(resp.body)
        theme = lxml.html.fromstring(theme)
        head = theme.cssselect("head")[0]
        for child in reversed(content.cssselect("head")[0].getchildren()):
            head.insert(0, child)
        div = theme.cssselect("#main")[0]
        div.text = ''
        for child in content.cssselect("#main")[0].getchildren():
            div.append(child)
        resp.body = lxml.html.tostring(theme)

        return resp(environ, start_response)


if __name__ == '__main__':
    serve(ProxyApp(), host='0.0.0.0', port=sys.argv[-1])
