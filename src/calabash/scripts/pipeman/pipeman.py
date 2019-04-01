import pymel.core as pm
from PySide2 import QtCore, QtUiTools, QtWidgets
from PySide2.QtGui import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as apiUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQDockWidget
import os
import json
import shutil
import re

#Convert Ui file from Designer to a python module
# run this in script editor
'''
import sys, pprint, os
from pyside2uic import compileUi
Ui_File = 'ui_file' #No Extension
scripts_path = "Path To Ui file"
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
from calabash import fileUtils
reload(ui_file)
reload(refEdit)
reload(fileUtils)
debug = False

class myGui(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent=parent)

        self.ui = ui_file.Ui_mainUI()
        self.ui.setupUi(self)

        self.proj_path = pm.system.Workspace.getPath()
        self.scenes_root = os.path.join(self.proj_path, 'scenes')
        self.spots = self.getSpots()
        self.assets_root = os.path.join(self.scenes_root, 'assets')
        self.status_path = os.path.join(self.scenes_root, 'status.json')
        ######## CONNECT UI ELEMENTS AND FUNCTIONS BELOW HERE #########

        self.header_assets = self.ui.treeWidget_versions.header()
        self.header_assets.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.header_assets.setStretchLastSection(False)
        self.header_assets.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.header_anim = self.ui.treeWidget_animVersions.header()
        self.header_anim.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.header_anim.setStretchLastSection(False)
        self.header_anim.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.pop_assetlist()
        self.pop_shotlist()
        self.ui.listWidget_assets.itemClicked.connect(self.pop_assetVersions)
        self.ui.listWidget_shots.itemClicked.connect(self.pop_shotVersions)
        self.ui.pushButton_makelive.clicked.connect(self.makelive_assets)
        self.ui.pushButton_anim_makelive.clicked.connect(self.makelive_shots)
        self.ui.pushButton_anim_openlatest.clicked.connect(self.open_latest_shot)
        self.ui.pushButton_asset_openlatest.clicked.connect(self.open_latest_asset)

        if not os.path.isfile(self.status_path):
            self.make_statusfile(self.status_path)

    def getSpots(self):
        spots = []
        for dir in os.listdir(self.scenes_root):
            if 'shots' in dir:
                spotname = dir.replace('_shots', '')
                spotpath = os.path.join(self.scenes_root, dir)
                spots.append((spotname, spotpath))
        if debug: print 'spots: ', spots
        return spots

    def getAssets(self):
        # return dict of assetname:assetPath pairs

        if debug: print 'assets_root:', self.assets_root
        assets = {}
        for asset_type in os.listdir(self.assets_root):
            asset_type_path = os.path.join(self.assets_root, asset_type)

            if os.path.isdir(asset_type_path):
                if debug: print asset_type, os.path.isdir(asset_type_path)
                for assetname in os.listdir(os.path.join(asset_type_path, 'dev')):
                    asset_path = os.path.join(asset_type_path, 'dev', assetname)
                    if os.path.isdir(asset_path):
                        assets[assetname] = os.path.normpath(asset_path)
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

    def getShots(self):
        shots = {}

        for spotname, spotpath in self.spots:
            shots[spotname] = {}
            if debug: print 'spotpath:', spotpath
            for shot in os.listdir(spotpath):
                if re.match('sh[0-9]+', shot):
                    shotpath = os.path.join(spotpath, shot)
                    if os.path.isdir(shotpath):
                        shots[spotname][shot] = shotpath
        return shots

    def getVersions_shot(self, shot_path):
        versions = []
        anim_publishpath = os.path.join(shot_path, 'anim', 'publish')
        cache_path = os.path.join(anim_publishpath, 'cache')
        try:
            for version in os.listdir(anim_publishpath):
                if os.path.isfile(os.path.join(anim_publishpath, version)):
                    versions.append(version)
            if os.path.isdir(cache_path):
                for version in os.listdir(cache_path):
                    if os.path.isfile(os.path.join(cache_path, version)):
                        versions.append(version)
        except:
            pass
        return versions

    def pop_shotlist(self):
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
        for version in self.getVersions_shot(self.getShots()[spot][shot]):
            version_item = QtWidgets.QTreeWidgetItem(self.ui.treeWidget_animVersions)
            version_item.setText(0, version)
            try:
                if stat_read['shot'][selected_shot]['anim'] == version_item.text(0):
                    version_item.setText(1, 'Live')
            except KeyError:
                pass
            try:
                if stat_read['shot'][selected_shot]['cache'] == version_item.text(0):
                    version_item.setText(1, 'Live')
            except KeyError:
                pass

    def pop_assetlist(self):
        for asset in self.getAssets():
            asset_item = QtWidgets.QListWidgetItem(self.ui.listWidget_assets)
            asset_item.setText(asset)

    def pop_assetVersions(self):
        selected_asset = self.ui.listWidget_assets.currentItem().text()
        with open(self.status_path, 'r') as statusfile_read:
            stat_read = json.load(statusfile_read)
        self.ui.treeWidget_versions.clear()
        for version in self.getVersions_asset(self.getAssets()[selected_asset]):
            if debug: print 'version:', version
            version_item = QtWidgets.QTreeWidgetItem(self.ui.treeWidget_versions)
            version_item.setText(0, version)
            try:
                if stat_read['asset'][selected_asset]['default'] == version_item.text(0):
                    version_item.setText(1, 'Live')
            except KeyError:
                pass
            try:
                if stat_read['asset'][selected_asset]['shd'] == version_item.text(0):
                    version_item.setText(1, 'Live')
            except KeyError:
                pass
            try:
                if stat_read['asset'][selected_asset]['mtl'] == version_item.text(0):
                    version_item.setText(1, 'Live')
            except KeyError:
                pass

    def make_statusfile(self, statusfile_path):
        with open(statusfile_path, 'w') as statusfile:
            default_content = {'asset':{},
                               'shot':{}
                               }
            json.dump(default_content, statusfile)

    def makelive_assets(self):
        selected_asset = self.ui.listWidget_assets.currentItem()
        selected_version = self.ui.treeWidget_versions.currentItem()
        asset_path = self.getAssets()[selected_asset.text()]
        dev_dir = os.path.dirname(asset_path)
        type_dir = os.path.dirname(dev_dir)
        if 'shd' in selected_version.text(0):
            version_path = os.path.join(asset_path, 'shd', 'publish', selected_version.text(0))
            shutil.copy2(version_path, os.path.join(type_dir, 'renderable', '{0}.mb'.format(selected_asset.text())))
            self.update_status('asset', selected_asset.text(), selected_version.text(0), 'shd')
        elif 'mtl' in selected_version.text(0):
            version_path = os.path.join(asset_path, 'shd', 'publish', selected_version.text(0))
            shutil.copy2(version_path, os.path.join(type_dir, 'renderable', '{0}_mtl.mb'.format(selected_asset.text())))
            self.update_status('asset', selected_asset.text(), selected_version.text(0), 'mtl')
        else:
            version_path = os.path.join(asset_path, 'publish', selected_version.text(0))
            shutil.copy2(version_path, os.path.join(type_dir, '{0}.mb'.format(selected_asset.text())))
            self.update_status('asset', selected_asset.text(), selected_version.text(0), 'default')

    def makelive_shots(self):
        selected_shot = self.ui.listWidget_shots.currentItem()
        selected_version = self.ui.treeWidget_animVersions.currentItem()
        spot = '_'.join(selected_shot.text().split('_')[:-1])
        shot = selected_shot.text().split('_')[-1]
        shotroot = spot + '_' + shot

        shot_path = self.getShots()[spot][shot]

        if '.abc' in selected_version.text(0):
            cachename = '{0}_{1}'.format('_'.join(selected_version.text(0).split('_')[:-3]), shotroot)
            live_path = os.path.join(shot_path, '{0}_cache.abc'.format(cachename))
            version_path = os.path.join(shot_path, 'anim', 'publish', 'cache', selected_version.text(0))
            shutil.copy2(version_path, live_path)
            self.update_status('shot', selected_shot.text(), selected_version.text(0), 'cache')
        else:
            live_path = os.path.join(shot_path, '{0}_anim.ma'.format(shotroot))
            version_path = os.path.join(shot_path, 'anim', 'publish', selected_version.text(0))
            shutil.copy2(version_path, live_path)
            print refEdit.edit(live_path)
            self.update_status('shot', selected_shot.text(), selected_version.text(0), 'anim')

    def update_status(self, type, name, version, shadestate):


        with open(self.status_path, 'r') as statusfile_read:
            stat_read = json.load(statusfile_read)
        # Try to edit asset status, if not found, create new entry
        try:
            stat_read[type][name][shadestate] = version
        except KeyError:
            stat_read[type][name] = {shadestate:version}

        with open(self.status_path, 'w') as statusfile_write:
            json.dump(stat_read, statusfile_write, indent=4)

        # Loop through current listed versions, clear status, if version matches value in shade state, mark as Live
        version_items = []
        if type == 'asset':
            for item in range(self.ui.treeWidget_versions.topLevelItemCount()):
                version_items.append(self.ui.treeWidget_versions.topLevelItem(item))
        elif type == 'shot':
            for item in range(self.ui.treeWidget_animVersions.topLevelItemCount()):
                version_items.append(self.ui.treeWidget_animVersions.topLevelItem(item))
        for item in version_items:
            item.setText(1, '')
            with open(self.status_path, 'r') as statusfile_read:
                stat_read = json.load(statusfile_read)
            try:
                if stat_read[type][name]['default'] == item.text(0):
                    item.setText(1, 'Live')
            except KeyError:
                pass

            try:
                if stat_read[type][name]['shd'] == item.text(0):
                    item.setText(1, 'Live')
            except KeyError:
                pass

            try:
                if stat_read[type][name]['mtl'] == item.text(0):
                    item.setText(1, 'Live')
            except KeyError:
                pass

            try:
                if stat_read[type][name]['anim'] == item.text(0):
                    item.setText(1, 'Live')
            except KeyError:
                pass
            try:
                if stat_read[type][name]['cache'] == item.text(0):
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
            print result
            if result == 'animation':
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

        selected_asset = self.ui.listWidget_assets.currentItem().text()

        def getType():
            assettype = ''
            for dir in os.listdir(self.assets_root):
                for item in os.listdir(os.path.join(self.assets_root, dir)):
                    if selected_asset in item:
                        assettype = dir
            return assettype

        sel_assetroot = os.path.join(self.assets_root, getType(), 'dev', selected_asset)
        shd_path = os.path.join(sel_assetroot, 'shd')
        latest_assetver = fileUtils.getLatest(sel_assetroot, selected_asset)
        if os.path.exists(shd_path):
            if os.listdir(shd_path):
                latest_shdver = fileUtils.getLatest(shd_path, selected_asset)
                for shd_version in os.listdir(shd_path):
                    if latest_shdver in shd_version:
                        latest_shd = shd_version
                    else:
                        print '{0} not found'.format(latest_shdver)
            else:
                print '{0} is empty'.format(shd_path)
        else:
            print '{0} doesnt exist'.format(shd_path)
        for asset_version in os.listdir(sel_assetroot):
            if latest_assetver in asset_version:
                latest_asset = asset_version
            else:
                print '{0} not found'.format(latest_assetver)

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

myWin = myGui()

def run():
    myWin.run()