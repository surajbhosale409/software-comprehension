
import os

def wsgiConfig(domain):

    wsgiLoad=open("/etc/apache2/mods-available/wsgi.load","w")
    wsgiLoad.writelines("LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so\n")
    wsgiLoad.close()
    return True

if __name__=="__main__":
    wsgiConfig("pucsd.online")

