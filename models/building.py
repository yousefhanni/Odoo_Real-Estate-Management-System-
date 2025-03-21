from odoo import models, fields

class Building(models.Model):
    _name = 'building'
    _description = 'Building Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _rec_name = 'code'

    no = fields.Integer(string="Number")
    code = fields.Char(string="Code")
    description = fields.Text(string="Description")
    
    # if has name field not needed to define _rec_name
    name=fields.Char(required=1,default='New Building')
    # Archiving => active field is used to archive the record instead of deleting it.  
    active=fields.Boolean(default=True) 
   
# Reserved Fields Names:
# - name
# - active

