from maya import cmds


def test_func():
    obj = cmds.ls()
    for o in obj:
        print o