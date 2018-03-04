from ..lib.Qt import QtCore, QtGui, QtWidgets
import playblast_ui as customUI
from . import playblast_utils
from maya import cmds
import pymel.core as pm

try:
    from shiboken import wrapInstance
except:
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

reload(playblast_utils)
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
        self.playblaster = playblast_utils.Playblaster()
        self.setWindowFlags(QtCore.Qt.Tool)
        self.ui = customUI.Ui_playblast_dlg()
        self.ui.setupUi(self)

        # Setup GUI values
        title = self.ui.title_lbl.text()
        self.ui.title_lbl.setText("%s V%s" % (title, self.version))
        self.ui.filename_le.setText(self.playblaster.filename)
        self.ui.start_le.setText(str(self.playblaster.start))
        self.ui.end_le.setText(str(self.playblaster.end))
        self.ui.width_le.setText(str(self.playblaster.w))
        self.ui.height_le.setText(str(self.playblaster.h))
        self.ui.hud_chk.setChecked(self.playblaster.hud)
        self.ui.frameHud_chk.setChecked(self.playblaster.hud_frame_chk)
        self.ui.cstmHud_chk.setChecked(self.playblaster.custom_hud_chk)
        self.ui.clearViewport_chk.setChecked(self.playblaster.clean_vp)
        self.ui.green_chk.setChecked(self.playblaster.green)
        self.ui.filename_le.setEnabled(self.playblaster.editname)
        self.ui.overwrite_chk.setChecked(self.playblaster.overwrite)
        self.ui.offscreen_chk.setChecked(self.playblaster.offscreen)
        self.ui.cam_chk.setChecked(self.playblaster.hidecameragates)
        self.set_button_color()

        self.custom_hud_chk()
        self.green_chk()

        self.ui.filename_le.textChanged.connect(self.filename)
        self.ui.editName_chk.clicked.connect(self.editname)
        self.ui.overwrite_chk.clicked.connect(self.overwrite)
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
        self.ui.color_btn.clicked.connect(self.set_color)
        self.ui.loadRender_btn.clicked.connect(self.load_render)
        self.ui.reset_btn.clicked.connect(self.reset)

        self.get_custom_hud_text()

    def playblast(self):
        cmds.optionVar(sv=("pbCustomHud", self.ui.cstmHud_le.text()))
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
            self.ui.cstmHud_chk.setEnabled(True)
            self.ui.cstmHud_le.setEnabled(True)
        else:
            self.ui.cstmHud_chk.setDisabled(True)
            self.ui.cstmHud_le.setDisabled(True)

    def filename(self):
        self.playblaster.filename = self.ui.filename_le.text()

    def editname(self):
        is_checked = self.ui.editName_chk.checkState()
        if is_checked:
            self.ui.filename_le.setDisabled(False)
        else:
            self.ui.filename_le.setDisabled(True)

    def load_render(self):
        w, h = self.playblaster.render_resolution()
        self.ui.width_le.setText(w)
        self.ui.height_le.setText(h)

    def overwrite(self):
        self.playblaster.overwrite = self.ui.overwrite_chk.checkState()

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

    def custom_hud(self):
        self.playblaster.custom_hud_chk = self.ui.cstmHud_chk.checkState()

    def get_custom_hud_text(self):
        if cmds.optionVar(exists="pbCustomHud"):
            self.playblaster.custom_hud_text = cmds.optionVar(q="pbCustomHud")
        self.ui.cstmHud_le.setText(self.playblaster.custom_hud_text)

    def custom_hud_text(self):
        self.playblaster.custom_hud_text = self.ui.cstmHud_le.text()
        if self.ui.cstmHud_le.text():
            self.ui.cstmHud_chk.setChecked(True)
        else:
            self.ui.cstmHud_chk.setChecked(False)

    def clean_vp(self):
        self.playblaster.clean_vp = self.ui.clearViewport_chk.checkState()

    def green(self):
        self.playblaster.green = self.ui.green_chk.checkState()

    def set_button_color(self, color=None):
        # This function sets the color on the color picker button
        if not color:
            color = self.playblaster.default_color
        else:
            self.playblaster.default_color = color

        assert len(color) == 3, "You must provide a list of 3 colors"

        # Qt expects it in integer values from 0 to 255
        r, g, b = [c * 255 for c in color]

        self.ui.color_btn.setStyleSheet('background-color: rgba(%s, %s, %s, 1.0);' % (r, g, b))

    def set_color(self):

        color = self.playblaster.default_color

        # Then we provide this to the maya's color editor which gives us back the color the user specified
        color = pm.colorEditor(rgbValue=color)

        # Annoyingly, it gives us back a string instead of a list of numbers.
        # So we split the string, and then convert it to floats
        r, g, b, a = [float(c) for c in color.split()]

        # We then use the r,g,b to set the colors on the light and the button
        color = (r, g, b)

        self.set_button_color(color)

    def reset(self):
        cmds.optionVar(remove="pbCustomHud")
        launch()
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
