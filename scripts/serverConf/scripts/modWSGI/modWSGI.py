
import os

def wsgiConfig(domain):

    wsgiLoad=open("/etc/apache2/mods-available/wsgi.load","w")
    wsgiLoad.writelines("LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so\n")
    wsgiLoad.close()

    #os.system("cp data/forum.conf /etc/apache2/conf-available/"+domain+".conf")
    os.system("sed -i '2s/example.com/"+domain+"/' /etc/apache2/conf-available/"+domain+".conf")

    return True

if __name__=="__main__":
    wsgiConfig("pucsd.online")

