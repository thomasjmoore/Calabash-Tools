# HotShot
# Shot syncing tool
# By Thomas Moore

import warnings
from ..lib import libJson

# json file stores shot name, start frame, and end frame

# keep maya separate


class hotShot():
    shot_file = ""
    shots = {}

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


    def edit_shot(self, shot=""):
        pass


    def remove_shot(self, shot=""):
        pass


    def save_shots(self):
        if not self.shot_file:
            warnings.warn("No shot file provided.")
            return

        libJson.write_json_file(self.shots, self.shotfile)