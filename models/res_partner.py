from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner' 

    property_ids = fields.Many2one('property', string='Property')
    price = fields.Float(compute="_calc_price")

    @api.depends('property_ids')  
    def _calc_price(self):
        for prop in self:
            if prop.property_ids:
                prop.price = prop.property_ids.selling_price
            else:
                prop.price = 0  
