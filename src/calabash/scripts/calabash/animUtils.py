import pymel.core as pm
import pymel.mayautils as pu
import os
import re
from PySide2 import QtWidgets
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import increaseVersion
import fileUtils
import shutil

# Convert Ui file from Designer to a python module
# run this in script editor
'''
import sys, pprint
from pyside2uic import compileUi
Ui_File = 'DoItMkr_ui'
scripts_path = "I:\GoogleDrive\Scripts\Pipeline"
pyfile = open("{0}.py".format(os.path.join(scripts_path, Ui_File)), 'w')
compileUi("{0}.ui".format(os.path.join(scripts_path, Ui_File)), pyfile, False, 4,False)
pyfile.close()
'''
# Run this in script editor to open the UI
'''
import sys
scripts_path = "I:\GoogleDrive\Scripts\Pipeline"
sys.path.append(scripts_path)

import DoItMkr as DoIt
reload(DoIt)

'''

# import converted ui file.
from pipeman import anim_autocache_ui as ui_file

reload(ui_file)
scripts_path = os.path.join(pu.getMayaAppDir(), 'modules', 'calabash', 'scripts')


class myGui(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    file_path = pm.system.sceneName()
    animroot, filename = os.path.split(file_path)
    shot_dir = os.path.dirname(animroot)
    #scene_dir = '_'.join(file_path.split('/')[:3])

    shot_name = filename.split('.')[0].replace('_anim', '')
    anim_dir = os.path.join(shot_dir, 'anim')
    cache_dir = os.path.join(shot_dir, 'anim', 'publish', 'cache')
    light_dir = os.path.join(shot_dir, 'render')
    DoIt_fileName = 'autocache_{0}'.format(shot_name)
    DoIt_dir = os.path.join(shot_dir, '{0}.bat'.format(DoIt_fileName))

    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent=parent)

        self.ui = ui_file.Ui_mainUI()
        self.ui.setupUi(self)

        ######## CONNECT UI ELEMENTS AND FUNCTIONS BELOW HERE #########

        self.ui.lineEdit_Path_Anim.setText(self.anim_dir)
        self.ui.lineEdit_Path_DoIt.setText(self.DoIt_dir)
        self.ui.lineEdit_FrameStart.setText(str(int(pm.playbackOptions(q=True, minTime=True))))
        self.ui.lineEdit_FrameEnd.setText(str(int(pm.playbackOptions(q=True, maxTime=True))))

        if os.path.exists(self.cache_dir):
            self.ui.lineEdit_Path_Pub.setText(self.cache_dir)
        else:
            #self.ui.lineEdit_Path_Pub.setText('<No publish folder found>')
            os.mkdir(self.cache_dir)
            self.ui.lineEdit_Path_Pub.setText(self.cache_dir)

        if os.path.exists(self.light_dir):
            self.ui.lineEdit_Path_Light.setText(self.light_dir)
        else:
            self.ui.lineEdit_Path_Light.setText('<No render folder found>')
        self.ui.pushButton_Browse_Anim.clicked.connect(self.set_dir_anim)
        self.ui.pushButton_Browse_Pub.clicked.connect(self.set_dir_pub)
        self.ui.pushButton_Browse_Light.clicked.connect(self.set_dir_light)
        self.ui.pushButton_Browse_DoIt.clicked.connect(self.set_dir_light)
        self.ui.pushButton_AddTargets.clicked.connect(self.add_targets)
        self.ui.pushButton_DoIt.clicked.connect(self.DoIt)

    def set_dir_anim(self):
        anim_dir = pm.windows.promptForFolder()
        self.ui.lineEdit_Path_Anim.setText(anim_dir)

    def set_dir_pub(self):
        cache_dir = pm.windows.promptForFolder()
        self.ui.lineEdit_Path_Pub.setText(cache_dir)

    def set_dir_light(self):
        light_dir = pm.windows.promptForFolder()
        self.ui.lineEdit_Path_Light.setText(light_dir)

    def set_dir_bat(self):
        bat_dir = pm.windows.promptForFolder()
        self.ui.lineEdit_Path_DoIt.setText(bat_dir)

    targets = []

    def add_targets(self):
        self.ui.listWidget_targets.clear()
        sel = pm.ls(sl=1)
        for item in sel:
            self.targets.append(item)
            target_item = QtWidgets.QListWidgetItem(self.ui.listWidget_targets)
            target_item.setText(str(item))

    def DoIt(self):
        def validate(path, scene_name, mode):
            if os.path.exists(path):
                listDir = os.listdir(path)
                for file in listDir:
                    if re.match('{0}_{1}.([0-9]+).ma'.format(scene_name, mode), file):
                        return True
            else:
                return False

        anim = self.ui.lineEdit_Path_Anim.text()
        cache = self.ui.lineEdit_Path_Pub.text()
        light = self.ui.lineEdit_Path_Light.text()
        frame_range = (self.ui.lineEdit_FrameStart.text(), self.ui.lineEdit_FrameEnd.text())
        if not validate(anim, self.shot_name, 'anim'):
            result = pm.confirmDialog(
                title='Invalid Path',
                message='Path not found or no scene files matching {0}?'.format(
                    os.path.join(anim, '{0}_{1}.###.ma'.format(self.shot_name, 'anim'))),
                button=['Close'],
                defaultButton='Close',
                cancelButton='Close',
                dismissString='Close',
            )
            return
        elif not validate(light, self.shot_name, 'render'):
            result = pm.confirmDialog(
                title='Invalid Path',
                message='Path not found or no scene files matching {0}?'.format(os.path.join(light,
                                                                                             '{0}_{1}.([0-9]+).ma'.format(
                                                                                                 self.shot_name,
                                                                                                 'render'))),
                button=['Close'],
                defaultButton='Close',
                cancelButton='Close',
                dismissString='Close',
            )
            return
        DoIt_dict = {
            'scene_name': self.shot_name,
            'anim_dir': anim,
            'cache_dir': cache,
            'light_dir': light,
            'frame_range': frame_range,
            'targets': {
            }
        }

        for target in self.targets:
            target_ns = str(target).split(':')[0]
            DoIt_dict['targets'][str(target)] = target_ns

        DoIt_script = 'import maya.standalone\n' \
                      'maya.standalone.initialize(name="python")\n' \
                      'import sys\n' \
                      'import pymel.mayautils as pu\n' \
                      'scripts_path = os.path.join(pu.getMayaAppDir(), "modules", "calabash", "scripts")\n' \
                      'sys.path.append(scripts_path)\n' \
                      'from pipeman import anim_autocache as anim_autocache\n' \
                      'DoIt_dict = {0}\n' \
                      'anim_autocache.run(DoIt_dict)'.format(DoIt_dict)

        DoIt_bat = '"{0}" "{1}.py"'.format(r"C:\Program Files\Autodesk\Maya2018\bin\mayapy.exe",
                                           os.path.join(self.shot_dir, self.DoIt_fileName))

        if len(self.targets) > 0:

            bat_fileName = '{0}.bat'.format(os.path.join(self.shot_dir, self.DoIt_fileName))
            DoIt_scriptName = '{0}.py'.format(os.path.join(self.shot_dir, self.DoIt_fileName))
            print self.shot_dir, self.DoIt_fileName
            with open(bat_fileName, 'w') as bat_write:
                bat_write.write(DoIt_bat)
                print 'bat write successful!', bat_fileName

            with open(DoIt_scriptName, 'w') as DoIt_scriptWrite:
                DoIt_scriptWrite.write(DoIt_script)
                print 'Script write successful!', DoIt_scriptName
        else:
            print 'No Targets Set!'



    ######## CONNECT UI ELEMENTS AND FUNCTIONS ABOVE HERE #########

    def deleteControl(self, control):
        if pm.workspaceControl(control, q=True, exists=True):
            pm.workspaceControl(control, e=True, close=True)
            pm.deleteUI(control, control=True)

    def run(self):
        # Set Ui's name
        self.setObjectName('Project_tools_ui')
        # Explictly define workspacecontrol name
        workspaceControlName = self.objectName() + 'WorkspaceControl'
        # delete existing controls
        self.deleteControl(workspaceControlName)
        # show as floating window initially, last position and float state is retained between execution
        self.show(dockable=True, floating=True)
        # not sure what e argument means
        pm.workspaceControl(workspaceControlName, e=True, ih=150)

def publishAnim():

    file_path = pm.system.sceneName()
    animroot, filename = os.path.split(file_path)
    # basename, ver, ext = filename.split('.')
    # nonver = '{0}.{1}'.format(basename, ext)
    publish_dir = os.path.join(animroot, 'publish')
    pm.system.saveFile(force=True)
    shutil.copy2(file_path, os.path.join(publish_dir, filename))

    increaseVersion.versionUp()

def ouroboros():
    """
    Ouroboros, the snake that eats its own tail
    """

    # Ouroboros exports a camera from an anim scene, the references it back in

    locdata = fileUtils.get_location()
    assetroot, filename = locdata['assetroot_filename']
    dev_dir = locdata['dev_dir']
    assetname, dept = locdata['assetname_dept']



    def getLatest(path, basename):
        if os.listdir(path):
            for n in os.listdir(path):
                if basename in n:
                    basename, ver, ext = n.split('.')
                    return '%03d' % (int(ver) + 1)
        else:
            return '001'

    exp_basename = "{0}_cam".format(assetname)

    camversion_path = os.path.join(assetroot, 'cam')
    if not os.path.exists(camversion_path):
        os.mkdir(camversion_path)
    camversion = getLatest(camversion_path, exp_basename)
    exp_vname = '{0}.{1}.mb'.format(exp_basename, camversion)
    exp_refname = '{0}.mb'.format(exp_basename)
    cam_vpath = os.path.join(assetroot, 'cam', exp_vname)
    cam_refpath = os.path.join(dev_dir, exp_refname)

    sel = pm.ls(sl=True)
    for node in sel:
        if pm.referenceQuery(node, isNodeReferenced=True):
            print "This is a ref'd node, I'll import it without namespaces, export a version to anim/cams, and then export to shot root"
            refnode = pm.referenceQuery(node, referenceNode=True)
            pm.system.FileReference(refnode).importContents(removeNamespace=True)

            pm.select(clear=True)
            pm.select(node)
            pm.exportSelected(cam_vpath,
                              channels=True,
                              expressions=True,
                              type='mayaBinary'
                              )

            shutil.copy2(cam_vpath, cam_refpath)
            pm.system.createReference(cam_refpath, namespace='CAM')
            pm.delete(node)


        else:
            print "This is a local camera, I'll export it to anim/cams, and to shot root. Then I will reference it in, and delete the local camera"
            pm.select(clear=True)
            pm.select(node)
            pm.exportSelected(cam_vpath,
                              channels=True,
                              expressions=True,
                              type='mayaBinary'
                              )
            shutil.copy2(cam_vpath, cam_refpath)
            pm.system.createReference(cam_refpath, namespace='CAM')
            pm.delete(node)


def next_version(scene_file):
    current_version = int(scene_file.split('.')[0].split('_')[-1])
    scene_name = scene_file.split('.')[0].rstrip('_%03d' % (current_version))
    next_version = '%03d' % (current_version + 1)
    return '{0}_{1}.ma'.format(scene_name, next_version)
myWin = myGui()
