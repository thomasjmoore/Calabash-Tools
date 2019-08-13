from __future__ import print_function
import os
import re
import fileinput
debug = False
def edit(animpath):
    repathed = []
    projectpath = animpath.split('scenes')[0]
    if debug: print('Project Path:'), print(projectpath)
    for rawline in fileinput.input(animpath, inplace=not debug):

        if '-typ "maya' in rawline:

            line = rawline.split()[-1]
            line = re.sub('[";]+', '', line)
            filepath, filename = os.path.split(line)
            filepath = filepath.replace('//', '')
            if debug: print('filepath:', filepath)
            assetpath = filepath.split('scenes')[-1]
            if debug: print('assetpath:', assetpath)


            #renderablepath = os.path.normpath(os.path.join('scenes', assetpath, 'renderable', filename))
            renderablepath = 'scenes{0}/renderable/{1}'.format(assetpath, filename)
            if os.path.exists('{0}/{1}'.format(projectpath, renderablepath)):
                renderablepath = renderablepath.replace('\\', '/')
                newline = rawline.replace(line, renderablepath)
                print(newline)
                repathed.append((line, renderablepath))
            else:
                if debug: print('path does not exist', '{0}/{1}'.format(projectpath, renderablepath))
                print(rawline)
        elif '//scenes' in rawline:

            line = rawline.split()[-1]
            line = re.sub('[";]+', '', line)
            assetpath, filename = os.path.split(line)

            assetpath = assetpath.split('//')[-1]

            renderablepath = os.path.normpath(os.path.join(assetpath, filename))
            renderablepath = renderablepath.replace('\\', '/')


            newline = rawline.replace(line, renderablepath)
            if not debug: print(newline)
            repathed.append((line, renderablepath))

        else:

            if not debug: print(rawline)

    return repathed

# animpath = "C:/Users/guest1/Documents/maya/projects/Hatchimals_Season6/scenes/snowball/sh010/anim/publish/snowBall_sh010-2_anim.017.ma"
# print(edit(animpath))