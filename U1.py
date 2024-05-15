import ast
import pyperclip

refdes = 'U19'  # needs to check filename instead
info_text = pyperclip.paste()
info = ast.literal_eval(info_text)

pins = []
for net in info['nets']:
    for node in info['nets'][net]:
        if node[0] == refdes:
            pins.append(node[1] + '\t' + net)
        else:
            pass
            # print(node)

pinstring = '\n'.join(pins)
print(pinstring)
print('\nPin count: ' + str(len(pins)))
pyperclip.copy(pinstring)

# EOF
