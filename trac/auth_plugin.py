from trac.core import *
from trac.web.api import IAuthenticator

class ThyngAuthenticator(Component):

    implements(IAuthenticator)

    def authenticate(self, req):
        return req.get_header("X-Thyng-Remote-User")
