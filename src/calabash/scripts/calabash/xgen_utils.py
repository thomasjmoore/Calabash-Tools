# Utilities for dealing with xgen
from maya import cmds
from maya import mel
import pymel.core as pm
import os
import maya.OpenMayaAnim as oma


def cache_groomableSplines(desc=[]):

    start = int(oma.MAnimControl.minTime().value())
    end = int(oma.MAnimControl.maxTime().value())
    relative_sample = 0
    sample_low = 0
    sample_high = 1
    currentFile = cmds.file(location=True, query=True)
    path, file = os.path.split(currentFile)

    fileName, num, ext = file.split(".")

    curProj = cmds.workspace(fn=True, q=True)
    alembic_path = os.path.join(curProj, "cache", "alembic")
    cache_dir = os.path.join(alembic_path, fileName)

    if not os.path.exists(alembic_path):
        os.mkdir(alembic_path)

    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    sel = cmds.ls(sl=True)
    if not desc and sel:
        for s in sel:
            if cmds.xgmSplineQuery(s, isSplineDescription=True):
                desc.append(s)

    if not desc:
        cmds.warning("No XGen Descriptions Selected, Caching all in scene...")
        desc = cmds.xgmSplineQuery(listSplineDescriptions=True)

    if not cmds.ogs(q=True, pause=True):
        cmds.ogs(pause=True)

    for d in desc:
        cmds.select(d)
        d_short = cmds.ls(d, sn=True)
        #d_removeNS = d_short[0].split(":")[-1]
        d_split = d_short[0].split(":")
        d_removeNS = "_".join(d_split)
        cache_name = "%s_%s.abc" % (fileName, d_removeNS)

        cache_path = "/".join([curProj, "cache", "alembic", fileName, cache_name])

        melCmd = ('tmXgmSplineCacheExportCmd -create "%s" %s %s %s %s %s' % (cache_path, start, end, relative_sample, sample_low, sample_high))
        #print melCmd

        mel.eval(melCmd)

    cmds.ogs(pause=True)


def repath_caches():
    repath = cmds.confirmDialog(title="Repath Caches",
                                   message="Repath Caches",
                                   button=["Local", "Renderfarm",    "Cancel"],
                                   defaultButton="Cancel",
                                   cancelButton="Cancel",
                                   dismissString="Cancel")
    if repath == "Cancel":
        cmds.warning("Action canceled")
        return


    sel = cmds.ls(sl=True, type="xgmSplineCache")
    if not sel:
        caches = cmds.ls(type="xgmSplineCache")
    else:
        caches = sel

    if repath == "Renderfarm":
        for cache in caches:
            loaded_data = cmds.getAttr("%s.activeDescription"%cache)
            print loaded_data

            curProj = os.path.basename(cmds.workspace(sn=True, q=True))
            val = cmds.getAttr("%s.fileName"%cache)
            valSplit = splitpath(val)
            del valSplit[0:-4]
            print valSplit
            network_path = r"\raid\3Dprojects\maya\projects"
            combined_path = [network_path] + [curProj] + valSplit
            new_path = "\\".join(combined_path)
            #print new_path

            cmds.setAttr("%s.fileName"%cache, new_path, type="string")
            cmds.setAttr("%s.activeDescription"%cache, loaded_data, type="string")
            print("Repathed %s to %s"%(cache, new_path))

    if repath == "Local":
        for cache in caches:
            loaded_data = cmds.getAttr("%s.activeDescription" % cache)

            curProj = cmds.workspace(fn=True, q=True)
            val = cmds.getAttr("%s.fileName"%cache)
            valSplit = splitpath(val)
            del valSplit[0:-4]

            combined_path = [curProj] + valSplit
            new_path = os.path.join(*combined_path)

            cmds.setAttr("%s.fileName"%cache, new_path, type="string")
            cmds.setAttr("%s.activeDescription" % cache, loaded_data, type="string")
            cmds.warning("Repathed %s to %s" % (cache, new_path))


def getShapes():
    sel = cmds.ls(sl=1, l=1)
    allShapes=set()
    if not sel:
        return
    for s in sel:
        shapes = cmds.listRelatives(s, s=1, ni=1, f=1)
        if not shapes:
            continue
        for shape in shapes:
            allShapes.add(shape)
    return allShapes

def splitpath(path):
    """

    Args:
        path: The path you would like to split

    Returns: List of directories that make the path

    """
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])

            break
        elif parts[1] == path:  # sentinel for relative paths
            allparts.insert(0, parts[1])

            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts