from odoo import http

class TestApi(http.Controller):
    # Defining the route with the correct endpoint '/api/test'
    #type => http | json
    @http.route('/api/test1', methods=['GET'],type='http', auth='none', csrf=False)
    def test_endpoint(self):
        # Logging the method call for debugging purposes
        print("inside test_endpoint method")
        # Returning a simple response to confirm the endpoint is working
        return "Test endpoint reached!"
    
