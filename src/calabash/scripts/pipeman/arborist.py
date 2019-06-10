"""An arborist, tree surgeon, or arboriculturist, is a professional in the practice of arboriculture, which is the
 cultivation, management, and study of individual trees"""

 #  Arborist builds customized project directory and asset directory hierarchy trees

from collections import defaultdict
import os
import os.path

def createProject(projname, dest):
    #check if dest exists
    projpath = os.path.join(dest, projname)

    if os.path.exists(dest):
        if not os.path.exists(projpath):
            os.mkdir(projpath)
            proj_rootdirs = ['scenes',
                             'scenes/assets',
                             'images',
                             'sourceimages',
                             'sound',
                             'movies',
                             'cache/alembic',
                             'cache/nCache',
                             'cache/particles']

            workspace_str ="""
//Maya 2018 Project Definition

workspace -fr "fluidCache" "cache/nCache/fluid";
workspace -fr "images" "images";
workspace -fr "JT_ATF" "data";
workspace -fr "offlineEdit" "scenes/edits";
workspace -fr "STEP_ATF Export" "data";
workspace -fr "furShadowMap" "renderData/fur/furShadowMap";
workspace -fr "INVENTOR_ATF Export" "data";
workspace -fr "SVG" "data";
workspace -fr "scripts" "scripts";
workspace -fr "STL_ATF" "data";
workspace -fr "DAE_FBX" "data";
workspace -fr "shaders" "renderData/shaders";
workspace -fr "NX_ATF" "data";
workspace -fr "furFiles" "renderData/fur/furFiles";
workspace -fr "CATIAV5_ATF Export" "data";
workspace -fr "OBJ" "data";
workspace -fr "alembicCache" "cache/alembic";
workspace -fr "PARASOLID_ATF Export" "data";
workspace -fr "FBX export" "data";
workspace -fr "furEqualMap" "renderData/fur/furEqualMap";
workspace -fr "BIF" "data";
workspace -fr "DAE_FBX export" "data";
workspace -fr "CATIAV5_ATF" "data";
workspace -fr "SAT_ATF Export" "data";
workspace -fr "movie" "movies";
workspace -fr "ASS Export" "data";
workspace -fr "autoSave" "autosave";
workspace -fr "mayaAscii" "scenes";
workspace -fr "move" "data";
workspace -fr "NX_ATF Export" "data";
workspace -fr "sound" "sound";
workspace -fr "mayaBinary" "scenes";
workspace -fr "timeEditor" "Time Editor";
workspace -fr "DWG_ATF" "data";
workspace -fr "JT_ATF Export" "data";
workspace -fr "iprImages" "renderData/iprImages";
workspace -fr "FBX" "data";
workspace -fr "renderData" "renderData";
workspace -fr "CATIAV4_ATF" "data";
workspace -fr "fileCache" "cache/nCache";
workspace -fr "eps" "data";
workspace -fr "STL_ATF Export" "data";
workspace -fr "3dPaintTextures" "sourceimages/3dPaintTextures";
workspace -fr "translatorData" "data";
workspace -fr "mel" "scripts";
workspace -fr "particles" "cache/particles";
workspace -fr "scene" "scenes";
workspace -fr "SAT_ATF" "data";
workspace -fr "PROE_ATF" "data";
workspace -fr "WIRE_ATF Export" "data";
workspace -fr "sourceImages" "sourceimages";
workspace -fr "clips" "clips";
workspace -fr "furImages" "renderData/fur/furImages";
workspace -fr "INVENTOR_ATF" "data";
workspace -fr "STEP_ATF" "data";
workspace -fr "DWG_ATF Export" "data";
workspace -fr "depth" "renderData/depth";
workspace -fr "sceneAssembly" "sceneAssembly";
workspace -fr "IGES_ATF Export" "data";
workspace -fr "PARASOLID_ATF" "data";
workspace -fr "IGES_ATF" "data";
workspace -fr "teClipExports" "Time Editor/Clip Exports";
workspace -fr "ASS" "data";
workspace -fr "audio" "sound";
workspace -fr "bifrostCache" "cache/bifrost";
workspace -fr "Alembic" "data";
workspace -fr "illustrator" "data";
workspace -fr "diskCache" "data";
workspace -fr "WIRE_ATF" "data";
workspace -fr "templates" "assets";
workspace -fr "OBJexport" "data";
workspace -fr "furAttrMap" "renderData/fur/furAttrMap";
"""

            with open(os.path.join(projpath, 'workspace.mel'), 'w') as workspace_file:
                workspace_file.write(workspace_str)
            for dir in proj_rootdirs:
                rootdir_path = os.path.join(projpath, dir)
                os.makedirs(rootdir_path)

        else:
            print 'Project: {0}, already exists! \n {1}'.format(projname, projpath)
    else:
        print 'Project: {0}, destination does not exist \n'.format(dest)
    return

def createSpot(projpath, spotname, shotcount):

    spotpath = os.path.join(projpath, 'scenes', spotname)
    if not os.path.exists(spotpath):
        for shot in range(shotcount):
            shot += 1
            shotname = 'sh{0}0'.format(('%02d' % shot))
            animpath = os.path.join(spotpath, shotname, 'anim', 'publish')
            renderpath = os.path.join(spotpath, shotname, 'render')
            print animpath
            print renderpath
            os.makedirs(animpath)
            os.makedirs(renderpath)

    else:
        print 'Spot: {0}, already exists! \n {1}'.format(spotname, spotpath)

def createShot(projpath, shotname):
    shotpath = os.path.join(projpath, 'scenes', shotname)
    if not os.path.exists(shotpath):
        print shotpath
        os.makedirs(shotpath)
    else:
        print 'Shot: {0}, already exists! \n {1}'.format(shotname, shotpath)

def createAsset(projpath, type, assetname):
    #print 'projpath: {0}'.format(projpath)
    assetpath = os.path.join(projpath, 'scenes', 'assets', type, 'dev', assetname)
    if not os.path.exists(assetpath):
        assetdirs = ['publish', 'shd/publish']
        for dir in assetdirs:
            dirpath = os.path.join(assetpath, dir)
            print dirpath
            os.makedirs(dirpath)
    else:
        print 'Asset: {0}, already exists! \n {1}'.format(assetname, assetpath)


