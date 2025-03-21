from odoo import models, fields
class PropertyHistory(models.Model):
    _name = 'property.history'
    _description = 'Property History'

    user_id = fields.Many2one('res.users', string="User")
    property_id = fields.Many2one('property', string="Property")
    old_state = fields.Char(string="Old State")
    new_state = fields.Char(string="New State")
    reason = fields.Char(string="Reason")
    line_ids = fields.One2many('property.history.line', 'history_id')
    
    
    
    



# adding Lines         
class PropertyHistoryLine(models.Model):
    _name = "property.history.line"

    area = fields.Float(string="Area")
    description = fields.Text(string="Description")
    history_id = fields.Many2one("property.history", string="Property")
    