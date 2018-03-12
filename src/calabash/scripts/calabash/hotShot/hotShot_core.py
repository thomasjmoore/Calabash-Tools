# HotShot
# Shot syncing tool
# By Thomas Moore

import warnings
from ..lib import libJson
import os

from maya import OpenMayaAnim as oma
from maya import OpenMaya as om
from maya import cmds
from pymel import core as pm


# json file stores shot name, start frame, and end frame

# keep maya separate


class hotShot():
    shot_file = ""
    shot_name = ""
    shots = {}
    start = ""
    end = ""
    software = "maya"

    def __init__(self):
        pass

    def read_shot_file(self):
        if not self.shot_file:
            warnings.warn("No shot file provided.")
            return

        self.shots = libJson.read_json_file(self.shot_file)

        return self.shots

    def add_shot(self, shot=""):
        pass

    def save_shot_file(self, shot=""):
        if not self.shots:
            warnings.warn("No data to write.")
            return

        libJson.write_json_file(self.shots, self.shot_file)


    def remove_shot(self, shot=""):
        pass

    def save_shots(self):
        if not self.shot_file:
            warnings.warn("No shot file provided.")
            return

        libJson.write_json_file(self.shots, self.shotfile)

    def set_software(self, software=""):
        self.software = software

        if self.software == "maya":
            print "importing maya"
            from maya import OpenMayaAnim as oma

    def get_current_shot(self):
        if self.software == "maya":
            current_file = cmds.file(location=True, query=True)
        elif self.software == "nuke":
            pass

        path, file = os.path.split(current_file)
        self.shot_name = file.split("_")[0]

        return self.shot_name

    def get_shot_settings(self):
        self.read_shot_file()

        for i in self.shots:
            if i == self.shot_name:
                self.start = self.shots[i]["start"]
                self.end = self.shots[i]["end"]

        # Bring up prompt if new shot settings do not match current shot settings
        # Ask if user wants shot to be updated
        # If yes: apply shot settings

    def current_shot_settings(self):
        difference = False
        if self.software == "maya":
            # GET timeline start frame, end frame, and render start/end frame
            cur_start = int(oma.MAnimControl.minTime().value())
            cur_end = int(oma.MAnimControl.maxTime().value())
            cur_render_start = int(cmds.getAttr("defaultRenderGlobals.startFrame"))
            cur_render_end = int(cmds.getAttr("defaultRenderGlobals.endFrame"))

            print cur_start == int(self.start)
            # COMPARE with new values
            # IF difference found, set return difference TRUE

            if (not cur_start == int(self.start) or
                not cur_render_start == int(self.start) or
                not cur_end == int(self.end) or
                not cur_render_end == int(self.end)):
                    difference = True

            apply_settings = False

            if difference:
                update = cmds.confirmDialog(
                    message="Updated Shot Settings Found for SHOT: %s.\nCurrent Start/End: %s, %s;\nCurrent Render Start/End: %s, %s;\nNew Start/End: %s, %s"
                            % (self.shot_name, cur_start, cur_end, cur_render_start, cur_render_end, self.start, self.end),
                    title="Update Settings?", button=["Update?", "Cancel"], defaultButton="Update?",
                    cancelButton="Cancel")
                if update == "Update?":
                    apply_settings = True
                if update == "Cancel":
                    print "Action Cancelled"
            else:
                print "Shot settings are up to date."
            return apply_settings

    def apply_shot_settings(self):
        if self.software == "maya":

            # set start timeline/render settings
            # set end timeline/render settings
            start = oma.MAnimControl.setMinTime(om.MTime(int(self.start)))

            end = oma.MAnimControl.setMaxTime(om.MTime(int(self.end)))
            oma.MAnimControl.setAnimationStartEndTime(om.MTime(int(self.start)), om.MTime(int(self.end)))
            cmds.setAttr("defaultRenderGlobals.startFrame", self.start)
            cmds.setAttr("defaultRenderGlobals.endFrame", self.end)


def test_func():
    my_hotShot = hotShot()

    my_hotShot.shot_file = "%s%sshots.json" % (get_proj(), os.path.sep)
    print my_hotShot.shot_file
    my_hotShot.set_software("maya")
    my_hotShot.shot_name = my_hotShot.get_current_shot()
    my_hotShot.get_shot_settings()
    apply_settings = my_hotShot.current_shot_settings()

    if apply_settings:
        my_hotShot.apply_shot_settings()

def get_proj():
    curProj = cmds.workspace(fn=True, q=True)

    return curProj