import os
import platform
import shutil
from maya import cmds
import sys


def install():
    project_name = "calabash"
    package_name = "calabash"
    this_path = os.path.normpath(os.path.dirname(__file__))

    # Cross Platform setup
    if platform.system() == "Darwin":
        home = os.getenv("HOME")
        MAYA_MODULES_INSTALL_PATH="%s/Library/Preferences/Autodesk/maya/modules"%home
        cmds.warning("OSX Installation untested...")

    elif platform.system() == "Linux":
        MAYA_MODULES_INSTALL_PATH = "/usr/autodesk/userconfig/maya/modules"
        cmds.warning("Linux Installation untested...")

    elif platform.system() == "Windows":
        home_dir = os.path.expanduser('~')
        MAYA_MODULES_INSTALL_PATH = "%s/maya/modules" % home_dir

    # Make modules directory if necessary
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

    # check install


    if (os.path.exists("%s%s%s.mod"%(MAYA_MODULES_INSTALL_PATH, os.path.sep,project_name)) and os.path.exists("%s%s%s"%(MAYA_MODULES_INSTALL_PATH, os.path.sep,project_name))):
        communicate("Calabash Tools installed, please restart Maya")
    else:
        communicate("Something went wrong. Manual installation may be required.")

def communicate(message, inScreen = True, color = ''):
    sys.stdout.write(str('\n' + message + '\n'));
    if inScreen == True:
        cmds.inViewMessage(message=message, pos='midCenter', fade=True, fadeStayTime=1500, fadeInTime=250, fadeOutTime=250, backColor = 0x00990000);


def onMayaDroppedPythonFile(obj):
    install()