import urllib2
import maya.cmds as cmds
import maya.mel as mel
import os
from os import listdir
from os.path import isfile, join
import zipfile
import shutil

temp = cmds.internalVar(utd=True)
this_path = os.path.normpath(os.path.dirname(__file__))
this_file = os.path.splitext(os.path.basename(__file__))
script_path = os.path.dirname(this_path)


def check_version():
    version_file = os.path.join(script_path, 'version.md')
    update_version = False

    version_url = 'https://raw.githubusercontent.com/thomasjmoore/Calabash-Tools/master/src/calabash/scripts/version.md'
    read_version = urllib2.urlopen(version_url).read()
    read_version = int(read_version[-3:])

    version_check = os.path.isfile(version_file)

    if version_check:
        current_version = open(version_file, 'r').read()
        current_version = int(current_version[-3:])

        if current_version < read_version:
            update_version = True

    else:
        update_version = True

    return update_version


def download():
    url = 'https://github.com/thomasjmoore/Calabash-Tools/archive/master.zip'
    download_file = "master.zip"
    file_name = os.path.join(temp, download_file)
    fileWrite = open(file_name, 'w')
    fileWrite.write(urllib2.urlopen(url).read())
    fileWrite.close()

    return file_name


def install(zip_file=""):
    print zip_file
    print script_path
    calabash_path = os.path.dirname(script_path)
    module_path = os.path.dirname(calabash_path)


    if os.path.exists("%s.mod"%(calabash_path)):
        os.remove("%s.mod"%(calabash_path))

    if os.path.exists(calabash_path):
        shutil.rmtree(calabash_path)


    zipname = os.path.splitext(zip_file)
    unzipped_files = os.path.join(zipname[0], "Calabash-Tools-master", "src")

    if os.path.exists(unzipped_files):
        shutil.rmtree(unzipped_files)
    zip = zipfile.ZipFile(zip_file)
    zip.extractall(zipname[0])

    print unzipped_files
    print os.path.exists("%s%s%s.mod"%(unzipped_files, os.path.sep,"calabash"))
    print ("%s%s%s.mod"%(calabash_path, os.path.sep,"calabash"))
    print os.path.exists("%s%s%s"%(unzipped_files, os.path.sep,"calabash"))
    print ("%s%s%s"%(calabash_path, os.path.sep,"calabash"))
    shutil.copy2("%s%s%s.mod"%(unzipped_files, os.path.sep,"calabash"), "%s%s%s.mod"%(module_path, os.path.sep,"calabash"))
    shutil.copytree("%s%s%s"%(unzipped_files, os.path.sep,"calabash"), "%s%s%s"%(module_path, os.path.sep,"calabash"))

def check():
    update = check_version()
    if not update:
        print("Tool up to date")
        return

    print("Update found")
    zip_file = download()

    if not zip_file:
        cmds.warning("Download unsuccesful")
        return

    install(zip_file)