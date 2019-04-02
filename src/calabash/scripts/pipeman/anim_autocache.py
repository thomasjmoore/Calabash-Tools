import pymel.core as pm
import maya.cmds as cmds
import os
import re
"""
       
"""
def export_anim(scene_name, anim_dir, cache_dir, targets, frame_range):
    path = os.path.join(anim_dir, current_version(anim_dir, scene_name, 'file_name'))
    frame_start, frame_end = frame_range
    version = scene_name
    pm.openFile(path, f=True)
    print '\n*************************************'
    print pm.sceneName()
    print '\n*************************************'
    for item in targets.keys():

        target, target_ns, target_dag = targets[item]

        for item in targets:
            for mesh in pm.listRelatives(item, ad=True, type=['mesh', 'nurbsCurve']):
                mesh = pm.PyNode(mesh)
                #mesh_transform = pm.PyNode(pm.listRelatives(mesh, p=True)[0])
                if len(mesh.namespaceList()) > 0:
                    if not pm.hasAttr(mesh, 'namespace'):
                        pm.addAttr(mesh, ln='namespace', dt='string')

                    pm.setAttr(mesh.longName() + '.namespace', ':'.join(mesh.namespaceList()))

        command = '-fr {0} {1}' \
                  ' -uvWrite ' \
                  '-worldSpace ' \
                  '-ro ' \
                  '-sn 0 ' \
                  '-wv ' \
                  '-attr color -attr Color -attr namespace -attr material -attr Material ' \
                  '-root {2} -file {3}'.format(frame_start, frame_end, target_dag, os.path.join(cache_dir, '{0}_{1}_anim.{2}.abc'.format(
            target_ns,
			scene_name,
            current_version(anim_dir, scene_name, 'number'))))
        print '\n*************************************'
        print command
        print '\n*************************************'

        cmds.AbcExport(j=command)

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
    export_anim(scene_name, anim_dir, cache_dir, targets, frame_range)
    #update_anim(scene_name, light_dir, cache_dir, targets)