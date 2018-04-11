import os

def postfixConfig(domain):

    #Postfix config
    #master.cf changes
    os.system("sed -i '12s/smtp/2525/' /etc/postfix/master.cf")

    allowedSP="gmail.com,smtp.gmail.com,yahoo.com,hotmail.com,aol.com"
    #main.cf changes
    os.system('postconf -e "myorigin ='+domain+'"')
    os.system('postconf -e "myhostname = '+domain+'"')
    os.system('postconf -e "relay_domains = '+domain+','+allowedSP+' "')
    maincf=open("/etc/postfix/main.cf","a")
    maincf.write("milter_protocol = 2\nmilter_default_action = accept\n")
    maincf.close()

    return True
