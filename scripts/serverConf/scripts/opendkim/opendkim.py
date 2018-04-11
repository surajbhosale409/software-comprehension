import os

def opendkimConfig(cwd,ipDomainList):

    #Configuring opendkim

    os.system("cp data/opendkim.conf /etc/opendkim.conf ")
    os.system("mkdir -p /etc/opendkim/keys/")

    keytab=open("/etc/opendkim/KeyTable","w")
    signtab=open("/etc/opendkim/SigningTable","w")
    trusthost=open("/etc/opendkim/TrustedHosts","w")
    trusthost.writelines("127.0.0.1\n")

    i=0
    for rec in ipDomainList:
        key="mail"+str(i)
        keytab.writelines(key+"._domainkey."+rec[1]+" "+rec[1]+":"+key+":/etc/opendkim/keys/"+key+".private\n")
        signtab.writelines("*@"+rec[1]+" "+key+"._domainkey."+rec[1]+"\n")
        trusthost.writelines(rec[1]+"\n")
        os.system("mkdir -p /etc/opendkim/keys/"+rec[1])
        os.chdir("/etc/opendkim/keys/"+rec[1])
        os.system("opendkim-genkey -s "+key+" -d "+rec[1])
        os.chdir(cwd)
        i+=1

    keytab.close()
    signtab.close()
    trusthost.close()
    defaultOpendkim=open("/etc/default/opendkim","w")
    defaultOpendkim.writelines('SOCKET="inet:8891@localhost"\n')
    defaultOpendkim.close()

    return True
