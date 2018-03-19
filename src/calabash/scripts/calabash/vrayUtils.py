# VRAY UTILS

from maya import cmds



def renderSettings():
    cmds.setAttr("vraySettings.samplerType", 4)
    cmds.setAttr("vraySettings.minShadeRate", 2)
    cmds.setAttr("vraySettings.aaFilterType", 1)
    cmds.setAttr("vraySettings.dmcMaxSubdivs", 4)
    cmds.setAttr("vraySettings.dmcs_useLocalSubdivs", 1)
    cmds.setAttr("vraySettings.sys_regsgen_xc", 16)
    cmds.setAttr("vraySettings.sys_regsgen_seqtype", 5)

def giSettings():
    cmds.setAttr("vraySettings.primaryEngine", 0)
    cmds.setAttr("vraySettings.imap_subdivs", 100)
    cmds.setAttr("vraySettings.imap_interpSamples", 40)
    cmds.setAttr("vraySettings.subdivs", 1800)


# Create a Vray Object ID attribute on shape nodes of selected geometry
def makeVrayObjId():
    shapes = getShapes()
    print shapes
    if not shapes:
        return
    for s in shapes:
        print s
        cmds.vray("addAttributesFromGroup", s, "vray_objectID", 1)

# Remove a Vray Object ID attribute on shape nodes of selected geometry
def removeVrayObjId():
    shapes = getShapes()
    print shapes
    if not shapes:
        return
    for s in shapes:
        print s
        cmds.vray("addAttributesFromGroup", s, "vray_objectID", 0)


# Create Vray Subdivision attributes on shape nodes of selected geometry
def makeVraySubdAttr():
    shapes = getShapes()

    if not shapes:
       return

    for s in shapes:
       cmds.vray("addAttributesFromGroup", s, "vray_subdivision", 1)
       cmds.vray("addAttributesFromGroup", s, "vray_subquality", 1)

def makeVrayMatId():
    shadingGrpSet = set()
    shaderSet = set()

    shapes = getShapes()

    if not shapes:
        return

    for s in shapes:
        shadingGrps = cmds.listConnections(s, type='shadingEngine')
        for sg in shadingGrps:
            shadingGrpSet.add(sg)

    for sg in shadingGrpSet:
        shaders = cmds.ls(cmds.listConnections(sg), materials=1)
        for s in shaders:
            shaderSet.add(s)

    for shader in shaderSet:
        cmds.vray("addAttributesFromGroup", s, "vray_material_id", 1)

def displacementControl():
    shapes = getShapes()

    if not shapes:
       return

    for s in shapes:
       cmds.vray("addAttributesFromGroup", s, "vray_displacement", 1)

def single_vop():
    cmds.vray("objectProperties", "add_single")


def primVis():
    sel=cmds.ls(sl=True, l=True)
    vops = getVrayObjProperties(sel)

    for v in vops:
        cmds.editRenderLayerAdjustment("%s.primaryVisibility"% v)
        cmds.setAttr("%s.primaryVisibility"% v, 0)


def matteSurface():
    sel = cmds.ls(sl=True, l=True)
    vops = getVrayObjProperties(sel)

    for v in vops:
        cmds.editRenderLayerAdjustment("%s.matteSurface" % v)
        cmds.editRenderLayerAdjustment("%s.receiveGI" % v)
        cmds.editRenderLayerAdjustment("%s.alphaContribution" % v)
        cmds.editRenderLayerAdjustment("%s.shadowBrightness" % v)
        cmds.editRenderLayerAdjustment("%s.reflectionAmount" % v)
        cmds.editRenderLayerAdjustment("%s.refractionAmount" % v)
        cmds.setAttr("%s.matteSurface" % v, 1)
        cmds.setAttr("%s.receiveGI" % v, 0)
        cmds.setAttr("%s.alphaContribution" % v, -1)
        cmds.setAttr("%s.shadowBrightness" % v, 0)
        cmds.setAttr("%s.reflectionAmount" % v, 0)
        cmds.setAttr("%s.refractionAmount" % v, 0)

# General Utils
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

def getVrayObjProperties(objs=[]):
    if not objs:
        return
    vops = set()
    for o in objs:
        if cmds.objectType(o) == "VRayObjectProperties":
            vops.add(o)
            print "success"
            continue
        vop = cmds.listConnections(o, type="VRayObjectProperties")
        if not vop:
            continue
        for v in vop:
            vops.add(v)

    if not vops:
        cmds.warning("Vray Object Properties node not found")
    return vops