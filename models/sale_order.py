from odoo import models,fields

class SaleOrder(models.Model):
    _inherit = 'sale.order' 
    
        
    property_id = fields.Many2one('property', string='Property')
    
   
# python inheritance(overriding) and type of inheritance model=> Classical Inheritance 
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        print("action_confirm")
        return res    
    
     
    
    

    
    