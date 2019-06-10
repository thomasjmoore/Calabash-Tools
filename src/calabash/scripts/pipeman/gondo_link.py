import pymel.core as pm
from PySide2 import QtCore, QtUiTools, QtWidgets
from PySide2.QtGui import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as apiUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQDockWidget
import os
import re
import json
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

#import converted ui file.
import gondo_link_ui as ui_file


class myGui(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, shots, comp_root, comp_proj, complinks, parent=None):

        super(self.__class__, self).__init__(parent=parent)

        self.shots = shots
        self.comp_root = comp_root
        self.comp_proj = comp_proj
        self.complinks_path = complinks
        self.ui = ui_file.Ui_mainUI()
        self.ui.setupUi(self)

        #self.ui.pushButton_gondo_save.clicked.connect(self.savelinks)

        with open(self.complinks_path, 'r') as r:
            self.complinks = json.load(r)

        for spotshot in shots:
            self.make_link(spotshot)
        ######## CONNECT UI ELEMENTS AND FUNCTIONS BELOW HERE #########

    def savelink(self, spotshot, path):
        debug = False
        if debug: print 'Saving Link: shot={0}, path={1}'.format(spotshot, path)
        with open(self.complinks_path, 'w') as w:
            if not 'complinks' in self.complinks:
                self.complinks['complinks'] = {}
            self.complinks['complinks'][spotshot] = path
            json.dump(self.complinks, w, indent=4)

    def make_link(self, spotshot):
        spot, shot = spotshot.split('/')
        debug = False
        comp_path = os.path.join(self.comp_root, self.comp_proj)
        comp_input = os.path.join(comp_path, '{0}_Comp'.format(self.comp_proj), 'input')
        shot_input = os.path.join(comp_input, shot)
        layout = QtWidgets.QHBoxLayout()
        self.ui.verticalLayout_5.addLayout(layout)
        label = QtWidgets.QLabel(spot + '/' + shot)
        lineedit = QtWidgets.QLineEdit()
        try:
            lineedit.setText(self.complinks['complinks'][shot])
            if debug: print 'Saved path found'
        except:
            if debug: print 'saved complink fail'
            if os.path.exists(comp_input):
                for dir in os.listdir(comp_input):
                    pat = '{0}'.format(dir)
                    if os.path.exists(shot_input):
                        if debug: print 'Path Exists:', shot_input
                        lineedit.setText(shot_input)
                        self.savelink(spotshot, shot_input)
                        break
                    elif re.match( pat, shot):
                        if debug: print 'Pattern Match: {0}, {1}, {2}'.format(pat, dir, shot)
                        lineedit.setText(os.path.join(comp_input, dir))
                        self.savelink(spotshot, os.path.join(comp_input, dir))
                        break
            else:
                if debug: print 'No match:', dir, shot
                lineedit.setText('input not found')
        def browsepath():
            bpath = pm.fileDialog2(dir=comp_path, fileMode=2)
            if bpath:
                lineedit.setText(bpath[0])
                self.savelink(spotshot, bpath[0])

        browse = QtWidgets.QPushButton("Browse")
        browse.clicked.connect(browsepath)

        layout.addWidget(label)
        layout.addWidget(lineedit)
        layout.addWidget(browse)

        ######## CONNECT UI ELEMENTS AND FUNCTIONS ABOVE HERE #########

    def deleteControl(self, control):
        if pm.workspaceControl(control, q=True, exists=True):
            pm.workspaceControl(control, e=True, close=True)
            pm.deleteUI(control, control=True)

    def run(self):
        # Set Ui's name
        self.setObjectName('links_ui')
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