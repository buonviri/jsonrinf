import os
import ast
import pyperclip

suppress_all = True


def GetAttr(attrlist, attrname):
    for keyvalue in attrlist:
        if keyvalue[0] == attrname:  # key
            return keyvalue[1]  # value
    return ''
# End


target = os.path.basename(__file__).split('.')[0]  # get script name without extension

info_text = pyperclip.paste()
info = ast.literal_eval(info_text)

clip = ''
for refdes in info['comps']:
    if 'attributes' in info['comps'][refdes]:
        a = GetAttr(info['comps'][refdes]['attributes'], target)
        if a == '':
            pass  # attribute not found, or value was blank
        elif suppress_all and a == 'ALL':
            pass  # doesn't really do anything anyway
        else:
            print(refdes + ": " + a)
            clip = clip + refdes + '\t' + a + '\n'  # tab data for pasting into spreadsheet
pyperclip.copy(clip)

print()
os.system("PAUSE")
# EOF
