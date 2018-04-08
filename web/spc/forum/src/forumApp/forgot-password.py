import MySQLdb as db
import os
from passlib.apache import HtpasswdFile

roll_number = raw_input("Enter Roll Number : ")
password = raw_input("Password : ")
print roll_number,password


def add_user(username,password):
		cwd = os.path.abspath(__file__)[:-18]
		if os.path.exists(cwd+".b17-dbms-htpasswd") == False:
				ht = HtpasswdFile(cwd+".htpasswd", new=True)
				result = ht.set_password(username, password)
				ht.save()
				return result
		else:
				ht = HtpasswdFile(cwd+".htpasswd")
				result = ht.set_password(username, password)
				ht.save()
				print
				print "Password Changed"
				return result
		


add_user(roll_number,password)
