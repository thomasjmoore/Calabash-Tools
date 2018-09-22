from .lib.Qt import QtCore, QtGui, QtWidgets
from . import vrayUtils
from . import vray_toolboxUI as customUI
from maya import cmds
import pymel.core as pm

try:
    from shiboken import wrapInstance
except:
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

reload(vrayUtils)
reload(customUI)

__all__ = [
    'launch',
    ]

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class ControlMainWindow(QtWidgets.QDialog):
    version = "1.1"

    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.ui = customUI.Ui_vray_toolbox()
        self.ui.setupUi(self)

        self.ui.applyTo_btngrp = QtWidgets.QButtonGroup(self.ui.applyTo_hlyt)
        self.ui.applyTo_btngrp.addButton(self.ui.transforms_rbtn)
        self.ui.applyTo_btngrp.addButton(self.ui.shapes_rbtn)
        self.ui.selection_rbtn.setChecked(True)
        self.ui.shapes_rbtn.setChecked(True)

        self.ui.add_btn.clicked.connect(self.add_btn_clicked)
        self.ui.rem_bt.clicked.connect(self.remove_btn_clicked)

        self.ui.transforms_rbtn.clicked.connect(self.transforms_clicked)
        self.ui.shapes_rbtn.clicked.connect(self.transforms_clicked)

    def check_ui(self):
        selected = self.ui.selection_rbtn.isChecked()
        shapes = self.ui.shapes_rbtn.isChecked()

        commands = []
        if self.ui.subd_chk.isChecked():
            commands.append("vray_subdivision")
        if self.ui.subdDisp_chk.isChecked():
            commands.append("vray_subquality")
        if self.ui.disp_chk.isChecked():
            commands.append("vray_displacement")
        if self.ui.objID_chk.isChecked():
            commands.append("vray_objectID")
        if self.ui.openSubdiv_chk.isChecked():
            commands.append("vray_opensubdiv")

        return selected, shapes, commands

    def add_btn_clicked(self):
        selected, shapes, commands = self.check_ui()

        if not commands:
            return

        for c in commands:
            vrayUtils.vray_attributes(selected=selected, shapes=shapes, add=True, command=c)

    def remove_btn_clicked(self):
        selected, shapes, commands = self.check_ui()

        if not commands:
            return

        for c in commands:
            vrayUtils.vray_attributes(selected=selected, shapes=shapes, add=False, command=c)

    def transforms_clicked(self):
        is_checked = self.ui.transforms_rbtn.isChecked()
        if is_checked:
            self.ui.subd_chk.setDisabled(True)
            self.ui.subdDisp_chk.setDisabled(True)
            self.ui.disp_chk.setDisabled(True)
            self.ui.openSubdiv_chk.setDisabled(True)
            self.ui.subd_chk.setChecked(False)
            self.ui.subdDisp_chk.setChecked(False)
            self.ui.disp_chk.setChecked(False)
            self.ui.openSubdiv_chk.setChecked(False)
        else:
            self.ui.subd_chk.setEnabled(True)
            self.ui.subdDisp_chk.setEnabled(True)
            self.ui.disp_chk.setEnabled(True)
            self.ui.openSubdiv_chk.setEnabled(True)

##########################################

def launch():
    global dialog
    #if dialog is None:
    #    dialog = ControlMainWindow(parent=maya_main_window())

    #dialog.show()
    try:
        if dialog:
            delete()
    except:
        pass
    dialog = ControlMainWindow(parent=maya_main_window())
    dialog.show()

def delete():
    global dialog
    if dialog is None:
        return
    dialog.deleteLater()
    dialog = None
