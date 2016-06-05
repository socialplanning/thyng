import re

from trac.core import *
from trac.perm import PermissionSystem, IPermissionRequestor
from trac.ticket import model
from trac.web import IRequestHandler


class ComponentModule(Component):

    implements(IRequestHandler)

    # IRequestHandler methods
    
    def match_request(self, req):
        if req.path_info.startswith("/thyng_api/"):
            return True
        
    def process_request(self, req):
        user = req.args.get('user')
        group = req.args.get("group")
        
        perm = PermissionSystem(self.env)
        perm.grant_permission(user, group)
        req.write("ok")
