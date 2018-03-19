from maya import cmds
from pymel import core as pm

def rename_shading_groups():
    # Renames selected shading groups, or all in scene if none are selected

    sel = pm.ls(sl=True)

    sg_sel = False
    sgs = []
    for s in sel:
        if pm.nodeType(s) == "shadingEngine":
            sg_sel = True
            sgs.append(s)

    if not sg_sel:
        cmds.warning("No shading groups selected, renaming all in scene")
        sgs = pm.ls(type="shadingEngine")

    sg_rename_count = 0

    for sg in sgs:
        if sg == "initialShadingGroup" or sg == "initialParticleSE":
            continue

        connections = sg.surfaceShader.listConnections()
        strip_mtl = connections[0].replace("Mtl", "")
        strip_mtl = strip_mtl.replace("_mtl", "")
        sg_name = "%sSG" % strip_mtl
        if not sg == sg_name:
            pm.rename(sg, sg_name)
            sg_rename_count += 1

    cmds.warning("%s shading group(s) were renamed."%sg_rename_count)