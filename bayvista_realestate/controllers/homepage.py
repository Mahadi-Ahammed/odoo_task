# -*- coding: utf-8 -*-
##############################################################################
# #

from odoo import http
from odoo.http import request


class BayVistaHome(http.Controller):
    @http.route('/', auth='public', type='http', website=True, sitemap=False)
    def root(self, **kw):
        return request.redirect('/bay_vista_home')
