from passlib.apache import HtpasswdFile
from collections import OrderedDict
from string import Template
import json, os, datetime
import MySQLdb as db


TEMPLATE_DIR = os.path.dirname(__file__)
mysql_username = "www-data"
mysql_password = "S"

def check_user_password_htpasswd(username,password):
    cwd = os.path.abspath(__file__)[:-8]
    ht = HtpasswdFile(cwd+".htpasswd")
    return ht.check_password(username, password)

def add_user(username,password):
    cwd = os.path.abspath(__file__)[:-8]
    if os.path.exists(cwd+".htpasswd") == False:
        ht = HtpasswdFile(cwd+".htpasswd", new=True)
        result = ht.set_password(username, password)
        ht.save()
        return result
    else:
        ht = HtpasswdFile(cwd+".htpasswd")
        result = ht.set_password(username, password)
        ht.save()
        if result == False:
            return True

def get_db_connection(database_name):
    database = db.connect('localhost',mysql_username,mysql_password,database_name)
    return database, database.cursor()


def perform_sql_action(database_name,query, action):
		try:
				db_con, db_cur = get_db_connection(database_name)
				db_cur.execute(query)
				if(action == 'select'):
						result = db_cur.fetchall()
						db_cur.close()
						return result
				else:
						db_con.commit()
						db_con.close()
		except Exception as e:
				return "DatabaseError, "+str(e)

def touple_to_list(touple):
    return map(lambda x:x[0],touple)

def insert_post_into_database(data):
    try:
        new_post = str(data["new_post"])
        username = str(data["email"])

        get_user_id_query = 'select user_id from user_details where username = "'+ username +'";'
        user_id = str(touple_to_list(perform_sql_action("forum",get_user_id_query,"select"))[0])

        query = 'insert into comments (comment_text,commenting_user_id) values ("'+new_post+'","'+user_id+'");'
        perform_sql_action("forum",query,"insert")

        get_comment_id_query = 'select max(comment_id) from comments;'

        comment_id = str(touple_to_list(perform_sql_action("forum",get_comment_id_query,"select"))[0])
        query = 'insert into comment_hierarchy(comment_id) values('+comment_id+');'
        perform_sql_action("forum",query,"insert")
        return "True"
    except Exception as e:
        print e
        return "username not found : " + username




def login(data):
    # call check_username_into_database here    
    email ,passwd = str(data["email"]), str(data["password"])

    if check_user_password_htpasswd(email, passwd):
        return "True"
    return "False"

def check_username_into_database(username):
    pass
    # return true here is username is already present in database
    # else return false

def insert_new_comment_into_database(data):
    try:
        new_post = str(data["new_comment"])
        username = str(data["email"])
        parent_comment_id = str(data["comment_id"])

        get_user_id_query = 'select user_id from user_details where email = "'+ username +'";'
        
        user_id = str(touple_to_list(perform_sql_action("forum",get_user_id_query,"select"))[0])

        query = 'insert into comments (comment_text,commenting_user_id) values ("'+new_post+'","'+user_id+'");'
        perform_sql_action("forum",query,"insert")

        get_comment_id_query = 'select max(comment_id) from comments;'
        comment_id = str(touple_to_list(perform_sql_action("forum",get_comment_id_query,"select"))[0])

        query = 'insert into comment_hierarchy(comment_id,parent_comment_id) values('+comment_id+','+parent_comment_id+');'
        perform_sql_action("forum",query,"insert")
        return "True"
    except Exception as e:
        print e
        return "username not found : " + username

def signup(data):
    # call check_username_into_database here
    email,passwd,cnf_passwd,username = str(data["email"]), str(data["password"]),str(data["cnf_password"]),str(data["username"])
    
    add_user(username,passwd)
    if passwd != cnf_passwd:
        return "Password and Confirm Password Not matched"
    
    query = 'insert into user_details (username,email) values ("'+username+'","'+email+'");'
    perform_sql_action("forum",query,"insert")
    return "True"
    
    # database query for dump details into database
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def childs(parent):
    sql_query = "select * from comment_hierarchy where parent_comment_id="+str(parent)+";"
    return perform_sql_action("forum",sql_query,"select")

def get_comments(comment_id):
    sql = "select * from comments where comment_id="+str(comment_id)+";"
    return perform_sql_action("forum",sql,"select")


def convert_to_html(ele ,level):
    html = ""
    if isinstance(ele, dict):
        for key,val in ele.items():
            if key == 'comment_text':
                html += str(ele[key])
    return html

def get_user_details_by_id(user_id):
    print user_id
    query = "select * from user_details where user_id="+str(user_id)+";"
    post = perform_sql_action("forum",query,"select")
    return post[0][1]

def hierarchical_comments(root ,level ,header):
    html = ""
    for record in get_comments(root):
        record_html = ""
        id_ = 'id="'+str(root)+'"'
        username = get_user_details_by_id(record[2])
        record_html += "<h"+header+">"+''.join("&nbsp;" * level)+str(username)+" : "+record[1]+'<h6 align="right"><button id="'+str(root)+'" onclick="reply(this.id)">Reply</button></h6><div id="'+str(root)+'_textarea_reply_div"  hidden><textarea id="'+str(root)+'_textarea_reply"'+'></textarea><button id="'+str(root)+'" onclick="submit_reply(this.id)">Submit Reply</button></div></h'+header+'><hr>'
        for child in childs(root):          
            record_html += hierarchical_comments(child[0], level+8, "4")
        html += record_html
    return html

#def hierarchical_comments(root):
#    child_json = OrderedDict()
#    for indx, child in enumerate(childs(root)):
#        for record in get_comments(child[0]):
#            json_record = OrderedDict()
#            json_record["comment_id"] ,json_record["commenting_user_id"] = record[0] ,record[2]
#            json_record["comment_text"] ,json_record["timestamp"] = record[1], datetime.datetime.strftime(record[3], '%d/%m/%Y %I:%M:%S %p')
#        json_record["child"] = hierarchical_comments(child[0])
#        child_json[str(indx)] = json_record
#    return child_json

def recusion_on_dict(post_hierarchy ,level ,htmlString):
    for key ,ele in post_hierarchy.items():
         if isinstance(ele, dict):
            htmlString += convert_to_html(ele, level)
            if key == 'child' and isinstance(ele, dict):
                for k, v in ele.items():
                    htmlString += recusion_on_dict(v ,level+8 ,htmlString)
    return htmlString

def get_comments_by_id(data):
    comment_id = data["id"]
    return hierarchical_comments(int(comment_id), 2 ,"1")
    #post_hierarchical_records = hierarchical_comments(int(comment_id) ,2)
    #html = recusion_on_dict(post_hierarchical_records ,2 ,"")
    #return str(comment_id)

def convert_to_dict(element):
    record_dict = {}
    record_dict["comment_id"], record_dict["post"] = element[0], element[1]
    return record_dict 

def get_topics():
    query = "select * from comments where comment_id IN (select comment_id from comment_hierarchy where parent_comment_id IS NULL);"
    post = perform_sql_action("forum",query,"select")
  
    return json.dumps(map(convert_to_dict ,post))
    
    ## read topics from database and
    ## return topics into json here
    
def application(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    body = environ['wsgi.input'].read(request_body_size)
    data = json.loads(body)

    response_headers = [('Content-type', 'text/html')]
    
    start_response('200 OK', response_headers)
    
    request = str(data["request"])
    if request == "login":
        return login(data)
    
    if request == "signup":
        return signup(data)

    if request == "new_topic":
        return insert_post_into_database(data)
    
    if request == "new_comment":
        return insert_new_comment_into_database(data)
    
    if request == "get_topics":
        return get_topics()
        #return get_topics(data)
    if request == "get_comments":
        return get_comments_by_id(data)
    