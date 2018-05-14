import os,sys,getpass

if getpass.getuser()!="root":
    print "Needs root privileges"
    sys.exit()


def bridgeSetup():
    os.system("apt-get install -y bridge-utils dnsmasq ")
    os.system("cp /etc/network/interfaces data/temp")
    os.system("cat data/temp data/bridge > /etc/network/interfaces")
    os.system("rm data/temp")
    os.system("brctl addbr br0")
    os.system("chmod +x data/bridgeInit")
    os.system("cp data/bridgeInit /etc/init.d/")
    os.system("update-rc.d bridgeInit defaults")

bridgeSetup()

#qemu-system-x86_64 -m 2048 -net nic -net bridge,br=br0 -hda minimal_debian1gb.img