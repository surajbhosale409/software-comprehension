import json, os
from dao.user import is_valid_user, get_user_by_email

def login(email, password):
    if is_valid_user(email, password):
        user = get_user_by_email(email)
        return '200 Ok', {responseData: user["username"]}

    try:
        user = get_user_by_email(email)
        return '200 Ok', {"responseData": user["username"]}
    except:
        return '401 Unauthorized', {}

def application(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    body = environ['wsgi.input'].read(request_body_size)
    data = json.loads(body)

    email = str(data["email"])
    password = str(data["password"])

    status ,output = login(email, password)
    output = json.dumps(output)

    response_headers = [('Content-type', 'application/json'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]
