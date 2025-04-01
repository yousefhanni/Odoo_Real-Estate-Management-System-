import math
from urllib.parse import parse_qs
from odoo import http 
from odoo.http import request 
import json
from ..utils.response_helper import valid_response, error_response

# WORK as a server   
class PropertyApi(http.Controller):
     # Add (create) property
    @http.route('/v1/property', methods=['POST'], type='http', auth='none', csrf=False)
    def create_property(self):
        try:
            args = request.httprequest.data.decode()  # Get data from the incoming request
            vals = json.loads(args)  # Convert JSON to Python dictionary
            result = request.env['property'].sudo().create(vals)  # Create a new property record

            if result:
                return valid_response({
                    "message": "Property has been created successfully",
                    "id": result.id,
                    "name": result.name,
                }, status=201)
            else:
                return error_response("Error creating property", status=400)

        except Exception as error:
            return error_response(str(error), status=500)

    # Update property
    @http.route('/v1/property/<int:property_id>', methods=['PUT'], type='http', auth='none', csrf=False)
    def update_property(self, property_id):
        try:
            property_record = request.env['property'].sudo().search([('id', '=', property_id)])

            if not property_record:
                return error_response("Property not found", status=404)

            args = request.httprequest.data.decode()
            vals = json.loads(args)
            result = property_record.write(vals)

            if result:
                return valid_response({
                    "message": "Property has been updated successfully",
                    "id": property_record.id,
                    "name": property_record.name,
                }, status=200)
            else:
                return error_response("Error updating property", status=400)

        except Exception as error:
            return error_response(str(error), status=500)

    # Get specific property
    @http.route('/v1/property/<int:property_id>', methods=['GET'], type='http', auth='none', csrf=False)
    def get_property(self, property_id):
        try:
            property_record = request.env['property'].sudo().search([('id', '=', property_id)])

            if not property_record:
                return error_response("Property not found", status=404)

            return valid_response({
                "id": property_record.id,
                "ref": property_record.ref,
                "name": property_record.name,
                "description": property_record.description,
                "postcode": property_record.postcode,
                "date_availability": property_record.date_availability,
                "expected_selling_date": property_record.expected_selling_date,
                "is_late": property_record.is_late,
                "expected_price": property_record.expected_price,
                "selling_price": property_record.selling_price,
                "bedrooms": property_record.bedrooms,
                "living_area": property_record.living_area,
                "facades": property_record.facades,
                "garage": property_record.garage,
                "garden": property_record.garden,
                "garden_area": property_record.garden_area,
                "garden_orientation": property_record.garden_orientation,
                "state": property_record.state,
                "owner_id": property_record.owner_id.id,
                "owner_phone": property_record.owner_phone,
                "owner_address": property_record.owner_address,
                "difference_price": property_record.difference_price,
            }, status=200)

        except Exception as error:
            return error_response(str(error), status=500)

    # Get all properties
    @http.route('/v1/properties', methods=['GET'], type='http', auth='none', csrf=False)
    def get_all_properties(self):
        try:
            property_records = request.env['property'].sudo().search([])

            if not property_records:
                return error_response("No properties found", status=404)

            properties_data = []

            for property_record in property_records:
                properties_data.append({
                    "id": property_record.id,
                    "ref": property_record.ref,
                    "name": property_record.name,
                    "description": property_record.description,
                    "postcode": property_record.postcode,
                    "date_availability": property_record.date_availability,
                    "expected_selling_date": property_record.expected_selling_date,
                    "is_late": property_record.is_late,
                    "expected_price": property_record.expected_price,
                    "selling_price": property_record.selling_price,
                    "bedrooms": property_record.bedrooms,
                    "living_area": property_record.living_area,
                    "facades": property_record.facades,
                    "garage": property_record.garage,
                    "garden": property_record.garden,
                    "garden_area": property_record.garden_area,
                    "garden_orientation": property_record.garden_orientation,
                    "state": property_record.state,
                    "owner_id": property_record.owner_id.id,
                    "owner_phone": property_record.owner_phone,
                    "owner_address": property_record.owner_address,
                    "difference_price": property_record.difference_price,
                })

            return valid_response({"properties": properties_data}, status=200)

        except Exception as error:
            return error_response(str(error), status=500)

   #Get all properties with filtration and pagination
    @http.route('/v1/properties_filtered', methods=['GET'], type='http', auth='none', csrf=False)
    def get_all_properties_filtered(self):
        try:
            #filtration
            property_domain = []
            state = request.params.get('state')
            if state:
                property_domain.append(('state', '=', state.lower()))  # .lower() to standardize

            # Get pagination parameters from the request
            page = int(request.params.get('page', 1))  # Default to page 1
            limit = int(request.params.get('limit', 3))  # Default to 3 records per page
            offset = (page - 1) * limit  # Calculate the offset based on page and limit 

            properties = request.env['property'].sudo().search(property_domain, offset=offset, limit=limit, order='id DESC')
            properties_count = request.env['property'].sudo().search_count(property_domain)

            if not properties:
                return error_response("No properties found", status=404)

            result = [{
                "id": prop.id,
                "name": prop.name,
                "description": prop.description,
                "state": prop.state,
                "expected_price": prop.expected_price,
                "selling_price": prop.selling_price,
                "bedrooms": prop.bedrooms,
                "living_area": prop.living_area,
                "facades": prop.facades,
                "garage": prop.garage,
                "garden": prop.garden,
                "garden_area": prop.garden_area,
                "garden_orientation": prop.garden_orientation,
                # add other fields as needed
            } for prop in properties]

            #pagination info
            pagination_info = {
                "page": page,
                "limit": limit,
                "count": properties_count,
                "pages": math.ceil(properties_count / limit) if limit else 1,
            }

            #Return the response with the properties data and pagination info
            #The data in valid_response combines the result (list of properties) and pagination info in a single response.
            return valid_response({
                "data": result,
                "pagination_info": pagination_info
            }, status=200)

        except Exception as e:
            return error_response(str(e), status=500)

        # Delete property
    @http.route('/v1/property/<int:property_id>', methods=['DELETE'], type='http', auth='none', csrf=False)
    def delete_property(self, property_id):
        try:
            property_record = request.env['property'].sudo().search([('id', '=', property_id)])

            if not property_record:
                return error_response("Property not found", status=404)

            property_record.unlink()  # Delete the property

            return valid_response({
                "message": "Property has been Deleted successfully"
            }, status=200)

        except Exception as error:
            return error_response(str(error), status=500)
  

#to integrate with another app must=> 
# 1- pip install  requests
#2- call get properties => make method get properties at property file  

#Controler : 
# Controller acts as an intermediary between the front-end and back-end.
# Its purpose is simple:
# 1- Receive requests, process them, and return responses.




