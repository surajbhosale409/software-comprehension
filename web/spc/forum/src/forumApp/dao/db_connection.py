import MySQLdb as db

mysql_username = "root"
mysql_password = "v"

def get_db_connection(database_name):
    database = db.connect('localhost', mysql_username, mysql_password, database_name)
    return database, database.cursor(db.cursors.DictCursor)


