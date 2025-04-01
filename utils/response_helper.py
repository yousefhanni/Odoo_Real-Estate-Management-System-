from odoo.http import request

def valid_response(data, status=200):
    response_body = {
        'message': 'successful',
        'data': data,
    }
    return request.make_json_response(response_body, status=status)

def error_response(message, status=500):
    return request.make_json_response({'error': message}, status=status)









#Why it's useful:
# Reduces code duplication by centralizing response formatting.
# Ensures consistent API response format.(بيوحد الstructure على مستوى ال collection)
# Makes it easier to modify response structure later (e.g., adding logging or metadata).