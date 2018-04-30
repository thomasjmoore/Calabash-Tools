from maya import cmds
from maya import OpenMaya as om
import os

cmds.evalDeferred('from calabash import calabash_menu')

def arnoldCheck(*args, **kwargs):
    if os.path.split(args[0][0])[-1] == "mtoa.mll":
        cmds.warning("arnold loading............................")
        cmds.confirmDialog(title='WARNING: ARNOLD IS LOADING', message='Arnold is being loaded.', button=['OK'],
                           defaultButton='OK')

arnoldCallback = om.MSceneMessage.addStringArrayCallback(om.MSceneMessage.kBeforePluginLoad, arnoldCheck)


