import os

def installPackages():
    #Installing needed packages
    packages="apache2 python2.7 libapache2-mod-wsgi  mysql-server python-mysqldb python-passlib python-requests postfix telnet telnetd libmilter-dev libssl-dev openssl opendkim opendkim-tools vde2 uml-utilities openssh-server"
    os.system("apt-get install "+packages+" -y")

    return True
