import os
import platform
import shutil
from maya import cmds

# find path to this file

# find maya module path
# make sure it is cross platform
# make modules folder if doesn't exist

# uninstall
# copy


def install():
    project_name = "calabash"
    package_name = "calabash"
    this_path = os.path.normpath(os.path.dirname(__file__))

    if platform.system() == "Darwin":
        # MAYA_MODULES_INSTALL_PATH="$HOME/Library/Preferences/Autodesk/maya/modules"
        pass

    elif platform.system() == "Linux":
        MAYA_MODULES_INSTALL_PATH = "/usr/autodesk/userconfig/maya/modules"

    elif platform.system() == "Windows":
        home_dir = os.path.expanduser('~')
        MAYA_MODULES_INSTALL_PATH = "%s/maya/modules" % home_dir

    if not os.path.exists(MAYA_MODULES_INSTALL_PATH):
        print MAYA_MODULES_INSTALL_PATH
        os.mkdir(MAYA_MODULES_INSTALL_PATH)

    project_path = os.path.join(this_path, "src")

    # uninstall
    if os.path.exists("%s%s%s.mod"%(MAYA_MODULES_INSTALL_PATH, os.path.sep,project_name)):
        os.remove("%s%s%s.mod"%(MAYA_MODULES_INSTALL_PATH, os.path.sep,project_name))

    if os.path.exists("%s%s%s"%(MAYA_MODULES_INSTALL_PATH, os.path.sep,project_name)):
        shutil.rmtree("%s%s%s"%(MAYA_MODULES_INSTALL_PATH, os.path.sep,project_name))
    
    # install
    shutil.copy2("%s%s%s.mod"%(project_path, os.path.sep,project_name), "%s%s%s.mod"%(MAYA_MODULES_INSTALL_PATH, os.path.sep,project_name))
    shutil.copytree("%s%s%s"%(project_path, os.path.sep,project_name), "%s%s%s"%(MAYA_MODULES_INSTALL_PATH, os.path.sep,project_name))



def onMayaDroppedPythonFile(obj):
    install()