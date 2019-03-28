from maya import cmds
from pymel import core as pm
import re

"""
apply look v2:
select all assets + mtl ref node last
for asset in selection:
    make list of mesh, dagpath tuples
    apply_materials(list of mesh/dagpaths, mtl_refnode)
    get SGs under refnode
    for sg in SGs:
        for mesh in sg.meshes:
            if mesh in assetmeshes[0]:
                apply mesh to sg
                
another possible fix:
add metadata to assetroot node (World),
assetName,

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

def make_assignments(asset_ns, asset_name):

    target_SGs = get_asset_look_SGs(asset_name)
    print 'Making assignments:', asset_name
    print target_SGs
    for SG in target_SGs:
        print SG
        meshes_list = SG.getAttr('meshes').split(", ")
        meshes = []
        print meshes_list
        for n, mesh in enumerate(meshes_list):
            check_name = asset_ns + ':' + mesh
            if pm.objExists(check_name):
                meshes.append(check_name)
        print meshes
        pm.select(clear=True)
        pm.select(meshes)
        pm.hyperShade(assign=SG)

def find_rig_connections(SG):

    controller_pairs = []
    pysg = pm.PyNode(SG)

    all_upstream_nodes = pm.hyperShade(lun=pysg)
    upstream_renderNodes = [node for node in all_upstream_nodes if pm.nodeType(node) in all_render_nodes()]
    if debugMode: print('upstream_renderNodes:', upstream_renderNodes)
    #filter for all transform and expression nodes connected to shader network
    transforms = [node for node in all_upstream_nodes if pm.nodeType(node) == 'transform']
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

    for expression in expressions:

        expression = pm.PyNode(expression)
        controller_pairs.append("expression, {0}, {1}".format(expression ,expression.getExpression()))


    return controller_pairs

def write_connections(SGs):
    for SG in SGs:
        scrubber(SG, 1)
        rig_connections = find_rig_connections(SG)
        cnt = 0
        for connection in rig_connections:
            add_attr(SG, 'control_' + str(cnt), connection)
            cnt+=1

def make_connections(asset_ns, asset_name):
    target_SGs = get_asset_look_SGs(asset_name)

    for SG in target_SGs:
        for attr in SG.listAttr():
            if re.search('control_', str(attr)):
                type, source, destination = pm.getAttr(attr).split(', ')
                if type == 'transform':
                    pm.connectAttr(asset_ns + source, asset_name + '_mtl' + destination)
                if type == 'expression':
                    source.setString(destination)

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
    assets = pm.ls(sl=1)
    for asset in assets:
        if ":" in asset:
            asset_ns = asset.split(":")[0]
            print asset_ns
            asset_name = get_asset_name(asset_ns)

            make_assignments(asset_ns, asset_name)
            make_connections(asset_ns, asset_name)
        else:
            print 'No Namespace found!'


