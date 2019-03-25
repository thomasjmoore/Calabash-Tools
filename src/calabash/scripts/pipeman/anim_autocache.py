import pymel.core as pm
import maya.cmds as cmds
import os
import re

def export_anim(scene_name, anim_dir, cache_dir, targets, frame_range):
    path = os.path.join(anim_dir, current_version(anim_dir, scene_name, 'file_name'))
    frame_start, frame_end = frame_range
    version = scene_name
    pm.openFile(path, f=True)
    print '\n*************************************'
    print pm.sceneName()
    print '\n*************************************'
    for target in targets.keys():
        command = '-fr {0} {1}' \
                  ' -uvWrite ' \
                  '-worldSpace ' \
                  '-ro ' \
                  '-sn ' \
                  '-root {2} -file {3}'.format(frame_start, frame_end, target, os.path.join(cache_dir, '{0}_{1}_anim.{2}.abc'.format(
            target.split(':')[0],
			scene_name,
            current_version(anim_dir, scene_name, 'number'))))
        print '\n*************************************'
        print command
        print '\n*************************************'

        cmds.AbcExport(j=command)

def update_anim(scene_name, light_dir, cache_dir, targets):
    light_file = current_version(light_dir, scene_name, 'file_name')
    path = os.path.join(light_dir, light_file)
    pm.openFile(path, f=True)
    try:
        for target in targets:
            target_name = target.split(':')[0]
            target_ref = pm.FileReference(namespace=targets[target])
            target_ver = current_version(cache_dir, target_name, 'file_name')
            abs_path = os.path.join(cache_dir, target_ver)
            rel_path = os.path.join('scenes', re.findall('(?:scenes)(.*)', abs_path)[0].strip('\\'))

            target_ref.replaceWith(rel_path)

            print '\n*************************************'
            print rel_path
            print '\n*************************************'

        pm.saveAs(os.path.join(light_dir, next_version(light_file)))
        print '\n*************************************'
        print 'Versioned up:', os.path.join(light_dir, next_version(light_file))
        print '\n*************************************'

    except:
        finish = raw_input('Something happened, Press enter to close')

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
    light_dir = dict_input['light_dir']
    targets = dict_input['targets']
    frame_range = dict_input['frame_range']
    export_anim(scene_name, anim_dir, cache_dir, targets, frame_range)
    #update_anim(scene_name, light_dir, cache_dir, targets)