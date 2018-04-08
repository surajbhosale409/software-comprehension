#!/usr/bin/python
import MySQLdb, numpy, collections

db = MySQLdb.connect("localhost", "root", "v", "forum")
cursor = db.cursor()

def childs(parent):
    sql = "select * from comment_hierarchy where parent_comment_id="+str(parent)+";"
    cursor.execute(sql)
    return cursor.fetchall()

def get_comments(comment_id):
    sql = "select * from comments where comment_id="+str(comment_id)+";"
    cursor.execute(sql)
    return cursor.fetchall()

def hierarchical_comments(root):
    child_json = {}
    for indx, child in enumerate(childs(root)):
        for record in get_comments(child[0]):
            json_record = {} 
            json_record["comment_id"] ,json_record["commenting_user_id"] = record[0] ,record[2]
            json_record["comment_text"] ,json_record["timestamp"] = record[1] ,record[3]
        json_record["child"] = hierarchical_comments(child[0])
        child_json[str(indx)] = json_record
    return child_json

hr = hierarchical_comments(2)
#[ {k,hr[k]} for k in sorted(hr.keys()) ] 
print dict(hr)
#print {k[0]:k[1] for k in sorted(hr.items(), key=operator.itemgetter(1))}
db.close()
