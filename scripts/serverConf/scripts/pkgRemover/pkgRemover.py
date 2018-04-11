import os

def removePackages():
    pkgFile=open("data/packagesToRemove","r")
    pkgNames=pkgFile.readlines()
    pkgNames=map(lambda x:x.replace("\n"," "),pkgNames)
    pkgNames=reduce(lambda x,y:x+y,pkgNames)
    pkgNames=pkgNames.split()

    for pkg in pkgNames:
        os.system("apt-get --purge remove -y "+pkg)

    return True

if __name__=="__main__":
    removePackages()
