from odoo import models, fields


#Delegation Inheritance=> Reuses parent fields dynamically with access , 
class Employee(models.Model):
    _name = 'custom.employee'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    employee_code = fields.Char(string="Employee Code")