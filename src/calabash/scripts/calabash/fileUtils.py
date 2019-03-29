from maya import cmds
import pymel.core as pm
import os
import shutil
#import zipfile
#import datetime
import increaseVersion
import shading_utils

__all__ = [
    'publishCurrentFile',
    'rename_hatch_rigs',
    #'publish_vray_rig'
]


def get_location():
    # Returns a dictionary of paths and names for asset dev
    file_path = cmds.file(sceneName=True, q=True)
    assetroot, filename = os.path.split(file_path)
    dept = ('default', assetroot)
    if os.path.split(assetroot)[1] == 'shd':
        shd_path = os.path.dirname(file_path)
        dept = ('shd', shd_path)
        assetroot, throwaway = os.path.split(shd_path)

    publish_dir = os.path.join(assetroot, 'publish')
    dev_dir = os.path.dirname(assetroot)
    type_dir = os.path.dirname(dev_dir)
    basename, ver, ext = filename.split(".")


    return {'file_path': file_path, 'assetroot_filename': (assetroot, filename), 'publish_dir': publish_dir,
            'dev_dir': dev_dir, 'type_dir': type_dir, 'basename_ver_ext': (basename, ver, ext), 'dept':dept}


def getLatest(path, basename):
    versions = []
    if os.listdir(path):
        for n in os.listdir(path):
            if basename in n:
                basename, ver, ext = n.split('.')
                versions.append(ver)
                #return '%03d' % (int(ver) + 1)
        return sorted(versions)[-1]
    else:
        return '001'


def publishCurrentFile():


    debug = True  # False to disable variable printout
    locdata = get_location()
    file_path = locdata['file_path']

    assetroot, filename = locdata['assetroot_filename']
    publish_dir = locdata['publish_dir']

    dev_dir = locdata['dev_dir']
    type_dir = locdata['type_dir']
    dept, deptpath = locdata['dept']
    basename, ver, ext = locdata['basename_ver_ext']

    sel = pm.ls(sl=True)

    if not sel:
        return

    if debug:
        print 'filepath', file_path
        print 'assetroot', assetroot
        print 'publish_dir', publish_dir
        print 'filename', filename
        print 'dev_dir', dev_dir
        print 'Type_dir', type_dir
        print 'basename: {0}, ver: {1} ext: {2}'.format(basename, ver, ext)
        print 'dept:', dept


    # Cleanup unknown nodes
    if pm.ls(type='unknown'):
        print 'Unknown Nodes found, cleaning up...'
        # Source cleanUpScene.mel
        # to make scOpt_performOneCleanup available
        pm.mel.source('cleanUpScene')

        pm.mel.scOpt_performOneCleanup({
            'unknownNodesOption'
        }
        )
    else:
        print 'No Unknown Nodes found...'


    # If in shd scene: define mtl export params, version up, import refs with namespaces,
    # export materials, remove namespaces, export shaded rig, reload current scene to restore references
    if dept == 'shd':
        basename = basename.replace('_shd', '')
        shd_publish = os.path.join(deptpath, 'publish')
        mtl_filename = '{0}_mtl.{1}.mb'.format(basename, ver)
        print '#############'
        print 'export mtl'
        mtl_export_path = os.path.join(shd_publish, mtl_filename)
        print '#############'
        print 'Versioning up: ', increaseVersion.versionUp()


        for node in sel:
            if pm.referenceQuery(node, inr=True):
                refNode = pm.referenceQuery(node, rfn=True)
                fileRef = pm.FileReference(refnode=refNode)
                fileRef.importContents(removeNamespace=True)
        pm.select(sel)
        shading_utils.publish_mtl(mtl_export_path)

        pm.select(sel)
        # for node in sel:
        #     ns, obj = node.split(':')
        #     pm.namespace(rm=str(ns), mnr=True)

        exp_ma = pm.exportSelected(os.path.join(shd_publish, filename),
                                   constructionHistory=True,
                                   channels=True,
                                   constraints=True,
                                   expressions=True,
                                   shader=True,
                                   preserveReferences=True,
                                   type='mayaBinary'
                                   )
        print ("Exported: %s" % (exp_ma))
        revert_path = cmds.file(sceneName=True, q=True)
        print 'Reverting: ', pm.system.openFile(revert_path, force=True)
    else:
        exp_ma = pm.exportSelected(os.path.join(publish_dir, filename),
                                   constructionHistory=True,
                                   channels=True,
                                   constraints=True,
                                   expressions=True,
                                   shader=True,
                                   preserveReferences=True,
                                   type='mayaBinary'
                                   )
        print ("Exported: %s" % (exp_ma))
        print'Versioning up: ', increaseVersion.versionUp()
    #
    # #shutil.copy2(exp_ma, os.path.join(nonvray_dir,non_ver))
    # shutil.copy2(exp_mb, os.path.join(nonvray_dir,non_ver_mb))


def rename_hatch_rigs():
    if cmds.objExists("|Group|Main"):
        cmds.rename("|Group|Main", "Character")

    if cmds.objExists("|Group"):
        cmds.rename("|Group", "World")


# def publish_vray_rig():
#     file_path = cmds.file(sceneName=True, q=True)
#
#     if cmds.file(modified=True, q=True):
#         save = cmds.confirmDialog(title="Scene Unsaved",
#                                   message="Save scene before publishing",
#                                   button=["Save", "Cancel"],
#                                   defaultButton="Save",
#                                   cancelButton="Cancel",
#                                   dismissString="Cancel")
#         if save == "Save":
#             saved_file = pm.saveFile()
#             print("Scene saved")
#         else:
#             cmds.warning("Action canceled")
#             return
#
#     fdir, filename = os.path.split(file_path)
#     rig_dir = os.path.dirname(fdir)
#     asset_dir = os.path.dirname(rig_dir)
#     dev_dir = os.path.dirname(asset_dir)
#     characters_dir = os.path.dirname(dev_dir)
#     # rig, character, dev, "Characters"
#     basename, ver, ext = filename.split(".")
#
#     non_ver = ".".join((basename, ext))
#     non_ver_mb = ".".join((basename, "mb"))
#
#     version_dir = os.path.join(rig_dir, "publish")
#
#     vray_dir = os.path.join(characters_dir, "vray")
#
#     sel = pm.ls(sl=True)
#
#     if not sel:
#         cmds.warning("Nothing selected")
#         return
#     reference = False
#     for s in sel:
#         try:
#             ref_node = pm.referenceQuery(s, referenceNode=True)
#             ref_scene = pm.referenceQuery(s, filename=True, shortName=True)
#             pm.FileReference(ref_node).importContents(removeNamespace=True)
#             rbasename = ref_scene.split(".")[0]
#             reference = True
#             break
#         except:
#             continue
#
#     if not reference:
#         cmds.error("Reference not found")
#         return
#
#     pm.select(sel)
#     #exp_ma = pm.exportSelected(os.path.join(version_dir, filename), type="mayaAscii", constructionHistory=True, f=True)
#     exp_mb = pm.exportSelected(os.path.join(version_dir, filename), type="mayaBinary",
#                                constructionHistory=True,
#                                channels=True,
#                                constraints=True,
#                                expressions=True,
#                                shader=True,
#                                preserveReferences=True,
#                                )
#     print ("Exported: %s" % (exp_mb))
#     #path, file = os.path.split(exp_ma)
#     #file, ext = os.path.splitext(file)
#     #shutil.copy2(exp_ma, os.path.join(vray_dir,rbasename + ".ma"))
#     print vray_dir
#     shutil.copy2(exp_mb, os.path.join(vray_dir,rbasename + ".mb"))
#
#     pm.newFile(f=True)

def publish_groom_rig():
    file_path = cmds.file(sceneName=True, q=True)

    if cmds.file(modified=True, q=True):
        save = cmds.confirmDialog(title="Scene Unsaved",
                                  message="Save scene before publishing",
                                  button=["Save", "Cancel"],
                                  defaultButton="Save",
                                  cancelButton="Cancel",
                                  dismissString="Cancel")
        if save == "Save":
            saved_file = pm.saveFile()
            print("Scene saved")
        else:
            cmds.warning("Action canceled")
            return

    fdir, filename = os.path.split(file_path)
    rig_dir = os.path.dirname(fdir)
    asset_dir = os.path.dirname(rig_dir)
    dev_dir = os.path.dirname(asset_dir)
    characters_dir = os.path.dirname(dev_dir)
    # rig, character, dev, "Characters"
    basename, ver, ext = filename.split(".")

    non_ver = ".".join((basename, ext))
    non_ver_mb = ".".join((basename, "mb"))

    version_dir = os.path.join(rig_dir, "publish")

    groom_dir = os.path.join(characters_dir, "groom")

    sel = pm.ls(sl=True)

    if not sel:
        cmds.warning("Nothing selected")
        return
    reference = False
    for s in sel:
        try:
            ref_node = pm.referenceQuery(s, referenceNode=True)
            ref_scene = pm.referenceQuery(s, filename=True, shortName=True)
            pm.FileReference(ref_node).importContents(removeNamespace=True)
            rbasename = ref_scene.split(".")[0]
            reference = True
            break
        except:
            continue

    if not reference:
        cmds.error("Reference not found")
        return

    pm.select(sel)
    #exp_ma = pm.exportSelected(os.path.join(version_dir, filename), type="mayaAscii", constructionHistory=True, f=True)
    exp_mb = pm.exportSelected(os.path.join(version_dir, filename), type="mayaBinary",
                               constructionHistory=True,
                               channels=True,
                               constraints=True,
                               expressions=True,
                               shader=True,
                               preserveReferences=True,
                               )

    print ("Exported: %s " % (exp_mb))
    #path, file = os.path.split(exp_ma)
    #file, ext = os.path.splitext(file)
    #shutil.copy2(exp_ma, os.path.join(groom_dir, rbasename + ".ma"))
    shutil.copy2(exp_mb, os.path.join(groom_dir, rbasename + ".mb"))

    pm.newFile(f=True)