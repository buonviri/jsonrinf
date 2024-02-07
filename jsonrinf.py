import os
import re
import pprint

double_quotes = '"“”'


def GetTokens(x):  # standard function for splitting strings containing quoted strings
    return [p for p in
        re.split("( |\\\".*?\\\"|'.*?')", x.strip()) if p.strip()]
# end of GetTokens()


def convert(lines):
    info = {}  # blank dict for storing all netlist info
    lastline = ''  # contains keyword of last line
    # list of words that aren't useful:
    badwords = {'.HEA': 'header',
                '.TIM': 'timestamp',
                '.APP': 'application',
                '.UNI': 'units',
                '.TYP': 'type',
                '.JOB': 'job',
                '.END': 'end',
                }
    # list of words that contain info:
    keywords = {'.ADD': 'add...',  # should be followed by _COM or _TER
                '.ATT': 'attribute',  # usually followed by _COM
                '.TER': 'pin',
                }
    device = 'UUU999'  # fake device
    pin = '123456'  # fake pin
    netname = 'HOMER SEZ NO NET (ERROR)'  # (hopefully) invalid netname
    for rawline in lines:
        line = rawline.strip().replace('\t',' ')  # strip newline and spaces, replace tab with space
        if len(line) == 0:
            pass  # do nothing with blanks lines
        elif line.startswith('#'):
            pass  # this line is a comment, same as in python
        elif line[0:4] in badwords:  # matches known bad word
            lastline = line[0:4]  # save for next loop
            try:
                info[line[0:4]].append(line[4:].strip().strip(double_quotes))  # try to append remainder of line to list
            except:
                info[line[0:4]] = [line[4:].strip().strip(double_quotes),]  # make new list
        elif line[0:4] in keywords:  # matches known keyword
            lastline = line[0:4]  # save for next loop
            if line.startswith('.ADD_TER'):
                words = GetTokens(line[8:].strip())
                device = words[0]
                pin = words[1]
                netname = words[2].strip(double_quotes)
                # note that words[3] *might* exist, as a comment
                print(device.ljust(10) + ' ' + pin.ljust(5) + ' ' + netname)
            elif line.startswith('.TER'):
                words = GetTokens(line[4:].strip())
                device = words[0]
                pin = words[1]
                # net name is inherited from earlier line
                # note that words[2] *might* exist, as a comment
                print(device.ljust(10) + ' ' + pin.ljust(5) + ' ' + netname)
        elif lastline == '.TER':  # special case, additional .TER lines don't need keyword
            words = GetTokens(line.strip())
            if len(words) > 1:  # should contain two or more words
                device = words[0]
                pin = words[1]
                # net name is inherited from earlier line
                # note that words[2] *might* exist, as a comment
                print(device.ljust(10) + ' ' + pin.ljust(5) + ' ' + netname)
            else:
                print('Bad line: ' + line)
        else:
            print('Bad line: ' + line)
    return info
# end of convert()


print()  # blank line to separate from prompt
for dirname, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        if filename.endswith('.frp'):
            name = os.path.join(dirname, filename[:-4])  # remove extension
            print('Writing: ' + name + '.dict')
            with open(name + '.frp', 'r') as f:
                info = convert(f.readlines())  # read entire file and pass as a list
            with open(name + '.dict', 'w') as f:
                f.write(pprint.pformat(info, indent=2))  # write using pformat
            print('Done.\n')
# end of main loop

os.system("PAUSE")
# EOF
