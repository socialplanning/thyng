import lxml.html
from paste.httpserver import serve
import sys
from webob import Request
from wsgifilter import proxyapp

import rewritelinks


class ProxyApp(object):

    def __init__(self, proxy_config, frontend_host):
        self.proxies = {}
        for key in proxy_config:
            self.proxies[key] = {
                "app": proxyapp.ForcedProxy(
                    remote=proxy_config[key], force_host=True),
                "host": proxy_config[key],
            }
        assert 'thyng' in self.proxies
        self.frontend_host = frontend_host

    def __call__(self, environ, start_response):
        req = Request(environ).copy()
        req.path_info = req.path_info.lstrip("/")
        resp = req.get_response(self.proxies['thyng']['app'])

        if resp.status_code != 305:
            return resp(environ, start_response)

        subreq = Request(dict(environ)).copy()
        if 'X-Thyng-Remote-User' in resp.headers:
            subreq.headers['X-Thyng-Remote-User'] = resp.headers['X-Thyng-Remote-User']
        container = resp.headers['X-Thyng-Container-Url'].lstrip("/")
        featurelet = resp.headers['X-Thyng-Featurelet-Slug'].lstrip("/")
        instance = resp.headers['X-Thyng-Featurelet-Instance'].rstrip("/")
        theme = resp.body
        
        path_info = (
            instance + "/" +
            resp.headers['X-Thyng-Path-Info'].lstrip("/")).lstrip("/")
        subreq.path_info = path_info
        proxy = resp.headers['Location']
        resp = subreq.get_response(self.proxies[proxy]['app'])
        resp = rewritelinks.rewrite_links(resp,
            self.proxies[proxy]['host'] + instance,
            self.frontend_host + container.strip('/') + '/' + featurelet,
            self.proxies[proxy]['host'] + subreq.path_info)

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
    app = ProxyApp(
        {"thyng": "http://localhost:8000/", "trac": "http://localhost:8001/"},
        "http://localhost:8002/",
    )
    serve(app, host='0.0.0.0', port=sys.argv[-1])
