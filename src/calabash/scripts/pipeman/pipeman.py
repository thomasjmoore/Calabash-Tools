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

        self.proj_path = pm.system.Workspace.getPath()
        self.scenes_root = os.path.join(self.proj_path, 'scenes')
        self.spots = self.getSpots()
        self.assets_root = os.path.join(self.scenes_root, 'assets')
        self.status_path = os.path.join(self.scenes_root, 'status.json')
        self.ui.tabWidget_pipeman.setCurrentIndex(0)

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
        self.ui.treeWidget_assets.itemClicked.connect(self.pop_assetVersions)
        self.ui.treeWidget_versions.itemClicked.connect(self.showcomment_asset)
        self.ui.listWidget_shots.itemClicked.connect(self.pop_shotVersions)
        self.ui.pushButton_makelive.clicked.connect(self.makelive_assets)

        self.ui.pushButton_makelive.customContextMenuRequested.connect(self.on_context_menu)
        self.popMenu_assetlive = QtWidgets.QMenu(self)
        self.popMenu_assetlive.addAction(QtWidgets.QAction('Make all latest Live', self))
        self.popMenu_assetlive.triggered.connect(self.makelive_assets_all)

        self.ui.pushButton_anim_makelive.clicked.connect(self.makelive_shots)
        self.ui.pushButton_anim_openlatest.clicked.connect(self.open_latest_shot)
        self.ui.pushButton_asset_openlatest.clicked.connect(self.open_latest_asset)
        self.ui.pushButton_arb_exe.clicked.connect(self.run_arborist)
        self.ui.pushButton_arb_projBrowse.clicked.connect(self.setarbProj)

        if not os.path.isfile(self.status_path):
            self.make_statusfile(self.status_path)

    def on_context_menu(self, point):
        self.popMenu_assetlive.exec_(self.ui.pushButton_makelive.mapToGlobal(point))

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
                        assets[assetname] = {'path':os.path.normpath(asset_path),"type":asset_type}
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

        type_items = []
        topItem_anim = QtWidgets.QTreeWidgetItem()
        topItem_anim.setText(0, 'Animation')
        type_items.append(topItem_anim)

        topItem_cache = QtWidgets.QTreeWidgetItem()
        topItem_cache.setText(0, 'Cache')
        type_items.append(topItem_cache)

        self.ui.treeWidget_animVersions.addTopLevelItems(type_items)


        for version in self.getVersions_shot(self.getShots()[spot][shot]):
            basename, ver, ext = version.split('.')
            shotname = '_'.join(basename.split('_')[:-1])
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
        asset_types = set()
        for asset in self.getAssets():
            asset_type = self.getAssets()[asset]['type']
            asset_types.add(asset_type)
        asset_types = list(asset_types)
        for itemtype in asset_types:
            type_item = QtWidgets.QTreeWidgetItem()
            type_item.setText(0, itemtype)
            self.ui.treeWidget_assets.addTopLevelItem(type_item)
        for asset in self.getAssets():
            asset_type = self.getAssets()[asset]['type']
            asset_type_item = self.ui.treeWidget_assets.findItems(asset_type, 0)[0]
            asset_item = QtWidgets.QTreeWidgetItem(asset_type_item)
            asset_item.setText(0, asset)

    def pop_assetVersions(self):
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
        except KeyError:
            pass

    def make_statusfile(self, statusfile_path):
        with open(statusfile_path, 'w') as statusfile:
            default_content = {'asset':{},
                               'shot':{}
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
            if stat_read.has_key(assetType):
                if stat_read[assetType].has_key(name):
                    if stat_read[assetType][name].has_key(state):

                        if type(stat_read[assetType][name][state]) == 'unicode':
                            stat_read[assetType][name][state] = {stat_read[assetType][name][state]}

                        stat_read[assetType][name][state][basename] = version

                    else:
                        stat_read[assetType][name][state] = {}
                        stat_read[assetType][name][state] = {basename:version}
                else:
                    stat_read[assetType][name] = {state:{basename:version}}
            else:
                stat_read[assetType] = {name:{state:{basename:version}}}


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

    def run_arborist(self):
        projectDest = self.ui.lineEdit_arb_projPath.text()
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
        self.show(dockable=True, floating=True)
        # not sure what e argument means
        pm.workspaceControl(workspaceControlName, e=True, ih=150)

myWin = myGui()

def run():
    myWin.run()

def test():
    return 'hello World!'