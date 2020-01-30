from odoo import http
import xmlrpc.client


class BaseController(http.Controller):
    url = "http://localhost:8070"
    db = "odoo"
    username = "admin"
    password = "admin"
    common = None
    uid = None
    models = None

    def get_conexion(self):
        self.common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        self.uid = self.common.authenticate(self.db, self.username, self.password, {})
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        return self.models
