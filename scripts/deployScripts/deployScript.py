import getpass,sys,os

if getpass.getuser()!="root":
    print "Needs root privileges"
    sys.exit()

def deploy():
    cwd=os.getcwd()
    os.chdir("/")
    os.system("tar -xvzf "+cwd+"/data/spcforum.tar.gz ")
    os.chdir(cwd)
    os.system("cp data/myforum.conf /etc/apache2/conf-available")
    os.system("cp data/default-ssl.conf /etc/apache2/sites-available")
    os.system("a2enconf myforum && service apache2 reload")
    os.system("mysql -u root -p < data/initDB.sql")
    os.system("mysql -u root -p forum < data/forum_dump.sql")
    os.system("mysql -u root -p forum_log < data/forum_log_dump.sql")



deploy()
