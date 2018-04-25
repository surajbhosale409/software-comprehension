import getpass,sys,os


if getpass.getuser()!="root":
    print "run as root"
    sys.exit()

def setup_ssl():
    cwd=os.getcwd()
    os.system("openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt;");
    os.system("openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048;");
    os.system("cp ssl-params.conf /etc/apache2/conf-available/ ;");
    os.system("cp /etc/apache2/sites-available/default-ssl.conf /etc/apache2/sites-available/default-ssl.conf.bak ;");
    os.system("a2enmod ssl ;");
    os.system("a2enmod headers ;");
    os.system("a2ensite default-ssl ;");
    os.system("a2enconf ssl-params ;");
    os.system("apache2ctl configtest ;");
    os.system("service apache2 reload");
    os.system("service apache2 restart");


if __name__=="__main__":
    setup_ssl()
