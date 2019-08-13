import pymel.core as pm
from PySide2 import QtCore, QtUiTools, QtWidgets
from PySide2.QtGui import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as apiUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQDockWidget
from functools import partial
import os
import shutil
import json

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

#import converted ui file.
import retrofit_ui as ui_file


class myGui(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, change_list, parent=None):

        super(self.__class__, self).__init__(parent=parent)

        self.ui = ui_file.Ui_mainUI()
        self.ui.setupUi(self)

        ######## CONNECT UI ELEMENTS AND FUNCTIONS BELOW HERE #########

        self.ui.pushButton_continue.clicked.connect(partial(self.engageRetro, change_list))
        self.ui.pushButton_cancel.clicked.connect(partial(self.deleteControl, 'retrofit_uiWorkspaceControl'))
        change_str = ''
        for action, src, dst in change_list:
            change_str = change_str + '({0} : {1} >>>>> {2})\n'.format(action, src, dst)
        self.ui.changes.setPlainText(change_str)
        self.ui.changes.setReadOnly(True)
        self.cnt = 0
        self.total = len(change_list)

    def recursive_copy(self, src, dst):
        debug = False
        if debug: print 'src:', src, 'dst:', dst
        if src != '.mayaSwatches':
            if os.path.isfile(src):
                if debug: print '{0} is file, moving'.format(src)
                shutil.move(src, dst)
            elif os.path.isdir(src):
                if debug: print '{0} is directory, diving in...'.format(src)
                for item in os.listdir(src):
                    dir = src.split('\\')[-1]
                    if debug: print 'src dir:', dir
                    new_dst = os.path.join(dst, dir)
                    new_src = os.path.join(src, item)
                    self.recursive_copy(new_src, new_dst)

    def modifyChangelog(self, src):
        with open(src, 'r') as logread:
            log = json.load(logread)
        newlog = {}
        for version in log:
            subname = version.split('.')[0]
            timestamp = log[version]['timestamp']
            comment = log[version]['comment']
            newlog[subname] = {version:[[timestamp, comment]]}
        with open(src, 'w') as logwrite:
            json.dump(newlog, logwrite)

    def engageRetro(self, change_list):
        print 'committing changes'
        remove_paths = []
        for action, src, dst in change_list:
            if action == 'move':
                self.recursive_copy(src, dst)
            elif action == 'remove':
                remove_paths.append(src)
            elif action == 'modify':
                self.modifyChangelog(src)
            self.cnt += 1

            print '{0}% Complete'.format((float(self.cnt)/self.total) * 100)
        for path in remove_paths:
            shutil.rmtree(path)
        self.deleteControl('retrofit_uiWorkspaceControl')

        ######## CONNECT UI ELEMENTS AND FUNCTIONS ABOVE HERE #########

    def deleteControl(self, control):
        if pm.workspaceControl(control, q=True, exists=True):
            pm.workspaceControl(control, e=True, close=True)
            pm.deleteUI(control, control=True)

    def run(self):
        # Set Ui's name
        self.setObjectName('retrofit_ui')
        # Explictly define workspacecontrol name
        workspaceControlName = self.objectName() + 'WorkspaceControl'
        # delete existing controls
        self.deleteControl(workspaceControlName)
        # show as floating window initially, last position and float state is retained between execution
        self.show(dockable=True, floating=True)
        # not sure what e argument means
        pm.workspaceControl(workspaceControlName, e=True, ih=150)

# myWin = myGui()
# myWin.run()