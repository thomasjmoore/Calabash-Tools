# #*********************************************************************
# content   = Utility for reading and writing json files
# version   = 0.1.0
# date      = 2017-09-30
#
# license   = MIT
# copyright = Copyright 2017 Thomas Moore
# author    = Thomas Moore <moore.thomasj@gmail.com>
# #*********************************************************************

import json

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


def write_json_file(dataToWrite, filename):
    if ".json" not in filename:
        filename += ".json"

    print "> write to json file is seeing: {0}".format(filename)

    with open(filename, "w") as jsonFile:
        json.dump(dataToWrite, jsonFile, indent=2)

    print "Data was successfully written to {0}".format(filename)

    return filename


def read_json_file(filename):
    if ".json" not in filename:
        filename += ".json"
    try:
        with open(filename, 'r') as jsonFile:
            return json.load(jsonFile)
    except:
        raise OSError('STOP PROCESS', "Could not read {0}".format(filename))