from dao.db_connection import get_db_connection
from dao.user import get_user_by_email
import os

def insert_new_post(email, PostText):
    conn, cursor = get_db_connection("forum")
    result = (False, None)

    try:
        cursor.execute("""INSERT INTO comments (comment_text, commenting_user_email) VALUES (%s, %s)""",(PostText, email))
        result = (True, cursor.lastrowid)
        conn.commit()
    except:
        conn.rollback()
    conn.close()
    return result

def insert_comment_hierarchy(ParentId, comment_id):
    conn, cursor = get_db_connection("forum")
    result = True

    try:
        if ParentId:
            cursor.execute("""INSERT INTO comment_hierarchy(comment_id, parent_comment_id) VALUES (%s, %s)""",(comment_id,ParentId))
        else:
            cursor.execute("""INSERT INTO comment_hierarchy(comment_id) VALUES (%s)""",(comment_id))
        conn.commit()
    except:
        result = False
        conn.rollback()
    conn.close()
    return result

def updatePostInDB(CommentId, PostText):
    conn, cursor = get_db_connection("forum")
    result = False

    try:
        cursor.execute("""UPDATE comments SET comment_text = %s WHERE comment_id = %s""",(PostText, CommentId))
        result = True
        conn.commit()
    except:
        conn.rollback()
    conn.close()
    return result

def getAllTopics():
    conn, cursor = get_db_connection("forum")
    query = 'select * from comments where comment_id IN (select comment_id from comment_hierarchy where parent_comment_id IS NULL);'

    cursor.execute(query)
    row = cursor.fetchall()
    conn.close()
    return row

def get_comment_by_id(comment_id):
    conn, cursor = get_db_connection("forum")

    cursor.execute("""select * from comments where comment_id=%s""",str(comment_id))
    row = cursor.fetchone()
    conn.close()
    return row

def get_child_by_parent_id(parent):
    conn, cursor = get_db_connection("forum")

    cursor.execute("""select * from comment_hierarchy where parent_comment_id=%s""",str(parent))
    row = cursor.fetchall()
    conn.close()
    return row

def html_hierarchical_comments(root, parentRoot, level, header):
    getButtonVal = lambda : 'Comment' if header=="1" else 'Reply'

    record = get_comment_by_id(root)
    email, post = record["commenting_user_email"], record["comment_text"]

    user = get_user_by_email(email)
    username = user["username"]

    child, rootParent = str(root), str(parentRoot)

    spacing = ''.join("&nbsp;" * level)
    header_start = "<div class='postText'><h"+header+">"
    username_post = '<div id="'+child+'_post"><b>'+username+'</b>'+" "+post+"</div></h"+header+">"

    links_div_start = '<div style="align:right;display:inline-block";>'
    reply = '<h6 class="col-sm-1"><a href="#" id="'+child+'" onclick="reply(this.id)">'+getButtonVal()+'</a></h6>'
    edit = '<h6 class="col-sm-1"><a href="#" id="'+child+'" onclick="edit(this.id)">Edit</a></h6>'
    links_div_ends = '</div>'

    reply_textarea = '<div id="'+child+'_textarea_reply_div" hidden><textarea id="'+child+'_textarea_reply"></textarea>'
    reply_textarea_button = '<button id="'+child+'_reply" onclick="submit_reply(this.id,'+rootParent+')">Reply</button></div>'

    edit_textarea = '<div id="'+child+'_textarea_edit_div" hidden><textarea id="'+child+'_textarea_edit">'+post+'</textarea>'
    edit_textarea_button = '<button id="'+child+'_edit" onclick="submit_edit(this.id,'+rootParent+')">Submit</button></div>'
    header_ends = '</div><br>'

    html, record_html = "", ""
    for child in get_child_by_parent_id(root):
        record_html += html_hierarchical_comments(child["comment_id"], parentRoot, level+8, "4")

    html += spacing+header_start+username_post+links_div_start+edit+reply+links_div_ends+edit_textarea+edit_textarea_button+reply_textarea+reply_textarea_button+header_ends+record_html
    return html


# Not Using This Function instead of this ->> html_hierarchical_comments
def hierarchical_comments(root):
    hierarchy = get_comment_by_id(root)
    user = get_user_by_email(hierarchy["commenting_user_email"])
    hierarchy["commenting_user_email"] = user["username"]

    childs = []
    for child in get_child_by_parent_id(root):
        childs.append(hierarchical_comments(child['comment_id']))

    hierarchy["children"] = childs
    return hierarchy

    #html += "<div class='postText'><h"+header+">"+''.join("&nbsp;" * level)+'<b>'+username+'</b>'+" "+'<p>'+post+'</p>'+'<h6 align="right"><a href="#" id="'+child+'" onclick="reply(this.id)">Reply</a></h6><div id="'+child+'_textarea_reply_div"  hidden><textarea id="'+child+'_textarea_reply"'+'></textarea><button id="'+child+'" onclick="submit_reply(this.id,'+rootParent+')">Reply</button></div></h'+header+'></div><br>'
    #html += "<h"+header+">"+''.join("&nbsp;" * level)+record["commenting_user_email"]+" : "+record["comment_text"]+'<h6 align="right"><button id="'+str(root)+'" onclick="reply(this.id)">Reply</button></h6><div id="'+str(root)+'_textarea_reply_div"  hidden><textarea id="'+str(root)+'_textarea_reply"'+'></textarea><button id="'+str(root)+'" onclick="submit_reply(this.id)">Submit Reply</button></div></h'+header+'><hr>'
