from odoo import models,fields

class AccountMove(models.Model):
    _inherit = 'account.move' 
    
        
    
    def action_do_something(self):
        record = self.env['property'].browse(1)  # Get a specific record
        data = record.read(['name', 'postcode'])
        print(data)  # Print the data
        # print(data[0]['name'])
        # print(data[0]['postcode'])
         
         
         
        
        
        