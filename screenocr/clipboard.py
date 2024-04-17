'''
this code only work on windows, it use clip.exe to copy string/text to 
windows system clipboard. if you want to manipulate clipboard cross-platform
use pyperclip library.
'''

import subprocess

def copy_to_clipboard(string_to_copy):
    process = subprocess.Popen(
        ['clip.exe'],
        stdin=subprocess.PIPE,
        close_fds=True
    )
    process.communicate(input=string_to_copy.encode('Shift_JIS'))