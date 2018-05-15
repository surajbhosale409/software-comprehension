import json, os
from dao.user import get_user_by_email
from dao.post import insert_new_post, insert_comment_hierarchy, getAllTopics, html_hierarchical_comments, updatePostInDB, hierarchical_comments
from bson import json_util

def createNewPost(PostText, ParentId, email):
    dbPostResult = insert_new_post(email, PostText)

    if ParentId:
        dbHierarchyResult = insert_comment_hierarchy(ParentId, dbPostResult[1])
    else:
        dbHierarchyResult = insert_comment_hierarchy(None, dbPostResult[1])

    if dbPostResult[0] and dbHierarchyResult:
        return '201 Created', {}
    return '400 Bad Request', {}

def updatePost(CommentId, PostText):
    updateResult = updatePostInDB(CommentId, PostText)

    if updateResult:
        return '200 Record Updated Successfully', {}
    return '400 Bad Request', {}

def application(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    method = environ.get('REQUEST_METHOD')
    url_params = environ.get('QUERY_STRING')

    if method == 'POST':
        body = environ['wsgi.input'].read(request_body_size)
        data = json.loads(body)

        PostType = str(data["PostType"])
        PostText = str(data["PostText"])
        email = str(data["email"])

        if PostType == "Parent":
            status ,output = createNewPost(PostText, None, email)
        elif PostType == "Child":
            ParentId = str(data["parent_id"])
            status ,output = createNewPost(PostText, ParentId, email)
        output = json.dumps(output)
    elif method == 'PUT':
        body = environ['wsgi.input'].read(request_body_size)
        data = json.loads(body)

        PostText = str(data["PostText"])
        CommentId = str(data["CommentId"])
        status ,output = updatePost(CommentId, PostText)
        output = json.dumps(output)
    elif method == 'GET':
        urlParamsList = url_params.replace('&',' ').replace('=',' ').split()

        if urlParamsList:
            comment, commentVal, login, loginVal = urlParamsList
            if json.loads(loginVal.lower()):
                status, output = '200 Ok', html_hierarchical_comments(commentVal, commentVal, 2 ,'1')
                response_headers = [('Content-type', 'text/html')]
                start_response('200 OK', response_headers)
                return [output]
            else:
                status, output = '200 Ok', {"responseData": hierarchical_comments(commentVal)}
        else:
            status, output = '200 Ok', {"responseData": list(getAllTopics())}
        output = json.dumps(output, default=json_util.default)

    response_headers = [('Content-type', 'application/json'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]
