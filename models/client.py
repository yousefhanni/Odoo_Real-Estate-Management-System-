from odoo import models,fields

#Prototype Inheritance => 
class Client(models.Model):
    _name = 'client'
    _inherit = 'owner'



