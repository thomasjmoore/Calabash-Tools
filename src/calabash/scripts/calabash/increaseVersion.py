# increaseVersion
# by Thomas Moore

import maya.cmds as cmds
import pymel.core as pm
import os
from maya import mel


def versionUp(*args):
    currentFile = cmds.file(location=True, query=True)
    path, file = os.path.split(currentFile)

    fileNameSplit = file.split(".")
    curVer = fileNameSplit[-2]
    newVer = '%03d' %(int(curVer) + 1)
    newfile = ".".join((fileNameSplit[0], newVer, fileNameSplit[-1]))
    new_file_path = os.path.join(path, newfile)

    ver_exists = False
    if os.path.exists(new_file_path):
        ver_exists = True
    if ver_exists:
        cmds.error("Next version already exists. Action cancelled. Please save manually.")

    save = cmds.confirmDialog(message="Would you like to save the current file before creating new version?",
                              title="Save file?", button=["Save?", "Don't Save", "Cancel"], defaultButton="Save?",
                              cancelButton="Cancel")
    if save == "Save?":
        pm.saveFile(force=True)
    if save =="Cancel":
        return

    pm.saveAs(new_file_path, f=True)

    # that slash replace might not work on mac
    mel.eval('addRecentFile("%s", "mayaAscii")'%(new_file_path.replace("\\","/")))
    return newfile
