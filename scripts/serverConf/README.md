Hello,
    This script is for configuring newly installed server to meet our following requirements:

        [1] Packages should be installed:    
            [ apache2, python2.7, libapache2-mod-wsgi, mysql-server, python-mysqldb, python-passlib, python-requests,
                postfix, opendkim, telnetd, libmilter-dev, libssl-dev, openssl]
        
        [2] Configure and set up http (apache2/httpd server with python and mod-wsgi)

        [3] Configure and set up smtp (postfix-esmtp server)

        [4] Configure and set up opendkim for postfix (DomainKeys Identified Mail)
        
        [5] Make entry of ip and domain in /etc/hosts

        [6] Set appropriate hostname to the server

    This are the tasks needed to be done before deployment of software.
    
    So we have provided python script named "serverConf.py".
    Before running the script you should provide IP addresses and Domains in file named "ipDomain" in same directory.
    
    [Example: content of ipDomain]
    =>127.0.0.1  yourdomain.com
    
    Now run [must be run with root priviledges]: sudo python serverConf.py 


    Tree structure of scripts:
    
    .
    ├── data
    │   ├── forum.conf
    │   ├── opendkim.conf
    │   └── packagesToRemove
    ├── ipDomain
    ├── README.md
    ├── scripts
    │   ├── hostsSpfSetup
    │   │   └── hostsSpfSetup.py
    │   ├── ipDomainReader
    │   │   └── ipDomainReader.py
    │   ├── modWSGI
    │   │   └── modWSGI.py
    │   ├── opendkim
    │   │   └── opendkim.py
    │   ├── pkgInstaller
    │   │   └── pkgInstaller.py
    │   ├── pkgRemover
    │   │   └── pkgRemover.py
    │   └── postfix
    │       └── postfix.py
    └── serverConf.py                 [Wrapper script]

