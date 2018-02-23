# Utilities for dealing with xgen
from maya import cmds
from maya import mel
import pymel.core as pm
import os
import maya.OpenMayaAnim as oma


def cache_groomableSplines(desc = []):
    mel.eval('ogs -pause;')
    start = int(oma.MAnimControl.minTime().value())
    end = int(oma.MAnimControl.maxTime().value())
    currentFile = cmds.file(location=True, query=True)
    path, file = os.path.split(currentFile)

    fileName, num, ext = file.split(".")

    curProj = cmds.workspace(sn=True, q=True)
    print fileName
    if not os.path.exists(os.path.join(curProj, "cache", "alembic", fileName)):
        os.mkdir(os.path.join(curProj, "cache", "alembic", fileName))


    sel = cmds.ls(sl=True)
    if not desc and sel:
        #shapes = getShapes()

        for s in sel:
            if cmds.xgmSplineQuery(s, isSplineDescription=True):
                desc.append(s)


    if not desc:
        print ("No XGen Descriptions Selected, Caching all in scene")
        desc = cmds.xgmSplineQuery(listSplineDescriptions=True)

    #print desc

    for d in desc:
        cmds.select(d)
        d_short = cmds.ls(d, sn=True)
        d_removeNS = d_short[0].split(":")[-1]
        cache_name = "%s_%s.abc" % (fileName, d_removeNS)

        cache_path = "/".join([curProj, "cache", "alembic", fileName, cache_name])
        #print cache_path

        #mel.eval('xgmSplineCache -create -j -file "Z:/raid/3Dprojects/maya/projects/Pikmi_Pops/data/testCache52.abc" -df ogawa -fr 1 62 -step 1 -obj ANIM:EBB:ebby_feet;')
        #mel.eval('tmXgmSplineCacheExportCmd -create "Z:/raid/3Dprojects/maya/projects/Pikmi_Pops/data/testCache02.abc" 1  10 {"pichiTail"}')
        melCmd = ('tmXgmSplineCacheExportCmd -create "%s" %s %s' % (cache_path, start, end))
        #print melCmd

        mel.eval(melCmd)

    mel.eval('ogs -pause;')
    #repath_caches()

def repath_caches():
    sel = cmds.ls(sl=True, type="xgmSplineCache")
    if not sel:
        caches = cmds.ls(type="xgmSplineCache")
    else:
        caches = sel

    for cache in caches:
        loaded_data = cmds.getAttr("%s.activeDescription"%cache)
        print loaded_data


        val = cmds.getAttr("%s.fileName"%cache)
        valSplit = splitpath(val)
        del valSplit[0]
        print valSplit
        new_path = "\\".join(valSplit)
        #new_path = "FRANCIS\\Users\\tom4p\\Desktop\%s"% valSplit[-1]
        #print new_path

        cmds.setAttr("%s.fileName"%cache, "\\\\%s"%new_path, type="string")
        #cmds.setAttr("%s.fileName"%cache, "\\\\FRANCIS\\Users\\tom4p\\Desktop\%s"% valSplit[-1], type="string")
        #cmds.setAttr("%s.fileName"%cache, val, type="string")
        cmds.setAttr("%s.activeDescription"%cache, loaded_data, type="string")
        print("Repathed %s to %s"%(cache, new_path))

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