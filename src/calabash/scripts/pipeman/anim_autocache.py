import pymel.core as pm
import maya.cmds as cmds
import os
import re
"""
       
"""
def starPrint(str):
    print '\n*************************************'
    print str
    print '\n*************************************'
def export_anim(scene_name, anim_dir, cache_dir, targets, frame_range):
    try:
        path = os.path.join(anim_dir, current_version(anim_dir, scene_name, 'file_name'))
        frame_start, frame_end = frame_range
        version = scene_name
        pm.openFile(path, f=True)
        print '\n*************************************'
        print pm.sceneName()
        print '\n*************************************'
        for item in targets.keys():
            geogrps = []

            target, target_ns, target_dag = targets[item]
            starPrint('Processing item: {0}'.format(item))
            null = pm.group(name=target_ns + ':null', empty=True)
            exattrs = []

            for d in pm.listRelatives(item, ad=True):
                for attr in pm.listAttr(d, ud=True):
                    if re.match('shd_', attr):
                        exattrs.append(d + '.' + attr)

            starPrint('Extra attributes for {0}: {1}'.format(item, exattrs))

            for exattr in exattrs:
                attrType = pm.getAttr(exattr, type=True)
                # starPrint('exattr: {0}, target_ns: {1}'.format(exattr, target_ns))
                nullattr = 'exattr_' + exattr.replace('.', '__').replace(target_ns + ':', '')
                # starPrint('nullattr: {0}'.format(nullattr))
                pm.addAttr(null, ln=nullattr, type=attrType, k=1)
                pm.connectAttr(exattr, null + '.' + nullattr)

            for child in pm.listRelatives(item, c=True):
                name = child.longName()
                meshes = pm.listRelatives(child, ad=True, type='mesh')
                # starPrint("name: {0}, meshes: {1}".format(name, meshes))

                if meshes:
                    # starPrint('Geo Found!: {0}'.format(name))
                    geogrps.append(name)
                    for mesh in meshes:
                        mesh = pm.PyNode(mesh)
                        # mesh_transform = pm.PyNode(pm.listRelatives(mesh, p=True)[0])
                        if len(mesh.namespaceList()) > 0:
                            if not pm.hasAttr(mesh, 'namespace'):
                                pm.addAttr(mesh, ln='namespace', dt='string')

                            pm.setAttr(mesh.longName() + '.namespace', ':'.join(mesh.namespaceList()))
            pm.addAttr(null, ln='namespace', dt='string')
            pm.setAttr(null.longName() + '.namespace', target_ns)
            # starPrint('namespacelist: {0}'.format(mesh.namespaceList()))
            # starPrint('namespace: {0}'.format(pm.getAttr(mesh + '.namespace')))
            starPrint('null, {0} created with attributes: {1}'.format(null.name(), pm.listAttr(null, ud=True)))
            # starPrint("Geo Groups: {0}".format(geogrps))
            rootstr = '{0} -root {1}'.format(null.longName(), ' -root '.join(geogrps))

            command = '-fr {0} {1}' \
                      ' -uvWrite ' \
                      '-worldSpace ' \
                      '-ro ' \
                      '-sn 0 ' \
                      '-wv ' \
                      '-atp exattr_ -atp namespace ' \
                      '-root {2} -file {3}'.format(frame_start, frame_end, rootstr, os.path.join(cache_dir, '{0}_{1}_cache.{2}.abc'.format(
                target_ns,
                scene_name,
                current_version(anim_dir, scene_name, 'number'))))
            print '\n*************************************'
            print command
            print '\n*************************************'

            cmds.AbcExport(j=command)

            return 0
    except Exception as exception:
        return exception

def current_version(path, scene_name, option):
    existing_files = []

    for scene_file in os.listdir(path):

        if re.search('{0}_[a-z]+.([0-9]+).ma'.format(scene_name), str(scene_file), re.I):
            existing_files.append(scene_file)
    # print existing_files
    if option == 'file_name':
        return sorted(existing_files)[-1]
    elif option == 'number':
        return sorted(existing_files)[-1].split('.')[-2]

def next_version(scene_file):
    current_version = int(scene_file.split('.')[0].split('_')[-1])
    scene_name = scene_file.split('.')[0].rstrip('_%03d' % (current_version))
    next_version = '%03d' % (current_version + 1)
    return '{0}_{1}.ma'.format(scene_name, next_version)

def run(dict_input):
    scene_name = dict_input['scene_name']
    anim_dir = dict_input['anim_dir']
    cache_dir = dict_input['cache_dir']
    targets = dict_input['targets']
    frame_range = dict_input['frame_range']
    export = export_anim(scene_name, anim_dir, cache_dir, targets, frame_range)
    if export:
        print export
    else:
        starPrint('Export successful!')
    raw_input('Press enter to exit')
    #update_anim(scene_name, light_dir, cache_dir, targets)