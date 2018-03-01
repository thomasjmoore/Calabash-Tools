#delete intermediate Shapes
from maya import cmds

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
