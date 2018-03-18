from maya import cmds
from pymel import core as pm
from maya import mel

__all__ = [
    'jointDisplay'
    ]

def jointDisplay(show=0):
    jnts = cmds.ls(type="joint")

    if show:
        display = 0
    else:
        display = 2
    for j in jnts:
        cmds.setAttr("%s.drawStyle"%j, display)

def copyTransformColorToShape():
    sel = pm.ls(sl=True)

    # for each object, get color mode, index, and rgb

    # for each object get shapes, for each shape apply settings

    for s in sel:

        type = s.overrideRGBColors.get()
        index = s.overrideColor.get()
        r,g,b = s.overrideColorRGB.get()

        shapes = s.getShapes()
        s.overrideEnabled.set(0)

        for shape in shapes:
            shape.overrideEnabled.set(1)
            shape.overrideRGBColors.set(type)
            shape.overrideColor.set(index)
            shape.overrideColorRGB.set((r, g, b))



