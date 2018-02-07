# increaseVersion
# by Thomas Moore

import maya.cmds as cmds
import pymel.core as pm
import os


def versionUp(*args):
    currentFile = cmds.file(location=True, query=True)
    path, file = os.path.split(currentFile)

    fileNameSplit = file.split(".")
    curVer = fileNameSplit[-2]
    newVer = '%03d' %(int(curVer) + 1)
    newfile = ".".join((fileNameSplit[0], newVer, fileNameSplit[-1]))

    save = cmds.confirmDialog(message="Would you like to save the current file before creating new version?",
                              title="Save file?", button=["Save?", "Don't Save", "Cancel"], defaultButton="Save?",
                              cancelButton="Cancel")
    if save == "Save?":
        pm.saveFile(force=True)
    if save =="Cancel":
        return
    pm.saveAs(os.path.join(path, newfile), f=True)

    return newfile
