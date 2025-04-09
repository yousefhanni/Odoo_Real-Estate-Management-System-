from odoo import models,fields,api
from odoo.exceptions import ValidationError
from datetime import timedelta 
import requests  

class Property(models.Model):
    _name = 'property'    
    _description = 'Property'
    _inherit=['mail.thread','mail.activity.mixin']
    # name=fields.Char(required=1) Client-Side (UI)
    ref=fields.Char(readonly=True,default='New')
    name=fields.Char(required=True,default='New',translate=True)
    description =fields.Text(tracking=True)
    postcode =fields.Char(required=True)
    date_availability =fields.Date(tracking=True)
    expected_selling_date=fields.Date(tracking=True)
    is_late=fields.Boolean()
    expected_price =fields.Float(digits=(0,5))
    selling_price=fields.Float()
    bedrooms =fields.Integer()
    living_area=fields.Integer()
    facades  = fields.Integer() 
    garage   = fields.Boolean(groups="app_one.property_manager_group")
    garden   = fields.Boolean()
    garden_area  = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'Southa'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string='Garden Orientation',
        default='north'          
    )
    
    state=fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
        
    ],default='draft')
    
    owner_id = fields.Many2one('owner',string='Owner')
    
    difference_price=fields.Float(compute="_calc_difference")
    #related field =>By default not represent in database, but if you want to store it in database you can add store=True same computed field
    owner_phone=fields.Char(related="owner_id.phone",readonly=False)
    owner_address=fields.Char(related="owner_id.address",readonly=False)
    #Database Level 
    _sql_constraints = [('unique_name', 'unique(name)', 'Name must be unique!')]
     
    line_ids = fields.One2many('property.line', 'property_id')
    
    active=fields.Boolean(default=True) 
    
    create_time=fields.Datetime(default=fields.Datetime.now()) 
    next_create_time=fields.Datetime(compute="_compute_next_time") 
    @api.depends("expected_price","selling_price","owner_id.phone")
    def _calc_difference(self):
        for prop in self:
            # print("inside _calc_difference")
            prop.difference_price =prop.expected_price-prop.selling_price
    
    @api.depends('create_time')
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_create_time=rec.create_time+timedelta(hours=6)         
            else:
                rec.next_create_time=False
                 
            
    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        if self.expected_price > 1000000:
            self.garden_area = 500
            return {
                'warning': {
                    'title': "High Expected Price!",
                    'message': "The expected price is very high. The garden area has been set to 500.",
                    'type': 'warning',
                }
            }
            
         
    #Python-Level Validation(Logic)
    @api.constrains('name', 'postcode', 'bedrooms')
    def _check_required_fields(self):
        for record in self:
            if not record.name or not record.name.strip():
                raise ValidationError("The 'Name' field is required and cannot be empty.")
            if not record.postcode or not record.postcode.strip():
                raise ValidationError("The 'Postcode' field is required and cannot be empty.")
            if record.bedrooms is None or record.bedrooms <= 0:
                raise ValidationError("The 'Bedrooms' field must be greater than 0.")
    
    def change_state(self):
        for rec in self:
            old_state = rec.state  # Get the current state before changing
            if rec.state == 'draft':
                new_state = 'pending'
            elif rec.state == 'pending':
                new_state = 'sold'
            elif rec.state == 'sold':
                new_state = 'draft'
            elif rec.state == 'closed':
                new_state = 'draft'
            else:   
              continue  # Ignore unexpected states

        rec.create_history_record(old_state, new_state)  # Log the state change
        rec.state = new_state  # Update the state

# Server action to mark property as closed
    def action_closed(self):
        for rec in self:
            old_state = rec.state  # Store the current state
            new_state = 'closed'  # New state
            rec.create_history_record(old_state, new_state)  # Log the transition
            rec.state = new_state  # Apply the new state

    # server action of wizard
    def action_open_change_state_wizard(self):
        action=self.env['ir.actions.actions']._for_xml_id('app_one.action_change_state_wizard')
        #use context to set default value 
        action['context']={'default_property_id': self.id}
        return action
    
                
    #Automated action

    #self: refer to model and not contain records(ids)=> must use search(orm method) to return for you set records to operate on it
    def check_expected_selling_date(self):
        print(self)
        property_ids = self.search([])  # return all records       
        for rec in property_ids:
            if rec.state in ['draft', 'pending']:
                if rec.expected_selling_date and rec.expected_selling_date < fields.Date.today():
                    rec.is_late = True
            
            
    # env=> object(instance) from class odoo.api.Environment
    # usages of env :
    # 1- can access on logined(current)user=>print(self.env.user)=>return record of user(hold all data of user at record )  
    # 2- can access on company 
    # 3- can access on context => object has set of info such as  lang ,time zone ,user id ,...
    # 4- can access on cr =>object of Cursor
    # 5- can access on any model at module through [env] and use any method inside it 
    # print(self.env.user.name)    
    # print(self.env.uid)   => without return whole record    
    # print(self.env.company.street)
    # print(self.env.context)
    # print(self.env.context)
    # print(self.env['owner'].create({
    #       'name':'name one',
    #       'phone':'01232566587',
    #       'address':'12 street'
    #   }) )
    #************************************************[domain]*******************************
    
    #domain => use with [search , views(filter,..) , Security(record rule)]
    #Logic opertors : (And | Or | not ) & => it means that all conditions must be met simultaneously for a record to be retrieved.
    # Commonly used operators with domain: (= | > | < | in (followed by a list or tuple) | != | like | ilike )
    #like VS ilike opertaors with domain in odoo ?=> |The like operator is used to search for records that match a specific pattern. It is case-sensitive,
    #The ilike operator is similar to the like operator, but it is case-insensitive., regardless of the case.
    def action(self):
        # [('name','=','Prop11'),(),()]
        # print(self.env['property'].search([('name','!=','Modern Apartment Downtown')])) 
        # print(self.env['property'].search(['|',('postcode','=','12345'),('facades','=','3')])) 
        print(self.env['property'].search(['&',('postcode','=','12345'),('facades','=','3')])) 
         
 
#######################################Sequence####################################################### 
       #Sequence => string : [prefix + serial number] => table=> ir.sequence
       #what is benefit from Sequence   
       
       # #Create d
    @api._model_create_multi
    def create(self,vals_list):
        res=super(Property,self).create(vals_list)
        if res.ref=="New":
            res.ref=self.env["ir.sequence"].next_by_code("property_seq")          
        return res   
            
     
    def create_history_record(self, old_state, new_state,reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,  # Log the user who made the change
                'property_id': rec.id,  # Link the history record to the property
                'old_state': old_state,  # Store previous state
                'new_state': new_state,  # Store new state
                'reason': reason or "",
                #Copying Related Property Lines use => magic | cammand tuple 
                'line_ids':[(0, 0,{'description':line.description,'area':line.area})for line in rec.line_ids] 
                
            })
            
            
    #CRUD Operation => Create , Read(Search , Read , )   
    # #Create 
    # @api._model_create_multi
    # def create(self,vals_list):
    #     res=super(Property,self).create(vals_list)
    #     print("Create Method Called") #Logic 
    #     return res
    
    # #Search
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #    # Correct the super call by removing the redundant 'self' argument
    #    res = super(Property, self)._search(domain, offset=offset, limit=limit, order=order, access_rights_uid=access_rights_uid)
    #    print("Search Method Called")  # Debugging statement
    #    return res

    #  #write
    # def write(self,vals_list):
    #     res=super(Property,self).write(vals_list)
    #     print("Write Method Called") #Logic 
    #     return res   
      
    #  #unlink
    # def unlink(self):
    #     res=super(Property,self).unlink()
    #     print("unlink Method Called") #Logic
    #     return res   
    
    
    # Smart Button to open related owner
    def action_open_related_owner(self):
        action= self.env['ir.actions.act_window']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.view_owner_form').id
        action['res_id'] = self.owner_id.id
        action['views'] =[[view_id,'form']]
        return action
        
         
    #the get_properties method will send a request to the Controller at the /v1/properties endpoint using requests.get,
    #and it will receive the response in the response variable.
    #Then it prints the response content with print(response.content).     
    
    # WORK as a Client  
    def get_properies(self):
        #i want to call endpoint that get properies 
        payload=dict() #make this to in case needed to add body with method 
        response = requests.get('http://localhost:8069/v1/properties',data=payload) #not need to payload(body of get)
        print(response.content)

# adding Lines         
class PropertyLine(models.Model):
    _name = "property.line"
    _description = "Property Line"

    area = fields.Float(string="Area")
    description = fields.Text(string="Description")
    property_id = fields.Many2one("property", string="Property")

    
    
    
    
    
    # there are two types of files must add to folder of translation
    # => exts : pot | po
    # => first type(pot):template => file has all terms that will translate at another files(po) and is one onlyto each custom addon
    # => second type(po):set of files => each lang is has file(po) 
    # => To translate terms that exist at po => there two types 
    # =>1- write at empty string الترجمه بتاعه كل حاجه 
    # =>2- use tool :=> po edit => 
    
    
    
    
    
    
