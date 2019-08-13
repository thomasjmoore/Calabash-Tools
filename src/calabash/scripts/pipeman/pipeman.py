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
from functools import partial
from __builtin__ import any as any
import pprint


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

#import converted ui file.
import pipeman_ui as ui_file
import openAsset as oa
import refEdit
import arborist
from calabash import fileUtils
reload(ui_file)
reload(oa)
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
        self.ui.lineEdit_arb_projPath.setText(self.proj_root)

        self.comproot = ''
        self.publishDict = {}
        self.scenes_root = os.path.join(self.proj_path, 'scenes')
        self.images_root = os.path.join(self.proj_path, 'images')
        self.spots = self.getSpots()
        self.assets_root = os.path.join(self.scenes_root, 'assets')
        self.status_path = os.path.join(self.scenes_root, 'status.json')

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

        self.header_assets = self.ui.treeWidget_versions.header()
        self.header_assets.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.header_assets.setStretchLastSection(False)
        self.header_assets.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.header_anim = self.ui.treeWidget_animVersions.header()
        self.header_anim.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.header_anim.setStretchLastSection(False)
        self.header_anim.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.header_asset_comments = self.ui.asset_comments.header()
        self.header_asset_comments.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.header_asset_comments.setStretchLastSection(False)
        self.header_asset_comments.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.header_anim_comments = self.ui.anim_comments.header()
        self.header_anim_comments.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.header_anim_comments.setStretchLastSection(False)
        self.header_anim_comments.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.ui.treeWidget_shots.itemClicked.connect(partial(self.pop_Versions, self.ui.treeWidget_shots))
        self.ui.treeWidget_assets.itemClicked.connect(partial(self.pop_Versions, self.ui.treeWidget_assets))
        self.ui.treeWidget_animVersions.itemClicked.connect(partial(self.showcomment, self.ui.treeWidget_animVersions))
        self.ui.treeWidget_versions.itemClicked.connect(partial(self.showcomment, self.ui.treeWidget_versions))

        self.ui.pushButton_makelive.clicked.connect(self.makelive_asset)

        self.ui.comboBox_mayaproject.customContextMenuRequested.connect(self.on_context_maya)
        self.popMenu_maya = QtWidgets.QMenu(self)
        self.popMenu_maya.addAction(QtWidgets.QAction('Set Maya projects location', self))
        self.popMenu_maya.triggered.connect(self.set_mayaroot)

        self.ui.comboBox_gondo_compproject.customContextMenuRequested.connect(self.on_context_comp)
        self.popMenu_gcomp = QtWidgets.QMenu(self)
        self.popMenu_gcomp.addAction(QtWidgets.QAction('Set Comp projects location', self))
        self.popMenu_gcomp.triggered.connect(self.set_comproot)

        self.ui.pushButton_anim_makelive.clicked.connect(self.makelive_shot)
        self.ui.pushButton_anim_openlatest.clicked.connect(partial(self.open_latest, self.ui.treeWidget_shots))
        self.ui.pushButton_asset_openlatest.clicked.connect(partial(self.open_latest, self.ui.treeWidget_assets))
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

        self.pop_assets()
        self.pop_shots()

    def mayaproj_changed(self):
        self.setProject()
        self.pop_shots()
        self.pop_assets()
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
        debug = False
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
        debug = False
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

    def get_subnames(self, filelist):
        debug = False
        if debug: print filelist
        subnames = set()
        for filename in filelist:
            if len(filename.split('.')) == 3:
                subname, version, ext = filename.split('.')
                subnames.add(subname)
        return list(subnames)

    def getAssets(self):
        # return dict of assettype:assetroot tuples
        debug = False
        print 'Getting Assets'
        if debug: print 'assets_root:', self.assets_root
        assets = {}

        for asset_type in os.listdir(self.assets_root):

            if os.path.isdir(os.path.join(self.assets_root, asset_type)):
                if debug: print asset_type
                typepath = os.path.join(self.assets_root, asset_type, 'dev')
                if debug: print typepath
                assetnames = [f for f in os.listdir(typepath) if os.path.isdir(os.path.join(typepath, f))]
                if debug: print assetnames
                for assetname in assetnames:
                    asset_root = os.path.normpath(os.path.join(typepath, assetname)).replace('\\', '/')
                    assets[assetname] = (asset_type,asset_root)

        if debug: print 'assets:', assets
        return assets

    def getAssetsubnames(self, asset):
        # return list of subname, path tuples
        debug = False
        if debug: print asset

        assetsubnames = {}
        asset_type, assetroot = self.getAssets()[asset]

        files = [f for f in os.listdir(assetroot) if os.path.isfile(os.path.join(assetroot, f))]
        for subname in self.get_subnames(files):
            assetsubnames[subname] = assetroot

        return assetsubnames

    def isSpot(self, dir):
        debug = False
        if debug: print dir
        if os.path.isdir(dir):
            if filter(lambda x: re.match('sh[0-9]+', x), os.listdir(dir)):
                return True
            else:
                return False

    def getSpots(self):
        spots = []
        for dir in os.listdir(self.scenes_root):
            dir_path = os.path.join(self.scenes_root, dir)
            if not re.match('\.', dir) and os.path.isdir(dir_path):

                if self.isSpot(dir_path):
                    spots.append(dir)
                if debug: print 'spots: ', spots
        return spots

    def getShots(self):
        debug = False
        shots = {}

        for dir in os.listdir(self.scenes_root):
            dir_path = os.path.join(self.scenes_root, dir)
            if not re.match('\.', dir) and os.path.isdir(dir_path):
                if self.isSpot(dir_path):
                    spotpath = dir_path
                    for subdir in os.listdir(dir_path):
                        if re.match('sh[0-9]+', subdir):
                            shotpath = os.path.join(spotpath, subdir)
                            if os.path.isdir(shotpath):
                                shotname = dir + '_' + subdir
                                shots[shotname] = shotpath
                elif re.match('sh[0-9]+', dir):
                    spotpath = self.scenes_root
                    shotpath = os.path.join(spotpath, dir)
                    if os.path.isdir(shotpath):
                        shots[dir] = shotpath

        if debug: print shots
        return shots

    def getShotsubnames(self, shot):
        debug = False
        # return subname, path tuples
        shotsubnames = {}
        shotroot = self.getShots()[shot]
        animdir = os.path.join(shotroot, 'anim')
        rendir = os.path.join(shotroot, 'render')

        animfiles = [f for f in os.listdir(animdir) if os.path.isfile(os.path.join(animdir, f))]
        renfiles = [f for f in os.listdir(rendir) if os.path.isfile(os.path.join(rendir, f))]
        for subname in self.get_subnames(animfiles):

            shotsubnames[subname] = animdir

        if renfiles:
            for subname in self.get_subnames(renfiles):
                shotsubnames[subname] = rendir

        return shotsubnames

    def getversions(self, subnames, *args):
        # return version, path tuples
        debug = False
        publish = ''
        for key in args:
            if key == 'p':
                print 'Getting Published Versions'
                publish = 'publish'
            else:
                print 'Getting Working Versions'

        version_dict = {}

        for subname in subnames:
            try:
                subname_path = os.path.join(subnames[subname], publish)
                if debug: print subname_path

                files = [f for f in os.listdir(subname_path) if os.path.isfile(os.path.join(subname_path, f))]

                if debug: print 'Files:', files
                for f in files:
                    path = os.path.join(subname_path, f)
                    if subname in f:
                        if not subname in version_dict.keys():
                            version_dict[subname] = {f:{'path':path}}
                        else:
                            version_dict[subname][f] = {'path':path}

            except WindowsError as winErr:
                print winErr
                continue

        return version_dict

    def pop_shots(self):
        debug = False
        spot_dict = {}
        self.ui.treeWidget_shots.clear()
        shots = self.getShots()
        for shotname in shots:

            spot = '_'.join(shotname.split('_')[:-1])
            if spot:
                if not spot in spot_dict:
                    spot_item = QtWidgets.QTreeWidgetItem()
                    spot_item.setText(0, spot)

                    spot_dict[spot] = spot_item

                shot_item = QtWidgets.QTreeWidgetItem(spot_dict[spot])
                shot_item.setText(0, shotname)
                if debug: print shot_item, shot_item.text(0)

                for item in spot_dict:
                    self.ui.treeWidget_shots.addTopLevelItem(spot_dict[item])
                    spot_dict[item].setExpanded(True)
            else:
                shot_item = QtWidgets.QTreeWidgetItem(self.ui.treeWidget_shots)
                shot_item.setText(0, shotname)
        if debug: print pprint.pprint(spot_dict)

    def pop_assets(self):
        debug = False
        self.ui.treeWidget_assets.clear()
        asset_dict = {}
        if debug: print '#pop_assets#'
        assets = self.getAssets()
        for assetname in assets:
            if debug: print assetname
            asset_type, path = assets[assetname]
            if debug: print asset_type
            shddir_check = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f)) and f == 'shd']

            if shddir_check:
                print 'OLD PROJECT DETECTED!!!!!!!!'
                self.retrofit()
                break
            if not asset_type in asset_dict:
                type_item = QtWidgets.QTreeWidgetItem()
                type_item.setText(0, asset_type)
                asset_dict[asset_type] = type_item
            asset_item = QtWidgets.QTreeWidgetItem(asset_dict[asset_type])
            asset_item.setText(0,assetname)
        if debug: print pprint.pprint(asset_dict)
        for item in asset_dict:
            self.ui.treeWidget_assets.addTopLevelItem(asset_dict[item])
            asset_dict[item].setExpanded(True)

    def pop_Versions(self, tree, *args):
        debug = False

        try:
            currentSelection = tree.currentItem()
            if currentSelection.childCount() < 1:
                if tree == self.ui.treeWidget_shots:
                    self.publishDict = self.getversions(self.getShotsubnames(currentSelection.text(0)), 'p')
                    if debug: '#pop_versions#', pprint.pprint(self.publishDict)
                    self.update_statusfile()
                    self.buildVersionTree(self.ui.treeWidget_animVersions, self.publishDict)


                elif tree == self.ui.treeWidget_assets:
                    # print 'Getting Asset Versions'
                    # print currentSelection.text(0)
                    self.publishDict = self.getversions(self.getAssetsubnames(currentSelection.text(0)), 'p')
                    if debug: '#pop_versions#', pprint.pprint(self.publishDict)
                    self.update_statusfile()
                    self.buildVersionTree(self.ui.treeWidget_versions, self.publishDict)


        except AttributeError as attrErr:
            print attrErr
            print 'Nothing Selected'
            pass

    def buildVersionTree(self, tree, versionDict):
        tree_dict = {}
        tree.clear()
        with open(self.status_path, 'r') as statread:
            statread = json.load(statread)
            for subname in versionDict:
                type = subname.split('_')[-1]
                if not type in tree_dict:
                    type_item = QtWidgets.QTreeWidgetItem()
                    type_item.setText(0, type)
                    tree_dict[type] = {'type':type_item}
                subname_item = QtWidgets.QTreeWidgetItem(tree_dict[type]['type'])
                subname_item.setText(0,subname)
                tree_dict[type][subname] = subname_item
                for version in versionDict[subname]:
                    version_item = QtWidgets.QTreeWidgetItem(subname_item)
                    version_item.setText(0, version)
                    if statread[subname][version]['live']:
                        status = 'Live'
                    else:
                        status = ''
                    version_item.setText(1, status)
            for type in tree_dict:
                tree.addTopLevelItem(tree_dict[type]['type'])
                for subname in tree_dict[type]:
                    tree_dict[type][subname].setExpanded(True)

    def makelive(self, assetsubname, version, src, dst):
        # copy src to dst, return dst path
        shutil.copy2(src, dst)
        print 'Setting {0} to Live'.format(version)
        self.update_assetStatus(assetsubname, version, True)
        #print 'makelive:', dst

        return dst

    def makelive_asset(self):
        debug = False
        pop = False
        for item in self.ui.treeWidget_versions.selectedItems():
            if item.childCount() < 1:
                pop = True
                asset = self.ui.treeWidget_assets.currentItem()
                asset_type = asset.parent()
                asset_version = item
                asset_subname = asset_version.parent()
                if 'shd' in asset_subname.text(0) or 'mtl' in asset_subname.text(0):
                    state = 'renderable'
                    if 'mtl' in asset_subname.text(0):
                        live_name = asset_subname.text(0) + '.mb'
                    else:
                        live_name = asset.text(0) + '.mb'
                else:
                    state = ''
                    live_name = asset.text(0) + '.mb'

                if debug: pprint.pprint(self.publishDict)
                src = self.publishDict[asset_subname.text(0)][asset_version.text(0)]['path']
                dst = os.path.join(self.assets_root, asset_type.text(0), state, live_name)
                if debug: print 'source:', src
                if debug: print 'Destination:', dst
                print '\n#\nResult:', self.makelive(asset_subname.text(0), asset_version.text(0), src, dst)

        if pop: self.pop_Versions(self.ui.treeWidget_assets)

    def makelive_shot(self):
        debug = True
        pop = False
        for item in self.ui.treeWidget_animVersions.selectedItems():

            if item.childCount() < 1:
                pop = True
                spot = self.ui.treeWidget_shots.currentItem().parent().text(0)
                shot = self.ui.treeWidget_shots.currentItem().text(0).split('_')[-1]
                shot_version = item
                shot_subname = shot_version.parent()
                shot_type = shot_subname.parent()
                if '.abc' in shot_version.text(0):
                    live_name = shot_subname.text(0) + '.abc'
                else:
                    live_name = shot_subname.text(0) + '.mb'

                src = self.publishDict[shot_subname.text(0)][shot_version.text(0)]['path']
                dst = os.path.join(self.scenes_root, spot, shot, live_name)

                if debug: print 'source:', src
                if debug: print 'Destination:', dst
                #if debug: pprint.pprint(self.assetDict)

                if 'anim' in shot_subname.text(0):
                    mklive = self.makelive(shot_subname.text(0), shot_version.text(0), src, dst)
                    print '\n#\nResult:', mklive
                    remapped = refEdit.edit(mklive)
                    print '\nPaths remapped:'
                    for org, result in remapped:
                        print 'Original: {0} \nRemapped: {1}\n'.format(org, result)
                else:
                    print '\n#\nResult:', self.makelive(shot_subname.text(0), shot_version.text(0), src, dst)

        if pop: self.pop_Versions(self.ui.treeWidget_shots)

    def update_assetStatus(self, assetsubname, version, live):
        with open(self.status_path, 'r') as statread:
            statread = json.load(statread)
        for statversion in statread[assetsubname]:
            statread[assetsubname][statversion]['live'] = False

        statread[assetsubname][version]['live'] = live

        with open(self.status_path, 'w') as statwrite:
            json.dump(statread, statwrite, indent=4)

    def update_statusfile(self):
        debug = False
        if not os.path.exists(self.status_path):
            self.make_statusfile(self.status_path)

        with open(self.status_path, 'r') as statread:
            statread = json.load(statread)

        if debug: print 'publish dict:', pprint.pprint(self.publishDict)
        print '#########'
        if debug: print 'statread', pprint.pprint(statread)

        for subname in self.publishDict:
            if debug: print 'Checking if {0} in status.log'.format(subname)
            if not subname in statread:
                if debug: print '{0} not in status.log, adding...'.format(subname)
                statread[subname] = self.publishDict[subname]
                for version in statread[subname]:
                    statread[subname][version]['live'] = False
            else:
                for version in self.publishDict[subname]:

                    if not version in statread[subname]:
                        if debug: print '{0} not found in status.log'.format(version)
                        statread[subname][version] = self.publishDict[subname][version]
                        if debug: print 'New Entry:', pprint.pprint(statread[subname][version])
                        statread[subname][version]['live'] = False

        if debug: print 'Result:'
        if debug: pprint.pprint(statread)
        with open(self.status_path, 'w') as statwrite:
            json.dump(statread, statwrite, indent=4)

    def make_statusfile(self, statusfile_path):
        print 'Making Status file: {0}'.format(statusfile_path)

        with open(statusfile_path, 'w') as statusfile:
            default_content = {}
            json.dump(default_content, statusfile)

    def unsaved_confirm(self):
        result = pm.confirmBox(
            title='Unsaved Changes',
            message='This file contains unsaved changes, save before continuing?',
            button=['Yes', 'No', 'Cancel'],
            dismissString='Close'
        )
        return result

    def open_latest(self, tree, *args):
        debug = True

        try:
            asset = tree.currentItem()
            if asset.childCount() < 1:
                if tree == self.ui.treeWidget_shots:
                    workingDict = self.getversions(self.getShotsubnames(asset.text(0)))
                    if debug: 'WorkingDict:', pprint.pprint(workingDict)

                elif tree == self.ui.treeWidget_assets:
                    workingDict = self.getversions(self.getAssetsubnames(asset.text(0)))
                    if debug: 'WorkingDict:', pprint.pprint(workingDict)
                    for subname in workingDict:
                        print'Sorted:', sorted(workingDict[subname])[-1]
                latest = {}
                for subname in workingDict:

                    latest_version = sorted(workingDict[subname])[-1]
                    version_path = workingDict[subname][latest_version]['path']
                    latest[subname] = version_path

                if len(latest) > 1:
                    oa_gui = oa.myGui(latest)
                    oa_gui.run()
                else:
                    try:
                        if debug: print '#open_latest# latest.dict():', latest
                        if debug: print '#open_latest# latest.values()', latest.values()
                        path = latest[latest.keys()[0]]
                        print 'Opening:', path
                        pm.openFile(path)
                    except RuntimeError as rte:
                        print rte
                        confirm = self.unsaved_confirm()
                        if confirm == True:

                            pm.saveFile()
                            pm.openFile(path, force=True)
                        else:
                            pm.openFile(path, force=True)

        except AttributeError as attrErr:
            print attrErr
            print 'Nothing Selected'
            pass

    def showcomment(self, tree, *args):
        debug = False

        selecteditem = tree.currentItem()
        if selecteditem.childCount() < 1:
            version = selecteditem
            subname = selecteditem.parent()
            version_path = self.publishDict[subname.text(0)][version.text(0)]['path']
            if debug: print 'version_path:', version_path
            asset_publish = os.path.dirname(version_path)
            asset_root = os.path.dirname(asset_publish)
            if debug: print 'asset_root:', asset_root
            changelog = os.path.join(asset_root, 'changelog.json')
            try:
                with open(changelog, 'r') as changelog_read:
                    log = json.load(changelog_read)
                if tree == self.ui.treeWidget_versions:
                    comments = self.ui.asset_comments
                elif tree == self.ui.treeWidget_animVersions:
                    comments = self.ui.anim_comments
                comments.clear()
                if debug: print 'Asset Comments:', pprint.pprint(log[subname.text(0)])

                for vers in log[subname.text(0)]:
                    vers_item = QtWidgets.QTreeWidgetItem(comments)
                    vers_item.setExpanded(True)
                    vers_item.setText(0, vers)
                    for timestamp, comment in log[subname.text(0)][vers]:
                        log_item = QtWidgets.QTreeWidgetItem(vers_item)
                        log_item.setText(2, timestamp)
                        log_item.setText(1, comment)
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

    def retrofit(self):
        debug = False
        import retrofit as retrofit
        reload(retrofit)
        #popup window notifying the current project is old and should be fixed
        #button to open new window showing planned changes
        #Continue/cancel buttons
        #for each asset, move contents of shd to root
        #modify changelog.json:
        #for each version, make subtype key = version = [[timestamp, comment]]
        #for each shot, move contents of anim/publish/cache to anim/publish

        change_list = []
        if debug: print '#retrofit#'
        assets = self.getAssets()
        if debug: print assets
        for asset in assets:
            type, asset_root = assets[asset]
            if debug: print type
            if debug: print asset_root
            shddir_check = [f for f in os.listdir(asset_root) if os.path.isdir(os.path.join(asset_root, f)) and f == 'shd']
            if shddir_check:
                shddir = os.path.join(asset_root, shddir_check[0])
                for item in os.listdir(shddir):
                    if item != '.mayaSwatches':
                        item_path = os.path.join(shddir, item)
                        change_list.append(('move', item_path, asset_root))
                change_list.append(('remove', shddir, ''))
                if 'changelog.json' in os.listdir(asset_root):
                    change_list.append(('modify', os.path.join(asset_root, 'changelog.json'), ''))
        shots = self.getShots()
        for shot in shots:
            type, shot_root = shots[shot]
            publish_path = os.path.join(shot_root, 'anim', 'publish')
            cache_path = os.path.join(publish_path, 'cache')
            if os.path.exists(cache_path):
                for item in os.listdir(cache_path):
                    item_path = os.path.join(cache_path, item)
                    change_list.append(('move', item_path, publish_path))
                change_list.append(('remove', cache_path, ''))
                if 'changelog.json' in os.listdir(asset_root):
                    change_list.append(('modify', os.path.join(asset_root, 'changelog.json'), ''))

        retro = retrofit.myGui(change_list)
        retro.run()

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
    test_item = QtWidgets.QTreeWidgetItem(myWin.ui.treeWidget_shots)
    test_item.setText(0,'blah')