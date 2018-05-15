import json
from dao.user import add_user, is_user_exist, insert_user

def signup(email, username, password):
    if is_user_exist(email):
        return '400 Bad Request', {}

    #ht_result = add_user(username, password)
    db_result = insert_user(email, username)

    if not db_result:
        return '500 Internal Server Error(DB)', {}
    return '201 Created', {}

def application(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    body = environ['wsgi.input'].read(request_body_size)
    data = json.loads(body)

    email = str(data["email"])
    username = str(data["username"])
    password = str(data["password"])

    status ,output = signup(email, username, password)
    output = json.dumps(output)

    response_headers = [('Content-type', 'application/json'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]
