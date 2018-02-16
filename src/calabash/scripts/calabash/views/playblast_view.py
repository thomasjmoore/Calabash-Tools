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
        self.setWindowFlags(QtCore.Qt.Tool)
        self.ui = customUI.Ui_playblast_dlg()
        self.ui.setupUi(self)
        self.setup()

        self.ui.playblast_btn.clicked.connect(self.playblast)


    def setup(self):
        filename = playblast_utils.pb_filename()
        start, end = playblast_utils.start_end()
        self.ui.filename_le.setText(filename)
        self.ui.start_le.setText(str(int(start)))
        self.ui.end_le.setText(str(int(end)))

    def playblast(self):
        filename = self.ui.filename_le.text()
        green = self.ui.green_chk.checkState()
        h = int(self.ui.height_le.text())
        w = int(self.ui.width_le.text())
        start = int(self.ui.start_le.text())
        end = int(self.ui.end_le.text())
        hud = self.ui.hud_chk.checkState()
        clean_vp = self.ui.clearViewport_chk.checkState()
        if self.ui.cstmHud_chk.checkState():
            custom_hud_text = self.ui.cstmHud_le.text()
        else:
            custom_hud_text = ""

        playblast_utils.playblast(filename=filename,
                                  green=green,
                                  h=h,
                                  w=w,
                                  start=start,
                                  end=end,
                                  hud=hud,
                                  clean_vp=clean_vp,
                                  custom_hud_text=custom_hud_text
                                  )

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
