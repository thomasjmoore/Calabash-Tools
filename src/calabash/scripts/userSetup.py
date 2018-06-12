from maya import cmds
from maya import OpenMaya as om
import os

cmds.evalDeferred('from calabash import calabash_menu')

def arnoldCheck(*args, **kwargs):
    if os.path.split(args[0][0])[-1] == "mtoa.mll":
        cmds.warning("arnold loading............................")
        cmds.confirmDialog(title='WARNING: ARNOLD IS LOADING', message='Arnold is being loaded.', button=['OK'],
                           defaultButton='OK')

#arnoldCallback = om.MSceneMessage.addStringArrayCallback(om.MSceneMessage.kBeforePluginLoad, arnoldCheck)


from maya import mel

mel.eval('source "gpmenu";')
mel.eval('global string $gMainWindowMenu;')
mel.eval('global string $gmyTimelineMenu = \"TimeSlider|MainTimeSliderLayout|formLayout8|TimeSliderMenu\";')

mel.eval('global int $gMyMenuItemsTest;')
mel.eval('global int $gMyTimelineMenuItemsTest;')

mel.eval('global string $gGPMenuItemVar;')
mel.eval('global string $gMyTimelineMenuVariable;')

mel.eval('$gMyMenuItemsTest = 0;')
mel.eval('$gMyTimelineMenuItemsTest = 0;')
mel.eval('$gGPMenuItemVar = "";')
mel.eval('$gMyTimelineMenuVariable = "";')

mel.eval("evalDeferred(\"addMenuItemSafe($gMainWindowMenu, \\\"AddMyMenuItems\\\", \\\"gGPMenuItemVar\\\");\")")
mel.eval("evalDeferred(\"addMenuItemSafe($gmyTimelineMenu, \\\"AddMyTimelineMenuItems\\\", \\\"gMyTimelineMenuVariable\\\");\")")
