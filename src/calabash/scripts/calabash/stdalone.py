import maya.standalone
import os
import sys

# Start Maya in batch mode
maya.standalone.initialize(name='python')
from maya import cmds

os.environ["PYMEL_SKIP_MEL_INIT"] = "1"
#print os.environ["PYMEL_SKIP_MEL_INIT"]

import pymel.core as pm
import shutil



def load_script():
    print sys.argv[3]

    cmds.workspace(sys.argv[3], o=True)

    cmds.file(sys.argv[1], force=True, open=True, loadAllReferences=True)
    cmds.evalDeferred('print cmds.ls(type="reference")')

    sel_list = sys.argv[2].split(",")
    del sel_list[-1]
    print sel_list
    cmds.select(sel_list)

    from . import fileUtils as fu
    reload(fu)
    fu.publish_vray_rig()
    os.system("pause")


def testRun():
    print "file tested"
    cmds.file(sys.argv[1], force=True, open=True)

    print sys.argv[1]
    cmds.evalDeferred('print cmds.ls(dag=True)')

    os.system("pause")

def publishCurrentFile():

    file_path = os.environ["MAYA_PUB_FILE"]
    sel = os.environ["MAYA_PUB_SEL"]


    # Open the file with the file command
    cmds.file(file_path, force=True, open=True)


    #file_path = cmds.file(sceneName=True, q=True)
    #now = datetime.datetime.now()

    dir, filename = os.path.split(file_path)
    rig_dir = os.path.dirname(dir)
    asset_dir = os.path.dirname(rig_dir)
    dev_dir = os.path.dirname(asset_dir)
    characters_dir = os.path.dirname(dev_dir)

    # rig, character, dev, "Characters"
    basename, ver, ext = filename.split(".")

    non_ver = ".".join((basename, ext))
    non_ver_mb = ".".join((basename, "mb"))

    version_dir = os.path.join(rig_dir, "publish")

    nonvray_dir = os.path.join(characters_dir, "noVray")
    vray_dir = os.path.join(characters_dir, "vray")

    #sel = pm.ls(sl=True)

    if not sel:
        return
    pm.select(sel)
    exp_ma = pm.exportSelected(os.path.join(version_dir, filename), constructionHistory=True, f=True)
    exp_mb = pm.exportSelected(os.path.join(version_dir, filename), type="mayaBinary", constructionHistory=True, f=True)

    print ("Exported: %s, %s" % (exp_ma, exp_mb))

    shutil.copy2(exp_ma, os.path.join(nonvray_dir,non_ver))
    shutil.copy2(exp_mb, os.path.join(nonvray_dir,non_ver_mb))

    if float(cmds.about(v=True)) >= 2017.0:
        maya.standalone.uninitialize()


def publish_vray_rig():
    file_path = os.environ["MAYA_PUB_FILE"]
    sel = os.environ["MAYA_PUB_SEL"]


    # Open the file with the file command
    cmds.file(file_path, force=True, open=True)


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

    vray_dir = os.path.join(characters_dir, "vray")

    #sel = pm.ls(sl=True)

    if not sel:
        cmds.warning("Nothing selected")
        return
    pm.select(sel)
    sel = pm.ls(sl=True)
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
    exp_ma = pm.exportSelected(os.path.join(version_dir, filename), type="mayaAscii", constructionHistory=True, f=True)
    #exp_mb = pm.exportSelected(os.path.join(version_dir, filename), type="mayaBinary", constructionHistory=True, f=True)

    #print ("Exported: %s, %s" % (exp_ma, exp_mb))
    path, file = os.path.split(exp_ma)
    file, ext = os.path.splitext(file)
    shutil.copy2(exp_ma, os.path.join(vray_dir, rbasename + ".ma"))
    #shutil.copy2(exp_mb, os.path.join(vray_dir, rbasename + ".mb"))


def assign_default_shader(file_path):
    # Start Maya in batch mode
    maya.standalone.initialize(name='python')

    cmds= __import__('maya.cmds')
    import pymel.core as pm
    import os
    import shutil


    # Open the file with the file command
    cmds.file(file_path, force=True, open=True)

    # Get all meshes in the scene
    meshes = cmds.ls(type="mesh", long=True)
    for mesh in meshes:
        # Assign the default shader to the mesh by adding the mesh to the
        # default shader set.
        cmds.sets(mesh, edit=True, forceElement='initialShadingGroup')

    # Save the file
    cmds.file(save=True, force=True)

    # Starting Maya 2016, we have to call uninitialize to properly shutdown
    if float(cmds.about(v=True)) >= 2016.0:
        maya.standalone.uninitialize()


