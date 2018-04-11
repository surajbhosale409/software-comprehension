
#Reading ip domain pairs and configuring /etc/hosts

def readIpDomainFile():
    ipDomainFile=open("ipDomain","r")
    ipDomainList=[]

    for line in ipDomainFile:
        temp=line.replace("\n","")
        temp=temp.split()
        ipDomainList.append(temp)

    if len(ipDomainList)==0:
        print "Please enter ip domain pairs in 'ipDomain' file:"
        return [False,ipDomainList]

    return [True,ipDomainList]

