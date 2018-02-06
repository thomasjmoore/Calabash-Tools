from maya import cmds
import pymel.core as pm
import os
import shutil
import zipfile

import datetime



def publishCurrentFile(vray=False, send=False):
    file_path = cmds.file(sceneName=True, q=True)
    now = datetime.datetime.now()

    dir, filename = os.path.split(file_path)
    top_dir = os.path.dirname(dir)

    basename, ver, ext = filename.split(".")

    non_ver = ".".join((basename, ext))

    version_dir = os.path.join(top_dir, "versions", filename)
    nonvray_dir = os.path.join(top_dir, "nonvray", non_ver)
    vray_dir = os.path.join(top_dir, "vray", non_ver)


    sel = pm.ls(sl=True)

    if not sel:
        return

    pm.exportSelected(version_dir)
    pm.exportSelected(nonvray_dir)
    if vray:
        pm.exportSelected(vray_dir)

    if send:
        date = now.strftime("%Y_%m_%d")

        cur_proj = cmds.workspace(fullName = True, q=True)

        clientPath = os.path.join(cur_proj, "TOCLIENT")
        dateFolder = os.path.join(clientPath, date)
        assetFolder = os.path.join(dateFolder, basename)

        if not os.path.exists(clientPath):
            os.mkdir(clientPath)

        if not os.path.exists(dateFolder):
           os.mkdir(dateFolder)

        if not os.path.exists(assetFolder):
            os.mkdir(assetFolder)

        if not os.path.exists(os.path.join(assetFolder, "versions")):
            os.mkdir(os.path.join(assetFolder, "versions"))

        if not os.path.exists(os.path.join(assetFolder, "nonvray")):
            os.mkdir(os.path.join(assetFolder, "nonvray"))

        if not os.path.exists(os.path.join(assetFolder, "vray")):
            os.mkdir(os.path.join(assetFolder, "vray"))

        shutil.copy2(version_dir, os.path.join(assetFolder, "versions"))
        shutil.copy2(nonvray_dir, os.path.join(assetFolder, "nonvray"))
        if vray:
            shutil.copy2(vray_dir, os.path.join(assetFolder, "vray"))


        shutil.make_archive(assetFolder + "_" + ver, 'zip', assetFolder)


def rename_hatch_rigs():
    if cmds.objExists("|Group|Main"):
        cmds.rename("|Group|Main", "Character")

    if cmds.objExists("|Group"):
        cmds.rename("|Group", "World")