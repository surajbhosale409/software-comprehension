from dao.db_connection import get_db_connection
from passlib.apache import HtpasswdFile
import os

def add_user(email, password):
    cwd = os.path.abspath(__file__)[:-7]

    if not os.path.exists(cwd + ".htpasswd"):
        ht = HtpasswdFile(cwd + ".htpasswd", new=True)
    else:
        ht = HtpasswdFile(cwd + ".htpasswd")

    result = ht.set_password(email, password)
    ht.save()
    return result

def get_user_by_email(email):
    conn, cursor = get_db_connection("forum")
    query = 'select * from user_details where email = "'+ email +'";'

    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()
    return row

def is_user_exist(email):
    row = get_user_by_email(email)
    if row is None:
        return False
    return True

def is_valid_user(email, password):
    cwd = os.path.abspath(__file__)[:-7]
    ht = HtpasswdFile(cwd + ".htpasswd")
    return ht.check_password(email, password)

def insert_user(email, username):
    conn, cursor = get_db_connection("forum")
    result = True

    try:
        cursor.execute("""INSERT INTO user_details (username, email) VALUES (%s, %s)""",(username, email))
        conn.commit()
    except:
        conn.rollback()
        result = False
    conn.close()
    return result
