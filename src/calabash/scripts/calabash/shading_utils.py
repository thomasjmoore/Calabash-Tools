from maya import cmds
from pymel import core as pm
import re

"""
bugs:
if shape node isnt named the same as transform, material app fails
fix: for each shape node connected to SG, get transform node instead

shading switches with shape node inputs are not recorded
fix: add if incommingConnection is type('mesh') check
"""

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

debugMode = False

def all_render_nodes():
    textureNodes = []
    for node in pm.listNodeTypes('texture'):
        textureNodes.append(node)

    for node in pm.listNodeTypes('shader'):
        textureNodes.append(node)

    for node in pm.listNodeTypes('utility'):
        textureNodes.append(node)

    return textureNodes

def get_ShaderGroups(asset):

    SG_set = set()
    pm.select(clear=True)
    pm.select(asset)
    pm.hyperShade(smn=1)
    asset_mtls = pm.ls(sl=1)

    for mtl in asset_mtls:
        SG = pm.ls(mtl.listConnections(), type='shadingEngine')[0]
        SG_set.add(SG)
    return list(SG_set)

def get_asset_name(asset):
    asset_type = asset.split("_")[-1]

    try:
        asset_name = re.sub('_' + asset_type, "", asset)
    except:
        asset_name = asset
    print 'asset_name:', asset_name
    return asset_name

def get_asset_look_SGs(asset_name):
    SGs = pm.ls(type='shadingEngine')
    target_SGs = []
    for SG in SGs:
        if re.search(asset_name + '_mtl', str(SG)):
            target_SGs.append(SG)

    return target_SGs

def scrubber(SG, mode):
    # mode 0 = meshes
    # mode 1 = control_

    allAttr = pm.listAttr(SG)
    pattern_meshes = re.compile('meshes')
    pattern_control = re.compile('control_')
    if mode == 0:
        for attr in allAttr:
            if pattern_meshes.match(attr):
                SG.setAttr(attr, lock=False)
                SG.deleteAttr(attr)
    if mode == 1:

        for attr in allAttr:
            if pattern_control.match(attr):
                SG.setAttr(attr, lock=False)
                SG.deleteAttr(attr)

def add_attr(node, attr, value):
    if not pm.hasAttr(node, attr):
        pm.addAttr(node, longName=attr, dataType='string')

    node.setAttr(attr, lock=False)
    node.setAttr(attr, value, lock=True)

def mk_mesh_list(SG):
    #get list of meshes
    mesh_list = pm.ls(SG.listConnections(sh=True), type='mesh')
    #remove namespace
    for n, mesh in enumerate(mesh_list):
        try:
            mesh_list[n] = mesh.split(":")[1]
        except:
            mesh_list[n] = mesh

    #make one long string from list
    meshes = ', '.join([str(x) for x in mesh_list])

    return meshes

def write_assignments(SGs):
    for SG in SGs:
        scrubber(SG, 0)
        add_attr(SG, 'meshes', mk_mesh_list(SG))

def make_assignments(namespace, target_meshes):

    target_SGs = get_asset_look_SGs(namespace)
    print 'Making assignments:', namespace

    for SG in target_SGs:

        meshes_list = SG.getAttr('meshes').split(", ")
        meshes = []

        for n, mesh in enumerate(meshes_list):
            if mesh in target_meshes:
                meshes.append(target_meshes[mesh])

        pm.select(clear=True)
        pm.select(meshes)
        pm.hyperShade(assign=SG)
        print 'Assigned {0} to {1}'.format(SG, meshes)

def find_rig_connections(SG):

    controller_pairs = []
    pysg = pm.PyNode(SG)

    all_upstream_nodes = pm.hyperShade(lun=pysg)
    upstream_renderNodes = [node for node in all_upstream_nodes if pm.nodeType(node) in all_render_nodes()]
    if debugMode: print('upstream_renderNodes:', upstream_renderNodes)
    #filter for all transform and expression nodes connected to shader network
    transforms = [node for node in all_upstream_nodes if pm.nodeType(node) == 'transform']
    shapes = [node for node in all_upstream_nodes if pm.nodeType(node) == 'mesh']
    expressions = [node for node in all_upstream_nodes if pm.nodeType(node) == 'expression']

    for transform in transforms:
        source = pm.PyNode(transform)
        if debugMode: print('source:',source, 'destinations:', source.listConnections(s=0,d=1,p=1))

        for dest in source.listConnections(s=0,d=1,p=1):

            dest = pm.PyNode(dest)
            if debugMode: print('destination:', dest, dest.nodeType())
            #if transform node is going into a render node,
            if dest.nodeType() in all_render_nodes():
                if debugMode: print dest
                try:
                    transformAttr = dest.listConnections(s=1,d=0,p=1)[0].split(':')[1]
                except:
                    transformAttr = dest.listConnections(s=1,d=0,p=1)[0]
                controller_pairs.append("transform, {0}, {1}".format(transformAttr, dest))
                if debugMode: print("transform, {0}, {1}".format(transformAttr, dest))

    for shape in shapes:
        source = pm.PyNode(shape)
        if debugMode: print 'source:', source, 'destinations:', source.listConnections(s=0, d=1, p=1)

        for dest in source.listConnections(s=0, d=1, p=1):

            dest = pm.PyNode(dest)
            if debugMode: print 'source:', source, 'destination:', dest, dest.nodeType()
            # if shape node is going into a render node,
            if dest.nodeType() in all_render_nodes():
                if debugMode: print dest
                try:
                    shapeAttr = dest.listConnections(s=1, d=0, p=1)[0].split(':')[1]
                except:
                    shapeAttr = dest.listConnections(s=1, d=0, p=1)[0]
                controller_pairs.append("shape, {0}, {1}".format(shapeAttr, dest))
                if debugMode: print "shape, {0}, {1}".format(shapeAttr, dest)

    for expression in expressions:

        expression = pm.PyNode(expression)
        controller_pairs.append("expression, {0}, {1}".format(expression ,expression.getExpression()))


    return controller_pairs

def write_connections(SGs):

    for SG in SGs:
        scrubber(SG, 1)
        rig_connections = find_rig_connections(SG)
        if True: print rig_connections
        cnt = 0
        for connection in rig_connections:
            add_attr(SG, 'control_' + str(cnt), connection)
            cnt+=1

def make_connections(namespace, target_curves, meshes):
    target_SGs = get_asset_look_SGs(namespace)
    #print target_curves
    for SG in target_SGs:
        for attr in SG.listAttr():

            if re.search('control_', str(attr)):

                type, source, destination = pm.getAttr(attr).split(', ')
                if ':' in destination:
                    destination = destination.split(':')[-1]
                source_ctl = source.split('.')[0]
                source_attr = source.split('.')[-1]

                for curve in target_curves:

                    if source_ctl in curve:
                        if type == 'transform':
                            #target_curve_noShape = re.sub(r'\|([a-z]+):{0}.([a-z]+)$'.format(curve), '',target_curves[curve], flags=re.IGNORECASE)
                            #print target_curve_noShape
                            print target_curves[curve]
                            target_curve_transform = pm.listRelatives(target_curves[curve], p=True)[0]
                            print target_curve_transform
                            print source_attr
                            print 'Connecting {0} to {1}'.format(target_curve_transform + '.' + source_attr, namespace + '_mtl:' + destination)
                            try:
                                pm.connectAttr(target_curve_transform + '.'+source_attr, namespace + '_mtl:' + destination)
                            except Exception as exception:
                                #     print 'FAILED'
                                print exception

                        if type == 'expression':
                            source.setString(namespace + '_mtl:' + destination)
                if type == 'shape':
                    print 'Connecting {0} to {1}'.format(meshes[source_ctl] + '.' + source_attr,
                                                         namespace + '_mtl:' + destination)
                    try:
                        print meshes
                        pm.connectAttr(meshes[source_ctl] + '.' + source_attr,
                                       namespace + '_mtl:' + destination)
                    except Exception as exception:
                        #     print 'FAILED'
                        print exception

def exportShaders(SGs, export_path):
    network_to_export = []

    for SG in SGs:
        SG = pm.PyNode(SG)
        network_to_export.append(SG)
        upstream_nodes = pm.hyperShade(lun=SG)
        items_to_remove = []

        for node in upstream_nodes:
            if pm.nodeType(node) not in all_render_nodes():
                items_to_remove.append(node)
        if debugMode: print('Removing non-render nodes:', items_to_remove)
        for item in items_to_remove:
            upstream_nodes.remove(item)

        for node in upstream_nodes:
            network_to_export.append(node)

    pm.select(clear=True)
    if debugMode: print('nodes to export:', network_to_export)
    pm.select(clear=True)
    for node in network_to_export:

        pm.select(node, ne=1, add=1)
    asset_name = pm.sceneName().split('/')[-1].split('_')[0]
    print '########################'
    print
    print asset_name
    print export_path
    print
    print '########################'
    expSel = cmds.file(export_path, f=True, es=True, exp=True, ch=False, chn=False, con=False, type='mayaBinary')


def publish_mtl(export_path):

    assets = pm.ls(sl=1)
    for asset in assets:

        sg_to_publish = get_ShaderGroups(asset)

        write_assignments(sg_to_publish)
        write_connections(sg_to_publish)
        exportShaders(sg_to_publish, export_path)


def apply_look():
    sel = pm.ls(sl=1)
    for item in sel:

        meshns_sorted = {}
        curvens_sorted = {}
        for mesh in pm.listRelatives(item, ad=True, type='mesh'):
            mesh = pm.PyNode(mesh)
            #mesh = pm.PyNode(pm.listRelatives(mesh, p=True)[0])
            if pm.hasAttr(mesh, 'namespace'):
                mesh_ns = mesh.getAttr('namespace')
                nodename = mesh.shortName().split(':')[-1]
                if mesh_ns in meshns_sorted:
                    meshns_sorted[mesh_ns][nodename] = mesh.longName()
                else:
                    meshns_sorted[mesh_ns] = {nodename: mesh.longName()}
        for curve in pm.listRelatives(item, ad=True, type='nurbsCurve'):
            curve = pm.PyNode(curve)
            #curve = pm.PyNode(pm.listRelatives(curve, p=True)[0])
            if pm.hasAttr(curve, 'namespace'):
                curve_ns = curve.getAttr('namespace')

                nodename = curve.shortName().split(':')[-1]
                if curve_ns in curvens_sorted:
                    curvens_sorted[curve_ns][nodename] = curve.longName()
                else:
                    curvens_sorted[curve_ns] = {nodename: curve.longName()}
        for namespace in meshns_sorted:
            #print 'Connecting meshes with namespace:', namespace
            target_meshes = meshns_sorted[namespace]
            make_assignments(namespace, target_meshes)

        for namespace in curvens_sorted:
            #print 'Connecting curves with namespace:', namespace
            target_curves = curvens_sorted[namespace]

            make_connections(namespace, target_curves, meshns_sorted[namespace])



