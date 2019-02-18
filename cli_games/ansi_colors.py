

codes = {
    'reset': '0',
    'bold_on': '1',
    'italics_on': '3',
    'underline_on': '4',
    'inverse_on' : '7',
	'strikethrough_on': '9',
    'bold_off': '22',
    'italics_off': '23',
    'underline_off': '24',
    'inverse_off': '27',
    'strikethrough_off':'29',
    'fg_black':'30',
    'fg_red': '31',
    'fg_green': '32',
    'fg_yellow': '33',
    'fg_blue': '34',
    'fg_magenta': '35',
    'fg_cyan': '36',
    'fg_white': '37',
    'fg_default': '39',
    'bg_black':'40',
    'bg_red': '41',
    'bg_green': '42',
    'bg_yellow': '43',
    'bg_blue': '44',
    'bg_magenta': '45',
    'bg_cyan': '46',
    'bg_white': '47',
    'bg_default': '49'}

def colored(string, *args):
    #print("\033[31;1;42mHello") + "\033[0m"
    tbprinted = ['\033[']
    for i in range(len(args)):
        if i == len(args) - 1:
            tbprinted.append(codes[args[i]] + 'm')
        else:
            tbprinted.append(codes[args[i]] + ';')
    tbprinted.append(string)
    tbprinted.append('\033[0m')
    tbprinted = ''.join(tbprinted)
    return tbprinted

def options_list():
    options = []
    for option in codes:
        options.append(option)
    return options


