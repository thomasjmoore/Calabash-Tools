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
            basename, filename = os.path.split(line)
            renderablepath = os.path.normpath(os.path.join(basename, 'renderable', filename))
            renderablepath = renderablepath.replace('\\', '/')
            if os.path.isfile(renderablepath):
                newline = rawline.replace(line, renderablepath)
                print(newline)
                repathed.append(newline)
            else:
                print(rawline)
        else:
            print(rawline)

    return repathed