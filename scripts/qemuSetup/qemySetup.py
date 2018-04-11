import os,sys,getpass

if getpass.getuser()!="root":
    print "Needs root privileges"
    sys.exit()


def setup():
    os.system("qemu-img create /vserver.img 5G")
    os.system("sudo qemu-system-x86_64 -boot d -cdrom data/debian-9-MyCustom.iso -m 1024 -hda /vserver.img")

setup()
