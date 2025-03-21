# Importing TransactionCase from odoo.tests.common to create test cases that interact with the database in a controlled transaction environment.
# What is TransactionCase in Odoo (Brief):
# TransactionCase is a base class in Odoo for writing unit tests. It runs each test inside a database transaction, 
# automatically rolling back (undoing) all changes after the test finishes, ensuring the database remains unchanged and tests are isolated.

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo import fields

class TestProperty(TransactionCase):
    
    # Override the setUp method to create dummy records 
    def setUp(self, *args, **kwargs):
        super(TestProperty, self).setUp()
           
        # Create a dummy owner record since owner_id is a Many2one field
        self.owner = self.env['owner'].create({
            'name': 'Test Owner',
            'phone': '1234567890',
            'address': '123 Test Street',
        })
        
        # Create a dummy property record with realistic data
        self.property_01_record = self.env['property'].create({
            'name': 'Property 01',
            'description': 'This is a property 01',
            'postcode': '12345',
            'date_availability': fields.Date.today(),  # Keep as today
            'expected_selling_date': fields.Date.today(),  # Keep as today
            'expected_price': 1000000.0,  # To trigger the onchange for garden_area
            'selling_price': 900000.0,
            'bedrooms': 3,
            'living_area': 120,
            'facades': 2,
            'garage': True,
            'garden': True,
            'garden_area': 100,
            'garden_orientation': 'north',
            'state': 'draft',
            'owner_id': self.owner.id,
            'active': True,
        })
        
        # Create a second property for testing constraints
        self.property_02_record = self.env['property'].create({
            'name': 'Property 02',
            'description': 'This is a property 02',
            'postcode': '67890',
            'date_availability': fields.Date.today(),  # Keep as today
            'expected_selling_date': fields.Date.today(),  # Keep as today
            'expected_price': 500000.0,
            'selling_price': 450000.0,
            'bedrooms': 2,
            'living_area': 80,
            'facades': 1,
            'garage': False,
            'garden': False,
            'garden_area': 0,
            'garden_orientation': 'south',
            'state': 'pending',
            'owner_id': self.owner.id,
            'active': True,
        })
        
        
     #what is benefits assertRecordValues method?     
     #1-Ensuring Correct Creation: It verifies that the property_01_record is stored with the correct values specified in the setUp.
     #2-Early Error Detection: It detects any issues in the creation process (like constraints or logic altering values) before they impact other tests.
    def test_property_values(self):
        """Test the property values for the first property."""
        property_id = self.property_01_record
        # assertRecordValues:is a method provided by TransactionCase in Odoo to compare the actual values of a record (or multiple records) with expected values.
        self.assertRecordValues(property_id, expected_values=[
           {
            'name': 'Property 01',
            'description': 'This is a property 01',
            'postcode': '12345',
            'date_availability': fields.Date.today(),
            'expected_selling_date': fields.Date.today(),
            'expected_price': 1000000.0,
            'selling_price': 900000.0,
            'bedrooms': 3,
            'living_area': 120,
            'facades': 2,
            'garage': True,
            'garden': True,
            'garden_area': 100,
            'garden_orientation': 'north',
            'state': 'draft',
            'owner_id': self.owner.id,
            'active': True,
        }
    ])
    

    # def test_difference_price_calculation(self):
    #     """Test the computation of difference_price field."""
    #     self.assertEqual(
    #         self.property_01_record.difference_price,
    #         100000,  # 1000000 - 900000
    #         "The difference price calculation is incorrect!"
    #     )

    # def test_onchange_expected_price(self):
    #     """Test the onchange method for expected_price affecting garden_area."""
    #     # Update expected_price to trigger onchange
    #     self.property_01_record.expected_price = 1500000
    #     self.property_01_record._onchange_expected_price()
    #     self.assertEqual(
    #         self.property_01_record.garden_area,
    #         500,
    #         "Garden area should be set to 500 when expected_price > 1000000!"
    #     )

    # def test_unique_name_constraint(self):
    #     """Test the unique_name SQL constraint."""
    #     with self.assertRaises(ValidationError):
    #         self.env['property'].create({
    #             'name': 'Property 01',  # Same name as property_01_record
    #             'postcode': '54321',
    #             'bedrooms': 2,
    #             'owner_id': self.owner.id,
    #         })

    # def test_required_fields_validation(self):
    #     """Test the Python-level validation for required fields."""
    #     # Test empty name
    #     with self.assertRaises(ValidationError):
    #         self.env['property'].create({
    #             'name': '',
    #             'postcode': '54321',
    #             'bedrooms': 2,
    #             'owner_id': self.owner.id,
    #         })

    #     # Test empty postcode
    #     with self.assertRaises(ValidationError):
    #         self.env['property'].create({
    #             'name': 'Property 03',
    #             'postcode': '',
    #             'bedrooms': 2,
    #             'owner_id': self.owner.id,
    #         })

    #     # Test invalid bedrooms
    #     with self.assertRaises(ValidationError):
    #         self.env['property'].create({
    #             'name': 'Property 03',
    #             'postcode': '54321',
    #             'bedrooms': 0,
    #             'owner_id': self.owner.id,
    #         })

    # def test_change_state_draft_to_pending(self):
    #     """Test state transition from draft to pending."""
    #     self.property_01_record.change_state()
    #     self.assertEqual(
    #         self.property_01_record.state,
    #         'pending',
    #         "State should change from draft to pending!"
    #     )

    # def test_change_state_pending_to_sold(self):
    #     """Test state transition from pending to sold."""
    #     self.property_02_record.change_state()
    #     self.assertEqual(
    #         self.property_02_record.state,
    #         'sold',
    #         "State should change from pending to sold!"
    #     )

    # def test_action_closed(self):
    #     """Test the action_closed method to set state to closed."""
    #     self.property_01_record.action_closed()
    #     self.assertEqual(
    #         self.property_01_record.state,
    #         'closed',
    #         "State should be set to closed!"
    #     )

    # def test_check_expected_selling_date(self):
    #     """Test the automated action to set is_late based on expected_selling_date."""
    #     # Set expected_selling_date to a hardcoded past date (e.g., 5 days ago)
    #     self.property_01_record.expected_selling_date = '2025-03-14'  # Hardcoded past date (today is 2025-03-19)
    #     self.property_01_record.check_expected_selling_date()
    #     self.assertTrue(
    #         self.property_01_record.is_late,
    #         "is_late should be True when expected_selling_date is in the past!"
    #     )

    # def test_create_history_record(self):
    #     """Test that a history record is created when state changes."""
    #     old_state = self.property_01_record.state
    #     new_state = 'pending'
    #     self.property_01_record.create_history_record(old_state, new_state)
    #     history = self.env['property.history'].search([('property_id', '=', self.property_01_record.id)])
    #     self.assertTrue(history, "A history record should be created!")
    #     self.assertEqual(history.old_state, old_state, "Old state should match!")
    #     self.assertEqual(history.new_state, new_state, "New state should match!")