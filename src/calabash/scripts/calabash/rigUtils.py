from maya import cmds

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