from odoo import models, fields

class SampleHello(models.Model):
    _name = 'sample.hello'
    _description = 'Sample Hello Model'

    name = fields.Char(string='Name', required=True)