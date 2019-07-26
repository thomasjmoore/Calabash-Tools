from __future__ import print_function
import os
import re
import fileinput
debug = False
def edit(animpath):
    repathed = []
    for rawline in fileinput.input(animpath, inplace=not debug):

        if '/assets/' in rawline:

            line = rawline.split()[-1]
            line = re.sub('[";]+', '', line)
            filepath, filename = os.path.split(line)

            basename = filepath.split('/scenes/')[-1]

            if debug: print(os.path.join(filepath, 'renderable', filename))
            if os.path.exists(os.path.join(filepath, 'renderable', filename)):
                renderablepath = os.path.normpath(os.path.join('scenes', basename, 'renderable', filename))
                renderablepath = renderablepath.replace('\\', '/')
                newline = rawline.replace(line, renderablepath)
                print(newline)
                repathed.append(newline)
            else:

                print(rawline)
        elif '//scenes' in rawline:

            line = rawline.split()[-1]
            line = re.sub('[";]+', '', line)
            basename, filename = os.path.split(line)

            basename = basename.split('//')[-1]

            renderablepath = os.path.normpath(os.path.join(basename, filename))
            renderablepath = renderablepath.replace('\\', '/')


            newline = rawline.replace(line, renderablepath)
            print(newline)
            repathed.append(newline)

        else:

            print(rawline)

    return repathed

# animpath = r"Z:\raid\3Dprojects\maya\projects\Lucky_Chariot\scenes\trackedElements\sh00\anim\trackedElements_sh00-props_anim.021.ma"
# edit(animpath)