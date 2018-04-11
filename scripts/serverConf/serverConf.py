#Date: 	 22 March 2018

import os,sys

libPath=["./scripts/pkgRemover/","./scripts/hostsSpfSetup/","./scripts/ipDomainReader/","./scripts/pkgInstaller","./scripts/postfix/","./scripts/opendkim/","./scripts/modWSGI/" , "./scripts/reverseProxy/"]
sys.path+=libPath

import pkgRemover,hostsSpfSetup,ipDomainReader,pkgInstaller,postfix,opendkim,modWSGI,reverseProxy

cwd=os.getcwd()

#Reading Ip Domain pairs from file "ipDomain"
status,ipDomainList=ipDomainReader.readIpDomainFile()

if status==False:
    sys.exit()

#Setting hosts,hostname and generating spf values
hostsSpfStatus,spfVals = hostsSpfSetup.hostsSpfSetup(ipDomainList)


#Removing unnecessary packages
pkgRemover.removePackages()


#Installing needed packages
pkgInstaller.installPackages()

#Postfix config
postfix.postfixConfig(ipDomainList[0][1])

#Configuring opendkim
opendkim.opendkimConfig(cwd,ipDomainList)

#Configuring mod-wsgi
modWSGI.wsgiConfig(ipDomainList[0][1])

#Starting apache2
os.system("service apache2 start")

#Reloading postfix
os.system("postfix reload")

#Starting opendkim
os.system("service opendkim start")

#Check and config if set as reverse proxy
print "Want to use as reverse proxy? (y/N)"
if raw_input().lower() == "y":
    reverseProxy.setup()

print "\n\nDONE!!! Now setup DNS records (A,spf,txt)"
print "\n\nUse following generated SPF values:"
for val in spfVals:
    print val
print "\n\nCheck For DKIM TXT values in /etc/opendkim/keys"

