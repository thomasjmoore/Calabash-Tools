import pymel.core as pm
import maya.cmds as cmds
from PySide2 import QtCore, QtUiTools, QtWidgets
from PySide2.QtGui import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as apiUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQDockWidget
import overscan_ui as ui_file
reload(ui_file)

class myGui(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent=parent)

        self.ui = ui_file.Ui_mainUI()
        self.ui.setupUi(self)

        self.vrsettings = pm.PyNode('vraySettings')

        self.ui.uniform_getres.clicked.connect(self.getres)
        self.ui.uniform_set.clicked.connect(self.setOverscan)


    def getres(self):

        frame_width = str(self.vrsettings.getAttr('width'))
        frame_height = str(self.vrsettings.getAttr('height'))
        self.ui.uniform_width.setText(frame_width)
        self.ui.uniform_height.setText(frame_height)

    def setOverscan(self):
        if self.ui.uniform_camera.text():
            camera = pm.PyNode(self.ui.uniform_camera.text())
            overscan = float(self.ui.uniform_overscan.text())
            frame_width = int(self.ui.uniform_width.text())
            frame_height = int(self.ui.uniform_height.text())
            self.vrsettings.setAttr('aspectLock', 0)
            self.vrsettings.setAttr('width', frame_width*overscan)
            self.vrsettings.setAttr('height', frame_height*overscan)
            self.vrsettings.setAttr('aspectLock', 1)
            camera.setAttr('cameraScale', overscan)

        else:
            print 'No Camera Specified!'

    ######## CONNECT UI ELEMENTS AND FUNCTIONS ABOVE HERE #########

    def deleteControl(self, control):
        if pm.workspaceControl(control, q=True, exists=True):
            pm.workspaceControl(control, e=True, close=True)
            pm.deleteUI(control, control=True)

    def run(self):
        # Set Ui's name
        self.setObjectName('overscan_ui')
        # Explictly define workspacecontrol name
        workspaceControlName = self.objectName() + 'WorkspaceControl'
        # delete existing controls
        self.deleteControl(workspaceControlName)
        # show as floating window initially, last position and float state is retained between execution
        self.show(dockable=True, floating=False)
        # not sure what e argument means
        pm.workspaceControl(workspaceControlName, e=True, ih=150)

ovrscan = myGui()

def run():
    ovrscan.run()