import pymel.core as pm
from PySide2 import QtCore, QtUiTools, QtWidgets
from PySide2.QtGui import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as apiUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQDockWidget
from functools import partial

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
import openAsset_ui as ui_file
reload(ui_file)

class myGui(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, latest, parent=None):

        super(self.__class__, self).__init__(parent=parent)

        self.ui = ui_file.Ui_mainUI()
        self.ui.setupUi(self)
        self.latest = latest
        self.pop_list()
        ######## CONNECT UI ELEMENTS AND FUNCTIONS BELOW HERE #########

        self.ui.pushButton_openSelected.clicked.connect(self.openSelected)

    def unsaved_confirm(self):
        result = pm.confirmBox(
            title='Unsaved Changes',
            message='This file contains unsaved changes, save before continuing?',
            button=['Yes', 'No', 'Cancel'],
            dismissString='Close'
        )
        return result

    def pop_list(self):

        for subname in self.latest:
            #print 'Creating Item:', subname
            subname_item = QtWidgets.QListWidgetItem(self.ui.subnamelist)
            subname_item.setText(subname)

    def openSelected(self):
        subname = self.ui.subnamelist.currentItem().text()
        #print subname, self.latest[subname]
        try:
            path = self.latest[subname]
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

        ######## CONNECT UI ELEMENTS AND FUNCTIONS ABOVE HERE #########

    def deleteControl(self, control):
        if pm.workspaceControl(control, q=True, exists=True):
            pm.workspaceControl(control, e=True, close=True)
            pm.deleteUI(control, control=True)

    def run(self):
        # Set Ui's name
        self.setObjectName('openAsset_ui')
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