import sys,os

def setup():
    os.system("apt-get install -y libapache2-mod-proxy-html libxml2-dev build-essential")

    cmds=["a2enmod proxy" ,"a2enmod proxy_http","a2enmod proxy_ajp","a2enmod rewrite","a2enmod deflate","a2enmod headers","a2enmod proxy_balancer","a2enmod proxy_connect","a2enmod proxy_html"]
    for cmd in cmds:
        os.system(cmd)

    os.system("cp data/000-default.conf /etc/apache2/sites-enabled/000-default.conf  && service apache2 restart")
