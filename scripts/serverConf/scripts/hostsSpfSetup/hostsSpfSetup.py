import os

def hostsSpfSetup(ipDomainList):
    spfVals=[]

    try:
        hosts=open("/etc/hosts","a")
        for rec in ipDomainList:
            hosts.writelines(rec[0]+" "+rec[1]+"\n")
            spfVals.append("v=spf1 +a +mx +ip4:"+rec[0]+" -all")

        hosts.close()
        #Setting hostname to server
        os.system("hostname "+ipDomainList[0][1])
        return [True,spfVals]

    except:
        return [False,spfVals]


