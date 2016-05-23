from Cookie import Cookie
from lxml.html import document_fromstring, tostring
import re
import urlparse

from http_proxy_cookielib import limit_cookie


_cookie_domain_re = re.compile(r'(domain="?)([a-z0-9._-]*)("?)', re.I)

def rewrite_links(request, response,
                  proxied_base, orig_base,
                  proxied_url):

    exact_proxied_base = proxied_base
    if not proxied_base.endswith('/'):
        proxied_base += '/'
    exact_orig_base = orig_base
    if not orig_base.endswith('/'):
        orig_base += '/'
    assert (proxied_url.startswith(proxied_base) 
            or proxied_url.split('?', 1)[0] == proxied_base[:-1]), (
        "Unexpected proxied_url %r, doesn't start with proxied_base %r"
        % (proxied_url, proxied_base))
    assert (request.url.startswith(orig_base) 
            or request.url.split('?', 1)[0] == orig_base[:-1]), (
        "Unexpected request.url %r, doesn't start with orig_base %r"
        % (request.url, orig_base))

    def link_repl_func(link):
        """Rewrites a link to point to this proxy"""
        if link == exact_proxied_base:
            return exact_orig_base
        if not link.startswith(proxied_base):
            # External link, so we don't rewrite it
            return link
        new = orig_base + link[len(proxied_base):]
        return new
    if response.content_type != 'text/html' or len(response.body) == 0:
        pass
    else:
        if not response.charset:
            ## FIXME: maybe we should guess the encoding?
            body = response.body
        else:
            body = response.unicode_body
        body_doc = document_fromstring(body, base_url=proxied_url)
        body_doc.make_links_absolute()
        body_doc.rewrite_links(link_repl_func)
        response.body = tostring(body_doc)

    if response.location:
        ## FIXME: if you give a proxy like
        ## http://openplans.org, and it redirects to
        ## http://www.openplans.org, it won't be rewritten and
        ## that can be confusing -- it *shouldn't* be
        ## rewritten, but some better log message is required
        loc = urlparse.urljoin(proxied_url, response.location)
        loc = link_repl_func(loc)
        response.location = loc
        
    if 'set-cookie' in response.headers:
        cookies = response.headers.getall('set-cookie')
        del response.headers['set-cookie']
        for cook in cookies:
            old_domain = urlparse.urlsplit(proxied_url)[1].lower()
            new_domain = request.host.split(':', 1)[0].lower()
            def rewrite_domain(match):
                """Rewrites domains to point to this proxy"""
                domain = match.group(2)
                if domain == old_domain:
                    ## FIXME: doesn't catch wildcards and the sort
                    return match.group(1) + new_domain + match.group(3)
                else:
                    return match.group(0)
            cook = _cookie_domain_re.sub(rewrite_domain, cook)
            
            _cook = Cookie(cook)
            assert len(_cook.keys()) == 1
            for key in _cook.keys():
                _morsel = _cook[key]
                if _morsel.get('path'):
                    _morsel['path'] = limit_cookie(
                        _morsel['path'],
                        urlparse.urlparse(exact_proxied_base).path,
                        urlparse.urlparse(exact_orig_base).path)
                cook = _morsel.OutputString()

            response.headers.add('set-cookie', cook)

    return response
