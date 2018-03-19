from maya import cmds
from pymel import core as pm
from maya import mel

def del_int_shapes():
    sel = cmds.ls(sl=True, long=True)

    if not sel:
        shapes = cmds.ls(type="mesh", long=True)
    else:
        shapes = set()
        for object in sel:
            shape = cmds.listRelatives(object, shapes=True, fullPath=True, type="mesh")
            if shape:
                shapes.update(shape)

    for s in shapes:
        if cmds.getAttr(s +".intermediateObject"):
            cmds.delete(s)
            cmds.warning("%s deleted"%s)


def cleanup_mesh():
    sel = pm.ls(sl=True)
    for s in sel:
        pm.select(s)
        pm.polyNormalPerVertex(ufn=True)
        pm.polySoftEdge(a=180)
        mel.eval("FreezeTransformations")
        del_int_shapes()

        pm.delete(s, ch=True)
        pm.setAttr(s + ".tx", k=True, l=False)
        pm.setAttr(s + ".ty", k=True, l=False)
        pm.setAttr(s + ".tz", k=True, l=False)
        pm.setAttr(s + ".rx", k=True, l=False)
        pm.setAttr(s + ".ry", k=True, l=False)
        pm.setAttr(s + ".rz", k=True, l=False)
        pm.setAttr(s + ".sx", k=True, l=False)
        pm.setAttr(s + ".sy", k=True, l=False)
        pm.setAttr(s + ".sz", k=True, l=False)
        pm.setAttr(s + ".visibility", k=True, l=False)

    pm.select(sel)

