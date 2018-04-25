import sys,os

def setupDebian():

    os.system("apt-get install -y apache2 libapache2-mod-proxy-html libxml2-dev ")
    cmds=["a2enmod proxy" ,"a2enmod proxy_http","a2enmod proxy_ajp","a2enmod rewrite","a2enmod deflate","a2enmod headers","a2enmod proxy_balancer","a2enmod proxy_connect","a2enmod proxy_html"]

    for cmd in cmds:
        os.system(cmd)
    os.system("cp data/000-default.conf /etc/apache2/sites-enabled/000-default.conf  && service apache2 restart")

def setupRHEL():
    os.system("yum install -y httpd")
    os.system("data/000-default.conf /etc/httpd/conf.d/default-site.conf")
    os.system("systemctl restart httpd")

def setup():
    print "Enter OS Debian/RHEL [D/R]"
    if raw_input()=="D":
        setupDebian()
    else:
        setupRHEL()

if __name__=="__main__":
    setup()
