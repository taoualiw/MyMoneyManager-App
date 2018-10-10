import os
from pathlib import Path
import sys

def get_env():
    sp = sys.path[1].split("/")
    if "envs" in sp:
        return sp[sp.index("envs") + 1]
    else:
        return ""

#=================================
home = str(Path.home())
nameApp = "MyMoneyManager"
pathAppFolder = home+"/Desktop/"
pathApp = pathAppFolder+nameApp
nameEnv = get_env()
pathM = pathApp+"/Contents/MacOs/"
pathR = pathApp+ "/Contents/Resources/"
pathIcon = "images/image.icns"
pathInfo = "resources/Info.plist"
pathExeApp = pathR+"bin/MyMoneyManager"
pathEnv = "~/anaconda/envs/"+nameEnv
pathMyCateg = "resources/myCategDF.csv"
#=================================
def create_AppBundle():
    # Create  Resources directory
    try:
        os.makedirs(pathR);print("Directory " , pathR ,  " Created ")
    except FileExistsError:
        print("Directory " , pathR ,  " already exists")
    #copy anaconda env folders  to Resources folder
    os.system("cp -R "+pathEnv+"/* "+pathR)
    # copy Icon file to Resources folder
    os.system("cp -R "+pathIcon+" "+ pathR)
    # copy Info.plist file to Resources folder
    os.system("cp -R "+pathInfo+" "+pathApp+"/Contents/")
    # Create  MacOS directory
    try:
        os.makedirs(pathM)
        print("Directory " , pathM ,  " Created ")
    except FileExistsError:
        print("Directory " , pathM ,  " already exists")
    # copy myCateg.csv to Resources folder
    os.system("cp -R "+pathMyCateg+" "+pathR)
    # copy excutable app file from Resources to MacOS folder
    os.system("cp -R "+pathExeApp+" "+pathM)
    # convert folder to .app bundle
    os.system("mv "+pathApp+" "+pathApp+".app")
    # touch to activate icon
    os.system("touch "+pathApp+".app")
    #os.system("touch "+pathR+"Info.plist;killall Dock")


if __name__=="__main__":
    print("Create a Standalone Local App in "+pathAppFolder)
    print("Only tested with MacOS Sierra 10.12.6")
    print("--------------")
    try:
        create_AppBundle()
        print("App created !");

    except PermissionError:
        print("Needs admin rights: try 'sudo python create_AppBundle.py'")
