import pymel.core as pm
import maya.mel as mel
from PySide2 import QtCore, QtUiTools, QtWidgets
from PySide2.QtGui import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as apiUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQDockWidget
import os
import json
import shutil
import re
from collections import defaultdict



#Convert Ui file from Designer to a python module
# run this in script editor
'''
import sys, pprint, os
from pyside2uic import compileUi
Ui_File = 'ui_file' #No Extension
userpath = os.path.expanduser('~')
scripts_path = "{0}/maya/modules/calabash/scripts/pipeman".format(userpath)
pyfile = open("{0}.py".format(os.path.join(scripts_path, Ui_File)), 'w')
compileUi("{0}.ui".format(os.path.join(scripts_path, Ui_File)), pyfile, False, 4,False)
pyfile.close()
'''
#Run this in script editor to open the UI
'''
src = r'path to gui module'
import sys
sys.path.append(src)

import <module> as blah
reload(blah)
'''

"""
Wishlist:
Make all latest live button
make multiple cache files live
    (compare basenames)

"""

#import converted ui file.
import pipeman_ui as ui_file
import refEdit
import arborist
from calabash import fileUtils
reload(ui_file)
reload(refEdit)
reload(arborist)
reload(fileUtils)
debug = False
class myGui(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent=parent)

        self.ui = ui_file.Ui_mainUI()
        self.ui.setupUi(self)

        self.proj_path = pm.workspace.getPath()
        self.proj_root = os.path.dirname(self.proj_path)
        self.ui.lineEdit_arb_projPath.setText(self.proj_path)
        self.comproot = ''
        self.scenes_root = os.path.join(self.proj_path, 'scenes')
        self.images_root = os.path.join(self.proj_path, 'images')
        self.spots = self.getSpots()
        self.assets_root = os.path.join(self.scenes_root, 'assets')
        self.status_path = os.path.join(self.scenes_root, 'status.json')

        #self.setProject()
        self.apivers = pm.about(api=True)
        self.mayaDir = str(self.apivers)[:4]
        self.pmprefs = os.path.expanduser('~/maya/{0}/prefs/pipeman'.format(self.mayaDir))
        self.userstate = os.path.join(self.pmprefs, 'userstate.json')
        self.popmayaproj()
        self.gondo_popshots()

        if not os.path.isfile(self.status_path):
            self.make_statusfile(self.status_path)
        if os.path.isfile(self.userstate):
            self.restorestate()
        else:
            self.make_userstate(self.userstate)
        #self.make_userstate(self.userstate)

        #self.ui.tabWidget_pipeman.setCurrentIndex(0)
        #self.ui.lineEdit_arb_projPath.setText("Z:/raid/3Dprojects/maya/projects")

        ######## CONNECT UI ELEMENTS AND FUNCTIONS BELOW HERE #########

        self.header_assets = self.ui.treeWidget_versions.header()
        self.header_assets.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.header_assets.setStretchLastSection(False)
        self.header_assets.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.header_anim = self.ui.treeWidget_animVersions.header()
        self.header_anim.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.header_anim.setStretchLastSection(False)
        self.header_anim.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        if os.path.exists(self.assets_root):
            self.pop_assetlist()
            self.pop_shotlist()
        self.ui.treeWidget_assets.itemClicked.connect(self.pop_assetVersions)
        self.ui.treeWidget_versions.itemClicked.connect(self.showcomment_asset)
        self.ui.listWidget_shots.itemClicked.connect(self.pop_shotVersions)
        self.ui.pushButton_makelive.clicked.connect(self.makelive_assets)

        self.ui.pushButton_makelive.customContextMenuRequested.connect(self.on_context_menu)
        self.popMenu_assetlive = QtWidgets.QMenu(self)
        self.popMenu_assetlive.addAction(QtWidgets.QAction('Make all latest Live', self))
        self.popMenu_assetlive.triggered.connect(self.makelive_assets_all)

        self.ui.comboBox_mayaproject.customContextMenuRequested.connect(self.on_context_maya)
        self.popMenu_maya = QtWidgets.QMenu(self)
        self.popMenu_maya.addAction(QtWidgets.QAction('Set Maya projects location', self))
        self.popMenu_maya.triggered.connect(self.set_mayaroot)

        self.ui.comboBox_gondo_compproject.customContextMenuRequested.connect(self.on_context_comp)
        self.popMenu_gcomp = QtWidgets.QMenu(self)
        self.popMenu_gcomp.addAction(QtWidgets.QAction('Set Comp projects location', self))
        self.popMenu_gcomp.triggered.connect(self.set_comproot)

        self.ui.pushButton_anim_makelive.clicked.connect(self.makelive_shots)
        self.ui.pushButton_anim_openlatest.clicked.connect(self.open_latest_shot)
        self.ui.pushButton_asset_openlatest.clicked.connect(self.open_latest_asset)
        self.ui.pushButton_arb_exe.clicked.connect(self.run_arborist)
        self.ui.pushButton_arb_projBrowse.clicked.connect(self.setarbProj)

        self.ui.pushButton_gondo_copy.clicked.connect(self.gcopy)
        self.ui.pushButton_gondo_setlinks.clicked.connect(self.open_linksUI)

        self.ui.comboBox_mayaproject.currentIndexChanged.connect(self.mayaproj_changed)
        self.ui.comboBox_gondo_compproject.currentIndexChanged.connect(self.savestate)

        self.ui.listWidget_gondo_shots.currentItemChanged.connect(self.gondo_poplayers)
        self.ui.listWidget_gondo_layers.itemClicked.connect(self.gondo_popversions)

        self.ui.treeWidget_gondo_versions.customContextMenuRequested.connect(self.on_context_gversions)
        self.popMenu_gversions = QtWidgets.QMenu(self)
        self.addToCopy = QtWidgets.QAction('Add to Copy List', self)
        self.addToCopy.triggered.connect(self.addversion_selected)
        self.copyMissing = QtWidgets.QAction('Show missing frames', self)
        self.copyMissing.triggered.connect(self.showMissingframes)
        self.popMenu_gversions.addAction(self.addToCopy)
        self.popMenu_gversions.addAction(self.copyMissing)

        self.ui.listWidget_gondo_copylist.customContextMenuRequested.connect(self.on_context_copylist)
        self.popMenu_copylist = QtWidgets.QMenu(self)
        self.popMenu_copylist.addAction(QtWidgets.QAction('Remove', self))
        self.popMenu_copylist.triggered.connect(self.removeCommand)

        self.ui.listWidget_gondo_layers.customContextMenuRequested.connect(self.on_context_glayers)
        self.popMenu_glayers = QtWidgets.QMenu(self)
        self.popMenu_glayers.addAction(QtWidgets.QAction('Add latest to Copy List', self))
        self.popMenu_glayers.triggered.connect(self.addversion_latest)

        self.ui.tabWidget_pipeman.currentChanged.connect(self.savestate)
        self.ui.lineEdit_arb_projPath.textChanged.connect(self.savestate)

    def mayaproj_changed(self):
        self.setProject()
        self.pop_shotlist()
        self.pop_assetlist()
        self.gondo_popshots()
        self.savestate()
        self.restorestate()

    def open_linksUI(self):
        import gondo_link as glink
        reload(glink)
        with open(self.userstate, 'r') as f:
            userstate = json.load(f)
        shots = []
        shotdict = self.getShots()
        for spot in shotdict:
            for shot in shotdict[spot]:
                shotname = spot + '/' + shot
                shots.append(shotname)
        comp_proj = self.ui.comboBox_gondo_compproject.currentText()
        comp_root = userstate["gondo_comproot"]
        glink_gui = glink.myGui(sorted(shots), comp_root, comp_proj, self.status_path)
        glink_gui.run()

    def setProject(self):
        curProj_index = self.ui.comboBox_mayaproject.currentIndex()
        curProj_text = self.ui.comboBox_mayaproject.itemText(curProj_index)
        if debug: print "curProj_index:", curProj_index
        if curProj_text:
            targetProj = os.path.join(self.proj_root, curProj_text).replace('\\','/')
            print 'Setting Project to: {0}'.format(targetProj)
            mel.eval('setProject \"' + targetProj + '\"')
            self.proj_path = pm.workspace.getPath()
            self.proj_root = os.path.dirname(self.proj_path)
            self.ui.lineEdit_arb_projPath.setText(self.proj_path)
            self.scenes_root = os.path.join(self.proj_path, 'scenes')
            self.images_root = os.path.join(self.proj_path, 'images')
            self.spots = self.getSpots()
            self.assets_root = os.path.join(self.scenes_root, 'assets')
            self.status_path = os.path.join(self.scenes_root, 'status.json')
        else:
            print 'Select A Project'

    def set_mayaroot(self):
        mayaroot = pm.windows.promptForFolder()
        self.proj_root = mayaroot
        print self.proj_root
        self.savestate()
        self.popmayaproj()

    def set_comproot(self):
        comproot = pm.windows.promptForFolder()
        print comproot
        self.comproot = comproot
        self.savestate()
        self.gondo_popcompproj()

    def make_userstate(self, userstate):
        if not os.path.exists(self.pmprefs):
            os.makedirs(self.pmprefs)
        with open(userstate, 'w') as f:
            defaults = {
                'tabIndex':0,
                'arb_projPath':'',
                'gondo_current_mpindex':-1,
                'gondo_current_mptext':'',
                'gondo_comproot':'',
                'gondo_current_cpindex':-1,
                'gondo_current_cptext':'',
                'arb_projPath':''
            }
            json.dump(defaults, f, indent=4)

    def savestate(self):
        if debug: print 'Saving State'
        tabIndex = self.ui.tabWidget_pipeman.currentIndex()
        arb_projPath = self.ui.lineEdit_arb_projPath.text()
        gondo_current_mpindex = self.ui.comboBox_mayaproject.currentIndex()
        gondo_current_mptext = self.ui.comboBox_mayaproject.itemText(gondo_current_mpindex)
        gondo_current_cpindex = self.ui.comboBox_gondo_compproject.currentIndex()
        gondo_current_cptext = self.ui.comboBox_gondo_compproject.itemText(gondo_current_cpindex)

        with open(self.userstate, 'r') as f:
            userstate = json.load(f)
        userstate['tabIndex'] = tabIndex
        userstate['arb_projPath'] = arb_projPath
        userstate['gondo_current_mpindex'] = gondo_current_mpindex
        userstate['gondo_current_mptext'] = gondo_current_mptext
        userstate['gondo_comproot'] = self.comproot
        userstate['gondo_current_cpindex'] = gondo_current_cpindex
        userstate['gondo_current_cptext'] = gondo_current_cptext
        userstate['arb_projPath'] = self.ui.lineEdit_arb_projPath.text()
        with open(self.userstate, 'w') as f:
            json.dump(userstate, f, indent=4)

    def restorestate(self):
        if debug: print 'Restoring State'
        with open(self.userstate, 'r') as f:
            userstate = json.load(f)
            self.ui.tabWidget_pipeman.setCurrentIndex(userstate['tabIndex'])
            self.ui.lineEdit_arb_projPath.setText(userstate['arb_projPath'])
            current_gmpText = self.ui.comboBox_mayaproject.itemText(userstate['gondo_current_mpindex'])
            if current_gmpText == userstate['gondo_current_mptext']:
                self.ui.comboBox_mayaproject.setCurrentIndex(userstate['gondo_current_mpindex'])
            else:
                print 'Saved project does not match current index, setting to None'
            self.comproot = userstate['gondo_comproot']
            self.gondo_popcompproj()
            current_cmpText = self.ui.comboBox_gondo_compproject.itemText(userstate['gondo_current_cpindex'])
            comp_loopstate = True

            for index in range(self.ui.comboBox_gondo_compproject.count()):
                if current_gmpText.lower() == self.ui.comboBox_gondo_compproject.itemText(index).lower():
                    self.ui.comboBox_gondo_compproject.setCurrentIndex(index)
                    comp_loopstate = False
                    break
            if comp_loopstate:
                if current_cmpText == userstate['gondo_current_cptext']:
                    self.ui.comboBox_gondo_compproject.setCurrentIndex(userstate['gondo_current_cpindex'])
                else:
                    print 'Current_cmpText: {0}, userstate: {1}'.format(current_cmpText,
                                                                        userstate['gondo_current_cptext'])
                    print 'Saved project does not match current index, setting to None'

    def popmayaproj(self):
        self.ui.comboBox_mayaproject.clear()
        projects = []
        for project in os.listdir(self.proj_root):
            if not re.match('\.', project):
                projects.append(project)
        self.ui.comboBox_mayaproject.addItem('')
        self.ui.comboBox_mayaproject.addItems(sorted(projects))

    def getCompprojects(self):
        if self.comproot:
            compprojects = []
            for project in os.listdir(self.comproot):
                if not re.match('\.', project):
                    compprojects.append(project)
            return compprojects
        else:
            return []

    def gondo_popcompproj(self):
        if debug: print 'Populating comp project list with root:', self.comproot
        self.ui.comboBox_gondo_compproject.addItem('')
        self.ui.comboBox_gondo_compproject.addItems(sorted(self.getCompprojects()))

    def getRenDirs(self):
        debug = False
        imageDict = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
        shotlist = []
        for dir in os.listdir(self.images_root):
            dirpath = os.path.join(self.images_root, dir)
            if self.isSpot(dirpath):
                for subdir in os.listdir(dirpath):
                    if re.match('sh[0-9]+', subdir):
                        subdirpath = os.path.join(dirpath, subdir)
                        if os.path.isdir(subdirpath):
                           shotlist.append((dir + '/' + subdir, subdirpath))
            elif re.match('sh[0-9]+', dir):
                if os.path.isdir(dirpath):
                    shotlist.append((dir, dirpath))
            else:
                pass
        for shot, shotdir in shotlist:
            for versiondir in os.listdir(shotdir):
                versionpath = os.path.join(shotdir, versiondir)
                verNum = versiondir.split('.')[-1]
                if os.path.isdir(versionpath):
                    for layer in os.listdir(versionpath):
                        layerpath = os.path.join(versionpath, layer)
                        imageDict[shot][layer][verNum] = layerpath
        if debug: print(json.dumps(imageDict, indent=4))
        return imageDict

    def gondo_popshots(self):
        debug = False
        if debug: print 'Populating images shot list for project:', self.proj_path
        self.ui.listWidget_gondo_shots.clear()
        gshots = self.getRenDirs().keys()
        if debug: print gshots
        for shot in gshots:
            shot_item = QtWidgets.QListWidgetItem(self.ui.listWidget_gondo_shots)
            shot_item.setText(shot)

    def gondo_poplayers(self):
        debug = False
        self.ui.listWidget_gondo_layers.clear()
        sel_shot = self.ui.listWidget_gondo_shots.currentItem().text()
        glayers = self.getRenDirs()[sel_shot]
        if debug: print sel_shot
        if debug: print json.dumps(glayers, indent=4)

        for layer in glayers.keys():
            layer_item = QtWidgets.QListWidgetItem(self.ui.listWidget_gondo_layers)
            layer_item.setText(layer)

    def gondo_popversions(self):
        debug = True
        self.ui.treeWidget_gondo_versions.clear()
        selected_shot = self.ui.listWidget_gondo_shots.currentItem().text()
        selected_layers = self.ui.listWidget_gondo_layers.selectedItems()
        if len(selected_layers) == 1:
            layer = selected_layers[0].text()
            for vers in self.getRenDirs()[selected_shot][layer]:
                vers_path = self.getRenDirs()[selected_shot][layer][vers]
                vers_item = QtWidgets.QTreeWidgetItem()
                vers_item.setText(0, vers)
                vers_item.setText(1, self.seqRange(vers_path))
                if self.listMissingframes(vers_path):
                    vers_item.setForeground(1, QBrush(QColor("red")))
                self.ui.treeWidget_gondo_versions.addTopLevelItem(vers_item)
            self.ui.treeWidget_gondo_versions.setSortingEnabled(True)
            #elf.ui.treeWidget_gondo_versions.sortItems(0)

    def seqRange(self, path):
        seq = os.listdir(path)
        seq_start = sorted(seq)[0].split('.')[-2]
        seq_end = sorted(seq)[-1].split('.')[-2]
        return('{0}-{1}'.format(seq_start, seq_end))

    def missingFrames(self, path):
        seq = os.listdir(path)
        seq_len = len(seq)
        seq_start = int(sorted(seq)[0].split('.')[-2])
        seq_end = int(sorted(seq)[-1].split('.')[-2])
        if seq_end - seq_start == seq_len -1:
            return False
        else:
            return True

    def showMissingframes(self):
        selected_version = self.ui.treeWidget_gondo_versions.currentItem().text(0)
        selected_shot = self.ui.listWidget_gondo_shots.currentItem().text()
        selected_layer = self.ui.listWidget_gondo_layers.currentItem().text()
        src = self.getRenDirs()[selected_shot][selected_layer][selected_version]
        result = pm.promptDialog(
            title='Missing frames',
            message='Sequence: {0}_{1}_{2}'.format(selected_shot, selected_layer, selected_version),
            text=self.listMissingframes(src),
        )

        if result:
            pass

    def listMissingframes(self, path):
        seq = [x.split('.')[-2] for x in os.listdir(path)]
        int_seq = [int(x) for x in seq]
        full_int_seq = [x for x in range(int_seq[0], int_seq[-1] + 1)]
        int_seq = set(int_seq)
        str_seq = [str(x) for x in list(int_seq ^ set(full_int_seq))]
        return ','.join(str_seq)

    def getDest(self, shot, layer):
        with open(self.status_path, 'r') as r:
            status = json.load(r)
        shotroot = status['complinks'][shot]
        return os.path.join(shotroot, layer)

    def addversion_selected(self):
        debug = True
        selected_version = self.ui.treeWidget_gondo_versions.currentItem().text(0)
        selected_shot = self.ui.listWidget_gondo_shots.currentItem().text()
        selected_layer = self.ui.listWidget_gondo_layers.currentItem().text()
        src = self.getRenDirs()[selected_shot][selected_layer][selected_version]
        dest = self.getDest(selected_shot, selected_layer)
        self.addCommand(src, dest)

    def addversion_latest(self):
        selected_shot = self.ui.listWidget_gondo_shots.currentItem().text()
        selected_layers = self.ui.listWidget_gondo_layers.selectedItems()


        for item in selected_layers:
            layer = item.text()
            dest = self.getDest(selected_shot, layer)
            latest_ver = sorted(self.getRenDirs()[selected_shot][layer].keys())[-1]
            src = self.getRenDirs()[selected_shot][layer][latest_ver]
            self.addCommand(src, dest)

    def addCommand(self, src, dest):
        command = '{0} >>> {1})'.format(src, dest)
        copy_item = QtWidgets.QListWidgetItem(self.ui.listWidget_gondo_copylist)
        copy_item.setFlags(copy_item.flags() | QtCore.Qt.ItemIsEditable)
        copy_item.setText(command)

    def removeCommand(self):
        selected_commands = self.ui.listWidget_gondo_copylist.selectedItems()
        for item in selected_commands:
            row = self.ui.listWidget_gondo_copylist.row(item)
            self.ui.listWidget_gondo_copylist.takeItem(row)

    def gcopy(self):
        def progress(copied, filecnt):
            percentage = int(float(copied) / float(filecnt) * 100)

            return percentage

        def copydone(fsrc, fdst, copied):
            print 'Done!'
            print 'Copied {0} files from: \n Source: {1} \n Destination: {2}'.format(copied, fsrc, fdst)

        def copyseq(src, dst):
            if not os.path.exists(dst):
                os.makedirs(dst)
            filecnt = len(os.listdir(src))
            prog_cnt = 0
            for n, file in enumerate(os.listdir(src)):
                prog_cnt += 1
                filepath = os.path.join(src, file)
                shutil.copy2(filepath, dst)
                percentage = progress(n, filecnt)
                if prog_cnt == 5:
                    print 'Progress = {0}%'.format(percentage)
                    prog_cnt = 0
            copydone(src, dst, filecnt)
        copylist_cnt = self.ui.listWidget_gondo_copylist.count()
        commandlist = []
        for n in range(copylist_cnt):
            command = self.ui.listWidget_gondo_copylist.item(n).text()
            commandlist.append(command)
        for command in commandlist:
            src, dst = command.split(' >>> ')
            copyseq(src, dst)

    def on_context_maya(self, point):
        self.popMenu_maya.exec_(self.ui.comboBox_mayaproject.mapToGlobal(point))

    def on_context_comp(self, point):
        self.popMenu_gcomp.exec_(self.ui.comboBox_gondo_compproject.mapToGlobal(point))

    def on_context_menu(self, point):
        self.popMenu_assetlive.exec_(self.ui.pushButton_makelive.mapToGlobal(point))

    def on_context_gversions(self, point):
        self.popMenu_gversions.exec_(self.ui.treeWidget_gondo_versions.mapToGlobal(point))

    def on_context_glayers(self, point):
        self.popMenu_glayers.exec_(self.ui.listWidget_gondo_layers.mapToGlobal(point))

    def on_context_copylist(self, point):
        self.popMenu_copylist.exec_(self.ui.listWidget_gondo_copylist.mapToGlobal(point))

    def getSpots(self):
        spots = []
        for dir in os.listdir(self.scenes_root):
            dir_path = os.path.join(self.scenes_root, dir)
            if not re.match('\.', dir) and os.path.isdir(dir_path):

                if self.isSpot(dir_path):
                    spots.append(dir)
                if debug: print 'spots: ', spots
        return spots

    def getAssets(self):
        # return dict of assetname:assetPath pairs

        if debug: print 'assets_root:', self.assets_root
        assets = {}
        try:
            for asset_type in os.listdir(self.assets_root):
                asset_type_path = os.path.join(self.assets_root, asset_type)

                if os.path.isdir(asset_type_path):
                    if debug: print asset_type, os.path.isdir(asset_type_path)
                    try:
                        for assetname in os.listdir(os.path.join(asset_type_path, 'dev')):
                            asset_path = os.path.join(asset_type_path, 'dev', assetname)
                            if os.path.isdir(asset_path):
                                assets[assetname] = {'path':os.path.normpath(asset_path),"type":asset_type}
                    except WindowsError as e:
                        print 'No Dev Folder found!'
                        print e
        except WindowsError as e:
            pass

        if debug: print 'assets:', assets
        return assets

    def getVersions_asset(self, asset_path):
        # return list of published model/rigs and renderable assets if shd found
        versions = []
        publish_base = os.path.join(asset_path, 'publish')
        publish_shd = os.path.join(asset_path, 'shd', 'publish')
        try:
            for version in os.listdir(publish_base):
                if os.path.isfile(os.path.join(publish_base, version)):
                    versions.append(version)
        except:
            print 'No rig publish directory found!'
            pass
        try:
            if os.path.isdir(publish_shd):
                for shd_version in os.listdir(publish_shd):
                    if os.path.isfile(os.path.join(publish_shd, shd_version)):
                        versions.append(shd_version)
        except:
            print 'No shd publish directory found!'
            pass
        return versions

    def isSpot(self, dir):

        if filter(lambda x: re.match('sh[0-9]+', x), os.listdir(dir)):
            return True
        else:
            return False

    def getShots(self):
        shots = defaultdict(lambda: defaultdict(str))

        for dir in os.listdir(self.scenes_root):
            dir_path = os.path.join(self.scenes_root, dir)
            if not re.match('\.', dir) and os.path.isdir(dir_path):
                if self.isSpot(dir_path):
                    spotpath = dir_path
                    for subdir in os.listdir(dir_path):
                        if re.match('sh[0-9]+', subdir):
                            shotpath = os.path.join(spotpath, subdir)
                            if os.path.isdir(shotpath):
                                shots[dir][subdir] = shotpath
                elif re.match('sh[0-9]+', dir):
                    spotpath = self.scenes_root
                    shotpath = os.path.join(spotpath, subdir)
                    if os.path.isdir(shotpath):
                        shots[''][dir] = shotpath

        return shots

    def getVersions_shot(self, shot_path):
        versions = []
        anim_publishpath = os.path.join(shot_path, 'anim', 'publish')
        cache_path = os.path.join(anim_publishpath, 'cache')
        # try:
        for version in os.listdir(anim_publishpath):
            if os.path.isfile(os.path.join(anim_publishpath, version)):
                versions.append(version)
        if os.path.isdir(cache_path):
            for version in os.listdir(cache_path):
                if os.path.isfile(os.path.join(cache_path, version)):
                    versions.append(version)
        # except:
        #     pass
        return versions

    def pop_shotlist(self):
        self.ui.listWidget_shots.clear()
        shotlist = self.getShots()
        for spot in shotlist:
            for shot in shotlist[spot]:
                shotname = spot + '_' + shot
                shot_item = QtWidgets.QListWidgetItem(self.ui.listWidget_shots)
                shot_item.setText(shotname)

    def pop_shotVersions(self):
        selected_shot = self.ui.listWidget_shots.currentItem().text()
        spot = '_'.join(selected_shot.split('_')[:-1])
        shot = selected_shot.split('_')[-1]

        with open(self.status_path, 'r') as statusfile_read:
            stat_read = json.load(statusfile_read)
        self.ui.treeWidget_animVersions.clear()

        type_items = []
        topItem_anim = QtWidgets.QTreeWidgetItem()
        topItem_anim.setText(0, 'Animation')
        type_items.append(topItem_anim)

        topItem_cache = QtWidgets.QTreeWidgetItem()
        topItem_cache.setText(0, 'Cache')
        type_items.append(topItem_cache)

        self.ui.treeWidget_animVersions.addTopLevelItems(type_items)

        for item in type_items:
            item.setExpanded(True)

        for version in self.getVersions_shot(self.getShots()[spot][shot]):
            basename, ver, ext = version.split('.')
            shotname = '_'.join(basename.split('_')[:2])

            if '.abc' in version.lower():
                version_item = QtWidgets.QTreeWidgetItem(topItem_cache)
                version_item.setText(0, version)
                if stat_read['shot'][shotname]['cache'][basename] == version_item.text(0):
                    version_item.setText(1, 'Live')
                #self.update_status('shot', selected_shot, version, 'cache')
            elif 'anim' in version.lower():
                version_item = QtWidgets.QTreeWidgetItem(topItem_anim)
                version_item.setText(0, version)
                if stat_read['shot'][shotname]['anim'][basename] == version_item.text(0):
                    version_item.setText(1, 'Live')
                #self.update_status('shot', selected_shot, version, 'anim')
            else:
                version_item = QtWidgets.QTreeWidgetItem(self.ui.treeWidget_animVersions)
                version_item.setText(0, version)

    def pop_assetlist(self):
        self.ui.treeWidget_assets.clear()
        asset_types = set()

        for asset in self.getAssets():
            asset_type = self.getAssets()[asset]['type']
            asset_types.add(asset_type)
        asset_types = list(asset_types)
        for itemtype in asset_types:
            type_item = QtWidgets.QTreeWidgetItem()
            type_item.setText(0, itemtype)
            self.ui.treeWidget_assets.addTopLevelItem(type_item)
            type_item.setExpanded(True)
        for asset in self.getAssets():
            asset_type = self.getAssets()[asset]['type']
            asset_type_item = self.ui.treeWidget_assets.findItems(asset_type, 0)[0]
            asset_item = QtWidgets.QTreeWidgetItem(asset_type_item)
            asset_item.setText(0, asset)

    def pop_assetVersions(self):
        debug = False
        selected_asset = self.ui.treeWidget_assets.currentItem().text(0)
        with open(self.status_path, 'r') as statusfile_read:
            stat_read = json.load(statusfile_read)
        self.ui.treeWidget_versions.clear()

        type_items = []
        topItem_rig = QtWidgets.QTreeWidgetItem()
        topItem_rig.setText(0, 'Rig')
        type_items.append(topItem_rig)

        topItem_shd = QtWidgets.QTreeWidgetItem()
        topItem_shd.setText(0, 'Shd')
        type_items.append(topItem_shd)

        topItem_mtl = QtWidgets.QTreeWidgetItem()
        topItem_mtl.setText(0, 'Mtl')
        type_items.append(topItem_mtl)

        self.ui.treeWidget_versions.addTopLevelItems(type_items)
        for item in type_items:
            item.setExpanded(True)
        try:
            for version in self.getVersions_asset(self.getAssets()[selected_asset]['path']):
                if debug: print 'version:', version

                if 'rig' in version.lower():
                    version_item = QtWidgets.QTreeWidgetItem(topItem_rig)
                    version_item.setText(0, version)
                elif 'shd' in version.lower():
                    version_item = QtWidgets.QTreeWidgetItem(topItem_shd)
                    version_item.setText(0, version)
                elif 'mtl' in version.lower():
                    version_item = QtWidgets.QTreeWidgetItem(topItem_mtl)
                    version_item.setText(0, version)
                else:
                    version_item = QtWidgets.QTreeWidgetItem(self.ui.treeWidget_versions)
                    version_item.setText(0, version)
                version_basename = version_item.text(0).split('.')[0]

                if debug: print version_basename
                try:
                    if stat_read['asset'][selected_asset]['default'][version_basename] == version_item.text(0):
                        version_item.setText(1, 'Live')
                except KeyError:
                    pass

                try:
                    if stat_read['asset'][selected_asset]['shd'][version_basename]  == version_item.text(0):
                        version_item.setText(1, 'Live')
                except KeyError:
                    pass

                try:
                    if stat_read['asset'][selected_asset]['mtl'][version_basename]  == version_item.text(0):
                        version_item.setText(1, 'Live')
                except KeyError:
                    pass
        except KeyError:
            pass

    def make_statusfile(self, statusfile_path):
        if os.path.exists(statusfile_path):
            with open(statusfile_path, 'w') as statusfile:
                default_content = {'asset':{},
                                   'shot':{},
                                   'complinks':{}
                                   }
                json.dump(default_content, statusfile)

    def makelive_assets(self):
        asset = self.ui.treeWidget_assets.currentItem()
        version = self.ui.treeWidget_versions.currentItem()
        asset_path = self.getAssets()[asset.text(0)]['path']

        dev_dir = os.path.dirname(asset_path)
        type_dir = os.path.dirname(dev_dir)
        if 'shd' in version.text(0):
            version_path = os.path.join(asset_path, 'shd', 'publish', version.text(0))
            shutil.copy2(version_path, os.path.join(type_dir, 'renderable', '{0}.mb'.format(asset.text(0))))
            self.update_status('asset', asset.text(0), version.text(0), 'shd')
        elif 'mtl' in version.text(0):
            version_path = os.path.join(asset_path, 'shd', 'publish', version.text(0))
            shutil.copy2(version_path, os.path.join(type_dir, 'renderable', '{0}_mtl.mb'.format(asset.text(0))))
            self.update_status('asset', asset.text(0), version.text(0), 'mtl')
        else:
            version_path = os.path.join(asset_path, 'publish', version.text(0))
            shutil.copy2(version_path, os.path.join(type_dir, '{0}.mb'.format(asset.text(0))))
            self.update_status('asset', asset.text(0), version.text(0), 'default')

    def makelive_assets_all(self):
        assets = self.getAssets()
        for asset in assets:

            asset_path = os.path.join(assets[asset]['path'], 'publish')
            asset_shd_path = os.path.join(assets[asset]['path'], 'shd', 'publish')
            latest_asset = fileUtils.getLatest(asset_path, asset, filename=True, none_return=True)
            latest_shd = fileUtils.getLatest(asset_shd_path, asset, filename=True, stage='shd', none_return=True)
            latest_mtl = fileUtils.getLatest(asset_shd_path, asset, filename=True, stage='mtl', none_return=True)
            type_dir = os.path.join(self.assets_root, assets[asset]['type'])
            print asset
            print 'rig', latest_asset
            print 'shd', latest_shd
            print 'mtl', latest_mtl
            print
            if latest_asset:
                version_path = os.path.join(asset_path, latest_asset)
                print version_path
                shutil.copy2(version_path, os.path.join(type_dir, '{0}.mb'.format(asset)))
                self.update_status('asset', asset, latest_asset, 'default')
            if latest_shd:
                version_path = os.path.join(asset_shd_path, latest_shd)
                print version_path
                shutil.copy2(version_path, os.path.join(type_dir,  'renderable', '{0}.mb'.format(asset)))
                self.update_status('asset', asset, latest_shd, 'shd')
            if latest_mtl:
                version_path = os.path.join(asset_shd_path, latest_mtl)
                print version_path
                shutil.copy2(version_path, os.path.join(type_dir, 'renderable', '{0}.mb'.format(asset)))
                self.update_status('asset', asset, latest_mtl, 'mtl')

    def makelive_shots(self):
        selected_shot = self.ui.listWidget_shots.currentItem()
        selected_version = self.ui.treeWidget_animVersions.currentItem()
        spot = '_'.join(selected_shot.text().split('_')[:-1])
        shot = selected_shot.text().split('_')[-1]
        shotroot = spot + '_' + shot

        shot_path = self.getShots()[spot][shot]

        if '.abc' in selected_version.text(0):
            cachename = '{0}'.format('_'.join(selected_version.text(0).split('_')[:-1]))
            live_path = os.path.join(shot_path, '{0}_cache.abc'.format(cachename))
            version_path = os.path.join(shot_path, 'anim', 'publish', 'cache', selected_version.text(0))
            shutil.copy2(version_path, live_path)
            self.update_status('shot', selected_shot.text(), selected_version.text(0), 'cache')
        else:
            live_path = os.path.join(shot_path, '{0}_anim.ma'.format('_'.join(selected_version.text(0).split('_')[:-1])))
            version_path = os.path.join(shot_path, 'anim', 'publish', selected_version.text(0))
            shutil.copy2(version_path, live_path)
            print refEdit.edit(live_path)
            self.update_status('shot', selected_shot.text(), selected_version.text(0), 'anim')

    def update_status(self, assetType, name, version, state):


        with open(self.status_path, 'r') as statusfile_read:
            stat_read = json.load(statusfile_read)
            basename, ver, ext = version.split('.')
        # Try to edit asset status, if not found, create new entry

        try:

            stat_read[assetType][name][state][basename] = version

        except:
            defdict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(str))), stat_read)
            defdict[assetType][name][state][basename] = version

        with open(self.status_path, 'w') as statusfile_write:
            json.dump(stat_read, statusfile_write, indent=4)

        # Loop through current listed versions, clear status, if version matches value in shade state, mark as Live
        version_items = []
        if assetType == 'asset':
            for item in range(self.ui.treeWidget_versions.topLevelItemCount()):
                #self.ui.treeWidget_versions.topLevelItem(item)
                type_item = self.ui.treeWidget_versions.topLevelItem(item)
                childcnt = type_item.childCount()
                for n in range(childcnt):
                    child = type_item.child(n)
                    version_items.append(child)
        elif assetType == 'shot':
            for item in range(self.ui.treeWidget_animVersions.topLevelItemCount()):
                toplvl_item = self.ui.treeWidget_animVersions.topLevelItem(item)
                for version_index in range(toplvl_item.childCount()):
                    version_item = toplvl_item.child(version_index)
                    version_items.append(version_item)

        for item in version_items:
            item.setText(1, '')
            item_basename, item_ver, item_ext = item.text(0).split('.')
            with open(self.status_path, 'r') as statusfile_read:
                stat_read = json.load(statusfile_read)
            try:
                if stat_read[assetType][name]['default'][item_basename] == item.text(0):
                    item.setText(1, 'Live')
            except KeyError:
                pass

            try:
                if stat_read[assetType][name]['shd'][item_basename] == item.text(0):
                    item.setText(1, 'Live')
            except KeyError:
                pass

            try:
                if stat_read[assetType][name]['mtl'][item_basename] == item.text(0):
                    item.setText(1, 'Live')
            except KeyError:
                pass

            try:
                if stat_read[assetType][name]['anim'][item_basename] == item.text(0):
                    item.setText(1, 'Live')
            except KeyError:
                pass
            try:
                if stat_read[assetType][name]['cache'][item_basename] == item.text(0):
                    item.setText(1, 'Live')
            except KeyError:
                pass

    def unsaved_confirm(self):
        result = pm.confirmBox(
            title='Unsaved Changes',
            message='This file contains unsaved changes, save before continuing?',
            button=['Yes', 'No', 'Cancel'],
            dismissString='Close'
        )
        return result

    def open_latest_shot(self):

        selected_shot = self.ui.listWidget_shots.currentItem().text()
        spot = '_'.join(selected_shot.split('_')[:-1])
        shot = selected_shot.split('_')[-1]
        shotroot = spot + '_' + shot
        animpath = os.path.join(self.scenes_root, "{0}_shots".format(spot), shot, 'anim')
        basename = shotroot
        basename_parts = []
        if fileUtils.ismultipart(animpath, basename):
            basename_parts = fileUtils.getLatest(animpath, basename, filename=True, stage='anim', parts=True)
        animver = fileUtils.getLatest(animpath, basename, filename=True, stage='anim')
        renderpath = os.path.join(self.scenes_root, "{0}_shots".format(spot), shot, 'render')
        basename_render = shotroot + '_render'
        latest_render = ''
        if os.path.exists(renderpath):
            if os.listdir(renderpath):
                latest_renderver = fileUtils.getLatest(renderpath, basename_render)
                for render_version in os.listdir(renderpath):
                    if latest_renderver in render_version:
                        latest_render = render_version

        if latest_render:
            result = pm.confirmDialog(
                title='Choose your own adventure!',
                message='A renderable scene of this shot was found, which scene do you want to open?',
                button=['animation', 'Renderable', 'Cancel'],
                cancelButton='Close',
                dismissString='Close',
            )

            if result == 'animation':
                if basename_parts:
                    print basename_parts.keys()
                    result = pm.confirmDialog(
                        title='Choose your own adventure!',
                        message='Multiple parts were found, which scene do you want to open?',
                        button=basename_parts.keys(),
                        cancelButton='Close',
                        dismissString='Close',
                    )
                    print result

                    try:
                        pm.openFile(os.path.join(animpath, result))
                    except RuntimeError:
                        print 'Opening:', basename_parts[result][-1]
                        confirm = self.unsaved_confirm()

                        if confirm == True:
                            pm.saveFile()
                            pm.openFile(os.path.join(animpath, basename_parts[result][-1]), force=True)
                        elif confirm == False:
                            pm.openFile(os.path.join(animpath, basename_parts[result][-1]), force=True)

                else:
                    try:
                        pm.openFile(os.path.join(animpath, animver))
                    except RuntimeError:
                        confirm = self.unsaved_confirm()

                        if confirm == True:
                            pm.saveFile()
                            pm.openFile(os.path.join(animpath, animver), force=True)
                        elif confirm == False:
                            pm.openFile(os.path.join(animpath, animver), force=True)
                        else:
                            pass
            if result == 'Renderable':
                try:
                    pm.openFile(os.path.join(renderpath, latest_render))
                except RuntimeError:
                    confirm = self.unsaved_confirm()

                    if confirm == True:
                        pm.saveFile()
                        pm.openFile(os.path.join(renderpath, latest_render), force=True)
                    elif confirm == False:
                        pm.openFile(os.path.join(renderpath, latest_render), force=True)
                    else:
                        pass
        else:
            try:
                pm.openFile(os.path.join(animpath, animver))
            except RuntimeError:
                confirm = self.unsaved_confirm()

                if confirm == True:
                    pm.saveFile()
                    pm.openFile(os.path.join(animpath, animver), force=True)
                elif confirm == False:
                    pm.openFile(os.path.join(animpath, animver), force=True)
                else:
                    pass

    def open_latest_asset(self):
        latest_shd = None
        selected_asset = self.ui.treeWidget_assets.currentItem().text(0)
        assettype = self.getAssets()[selected_asset]['type']
        # def getType():
        #     assettype = ''
        #     for dir in os.listdir(self.assets_root):
        #         for item in os.listdir(os.path.join(self.assets_root, dir)):
        #             if selected_asset in item:
        #                 assettype = dir
        #     return assettype

        sel_assetroot = os.path.join(self.assets_root, assettype, 'dev', selected_asset)
        shd_path = os.path.join(sel_assetroot, 'shd')
        try:
            latest_assetver = fileUtils.getLatest(sel_assetroot, selected_asset)
            if os.path.exists(shd_path):
                if os.listdir(shd_path):
                    latest_shdver = fileUtils.getLatest(shd_path, selected_asset)
                    for shd_version in os.listdir(shd_path):
                        if latest_shdver in shd_version:
                            latest_shd = shd_version
                        else:
                            pass
                else:
                    print '{0} is empty'.format(shd_path)
            else:
                print '{0} doesnt exist'.format(shd_path)
            for asset_version in os.listdir(sel_assetroot):
                if latest_assetver in asset_version:
                    latest_asset = asset_version
                else:
                    pass
        except WindowsError:
            return

        if latest_shd:
            result = pm.confirmDialog(
                title='Choose your own adventure!',
                message='A renderable version of this asset was found, which rig do you want to open?',
                button=['Non-Renderable', 'Renderable', 'Cancel'],
                cancelButton='Close',
                dismissString='Close',
            )
            if result == 'Non-Renderable':
                try:

                    pm.openFile(os.path.join(sel_assetroot, latest_asset))
                except RuntimeError:

                    confirm = self.unsaved_confirm()

                    if confirm == True:

                        pm.saveFile()
                        pm.openFile(os.path.join(sel_assetroot, latest_asset), force=True)
                    elif confirm == False:

                        pm.openFile(os.path.join(sel_assetroot, latest_asset), force=True)
                    else:
                        pass

            elif result == 'Renderable':
                try:

                    pm.openFile(os.path.join(shd_path, latest_shd))
                except RuntimeError:

                    confirm = self.unsaved_confirm()

                    if confirm == True:

                        pm.saveFile()
                        pm.openFile(os.path.join(shd_path, latest_shd), force=True)
                    elif confirm == False:

                        pm.openFile(os.path.join(shd_path, latest_shd), force=True)
                    else:
                        pass
            else:
                return

        else:
            try:

                pm.openFile(os.path.join(sel_assetroot, latest_asset))
            except RuntimeError:

                confirm = self.unsaved_confirm()

                if confirm == True:

                    pm.saveFile()
                    pm.openFile(os.path.join(sel_assetroot, latest_asset), force=True)
                elif confirm == False:

                    pm.openFile(os.path.join(sel_assetroot, latest_asset), force=True)
                else:
                    pass

    def showcomment_asset(self):
        selected_asset = self.ui.treeWidget_assets.currentItem().text(0)
        selected_version = self.ui.treeWidget_versions.currentItem().text(0)
        assets = self.getAssets()
        try:
            if selected_asset in assets:
                asset_changelog = os.path.join(assets[selected_asset]['path'], 'changelog.json')
                if os.path.exists(asset_changelog):
                    with open(asset_changelog, 'r') as log_read:
                        log = json.load(log_read)
                    self.ui.comment_asset.setText(log[selected_version]['comment'])
        except:
            pass

    def setarbProj(self):
        arbproj_root = pm.windows.promptForFolder()
        self.ui.lineEdit_arb_projPath.setText(arbproj_root)
        #self.ui.lineEdit_arb_projPath.setText("Z:/raid/3Dprojects/maya/projects")
    def run_arborist(self):
        projectDest = self.ui.lineEdit_arb_projPath.text()
        #print 'projectDest: {0}'.format(projectDest)
        commands = self.ui.textEdit_arb_commands.toPlainText().split('\n')
        for line in commands:
            projname = line.split(' ')[0]
            projpath = os.path.join(projectDest, projname)
            obj_type = line.split(' ')[2]
            if obj_type == 'project':
                arborist.createProject(projname, projectDest)
            if obj_type == 'spot':
                spotname = line.split(' ')[3]
                shotcnt = int(line.split(' ')[4])
                arborist.createSpot(projpath, spotname, shotcnt)
            if obj_type == 'shot':
                'starkist create shot sk_bpouch/sh051'
                shot = line.split(' ')[3]
                arborist.createShot(projpath, shot)
            if obj_type == 'asset':
                assettype = line.split(' ')[3]
                assetname = line.split(' ')[4]
                arborist.createAsset(projpath, assettype, assetname)
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
        #self.show(dockable=True, floating=True)
        self.show(dockable=True)
        # not sure what e argument means
        pm.workspaceControl(workspaceControlName, e=True, ih=150)

myWin = myGui()

def run():
    myWin.run()

def test():
    return 'hello World!'