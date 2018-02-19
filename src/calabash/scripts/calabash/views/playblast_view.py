from ..lib.Qt import QtCore, QtGui, QtWidgets
import playblast_ui as customUI
from .. import playblast_utils
from maya import cmds

try:
    from shiboken import wrapInstance
except:
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

reload(playblast_utils)
reload(customUI)

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class ControlMainWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.playblaster = playblast_utils.Playblaster()
        self.setWindowFlags(QtCore.Qt.Tool)
        self.ui = customUI.Ui_playblast_dlg()
        self.ui.setupUi(self)

        self.ui.filename_le.setText(self.playblaster.filename)
        self.ui.start_le.setText(str(self.playblaster.start))
        self.ui.end_le.setText(str(self.playblaster.end))
        self.ui.width_le.setText(str(self.playblaster.w))
        self.ui.height_le.setText(str(self.playblaster.h))
        self.ui.hud_chk.setChecked(self.playblaster.hud)
        self.ui.cstmHud_chk.setChecked(self.playblaster.custom_hud_chk)
        self.ui.cstmHud_le.setText(self.playblaster.custom_hud_text)
        self.ui.clearViewport_chk.setChecked(self.playblaster.clean_vp)
        self.ui.green_chk.setChecked(self.playblaster.green)


        self.custom_hud_chk()
        self.green_chk()

        self.ui.filename_le.textChanged.connect(self.filename)
        self.ui.width_le.textChanged.connect(self.width)
        self.ui.height_le.textChanged.connect(self.height)
        self.ui.start_le.textChanged.connect(self.start)
        self.ui.end_le.textChanged.connect(self.end)
        self.ui.hud_chk.clicked.connect(self.hud)
        self.ui.cstmHud_chk.clicked.connect(self.custom_hud)
        self.ui.cstmHud_le.textChanged.connect(self.custom_hud_text)
        self.ui.clearViewport_chk.clicked.connect(self.clean_vp)
        self.ui.green_chk.clicked.connect(self.green)

        self.ui.playblast_btn.clicked.connect(self.playblast)
        self.ui.hud_chk.clicked.connect(self.custom_hud_chk)
        self.ui.green_chk.clicked.connect(self.green_chk)

    def playblast(self):
        self.playblaster.playblast()

    def green_chk(self):
        is_checked = self.ui.green_chk.checkState()
        if not is_checked:
            filename = self.playblaster.pb_filename()
            self.ui.filename_le.setText(filename)
            self.ui.cstmHud_chk.setDisabled(False)
            self.ui.cstmHud_le.setDisabled(False)
            self.ui.hud_chk.setDisabled(False)
            self.ui.clearViewport_chk.setDisabled(False)


        else:
            filename = self.playblaster.pb_filename()
            self.ui.filename_le.setText(filename)
            self.ui.cstmHud_chk.setDisabled(True)
            self.ui.cstmHud_le.setDisabled(True)
            self.ui.hud_chk.setDisabled(True)
            self.ui.clearViewport_chk.setDisabled(True)



    def custom_hud_chk(self):
        is_checked = self.ui.hud_chk.checkState()
        if is_checked:
            self.ui.cstmHud_chk.setDisabled(False)
            self.ui.cstmHud_le.setDisabled(False)
        else:
            self.ui.cstmHud_chk.setDisabled(True)
            self.ui.cstmHud_le.setDisabled(True)

    def filename(self):
        self.playblaster.filename = self.ui.filename_le.text()

    def height(self):
        self.playblaster.h = int(self.ui.height_le.text())

    def width(self):
        self.playblaster.w = int(self.ui.width_le.text())

    def start(self):
        self.playblaster.start = int(self.ui.start_le.text())

    def end(self):
        self.playblaster.end = int(self.ui.end_le.text())

    def hud(self):
        self.playblaster.hud = self.ui.hud_chk.checkState()

    def hud(self):
        self.playblaster.hud = self.ui.hud_chk.checkState()

    def custom_hud(self):
        self.playblaster.custom_hud_chk = self.ui.cstmHud_chk.checkState()

    def custom_hud_text(self):
        self.playblaster.custom_hud_text = self.ui.cstmHud_le.text()

    def clean_vp(self):
        self.playblaster.clean_vp = self.ui.clearViewport_chk.checkState()

    def green(self):
        self.playblaster.green = self.ui.green_chk.checkState()
#############################################################################################################


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
