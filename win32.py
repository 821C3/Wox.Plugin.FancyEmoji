####
# Copy to clipboard function (put) compatible with x64 from https://forums.autodesk.com/t5/maya-programming/ctypes-bug-cannot-copy-data-to-clipboard-via-python/td-p/9195866
import ctypes
from ctypes import wintypes
import time

CF_UNICODETEXT = 13

user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32')

OpenClipboard = user32.OpenClipboard
OpenClipboard.argtypes = wintypes.HWND,
OpenClipboard.restype = wintypes.BOOL
CloseClipboard = user32.CloseClipboard
CloseClipboard.restype = wintypes.BOOL
EmptyClipboard = user32.EmptyClipboard
EmptyClipboard.restype = wintypes.BOOL
GetClipboardData = user32.GetClipboardData
GetClipboardData.argtypes = wintypes.UINT,
GetClipboardData.restype = wintypes.HANDLE
SetClipboardData = user32.SetClipboardData
SetClipboardData.argtypes = (wintypes.UINT, wintypes.HANDLE)
SetClipboardData.restype = wintypes.HANDLE

GlobalLock = kernel32.GlobalLock
GlobalLock.argtypes = wintypes.HGLOBAL,
GlobalLock.restype = wintypes.LPVOID
GlobalUnlock = kernel32.GlobalUnlock
GlobalUnlock.argtypes = wintypes.HGLOBAL,
GlobalUnlock.restype = wintypes.BOOL
GlobalAlloc = kernel32.GlobalAlloc
GlobalAlloc.argtypes = (wintypes.UINT, ctypes.c_size_t)
GlobalAlloc.restype = wintypes.HGLOBAL
GlobalSize = kernel32.GlobalSize
GlobalSize.argtypes = wintypes.HGLOBAL,
GlobalSize.restype = ctypes.c_size_t

GMEM_MOVEABLE = 0x0002
GMEM_ZEROINIT = 0x0040

unicode = type(u'')

def put(s):
    if not isinstance(s, unicode):
        s = s.decode('mbcs')
    data = s.encode('utf-16le')
    OpenClipboard(None)
    EmptyClipboard()
    handle = GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, len(data) + 2)
    pcontents = GlobalLock(handle)
    ctypes.memmove(pcontents, data, len(data))
    GlobalUnlock(handle)
    SetClipboardData(CF_UNICODETEXT, handle)
    CloseClipboard()
######

###Following was used to input selected Emoji, not used anymore because to slow
# Adding the inut feature will require some mire brainstorming

# directkeys.py
# http://stackoverflow.com/questions/13564851/generate-keyboard-events
# msdn.microsoft.com/en-us/library/dd375731
# https://gist.github.com/Aniruddha-Tapas/1627257344780e5429b10bc92eb2f52a
#INPUT_MOUSE    = 0
#INPUT_KEYBOARD = 1
#INPUT_HARDWARE = 2

# KEYEVENTF_EXTENDEDKEY = 0x0001
# KEYEVENTF_KEYUP       = 0x0002
# KEYEVENTF_UNICODE     = 0x0004
# KEYEVENTF_SCANCODE    = 0x0008

# MAPVK_VK_TO_VSC = 0

# List of all codes for keys:
# # msdn.microsoft.com/en-us/library/dd375731
#CTRL = 0x11
#V = 0x56
#ALT = 0x12
#TAB = 0x09


# # C struct definitions

# wintypes.ULONG_PTR = wintypes.WPARAM

# class MOUSEINPUT(ctypes.Structure):
#     _fields_ = (("dx",          wintypes.LONG),
#                 ("dy",          wintypes.LONG),
#                 ("mouseData",   wintypes.DWORD),
#                 ("dwFlags",     wintypes.DWORD),
#                 ("time",        wintypes.DWORD),
#                 ("dwExtraInfo", wintypes.ULONG_PTR))

# class KEYBDINPUT(ctypes.Structure):
#     _fields_ = (("wVk",         wintypes.WORD),
#                 ("wScan",       wintypes.WORD),
#                 ("dwFlags",     wintypes.DWORD),
#                 ("time",        wintypes.DWORD),
#                 ("dwExtraInfo", wintypes.ULONG_PTR))

#     def __init__(self, *args, **kwds):
#         super(KEYBDINPUT, self).__init__(*args, **kwds)
#         # some programs use the scan code even if KEYEVENTF_SCANCODE
#         # isn't set in dwFflags, so attempt to map the correct code.
#         if not self.dwFlags & KEYEVENTF_UNICODE:
#             self.wScan = user32.MapVirtualKeyExW(self.wVk,
#                                                  MAPVK_VK_TO_VSC, 0)

# class HARDWAREINPUT(ctypes.Structure):
#     _fields_ = (("uMsg",    wintypes.DWORD),
#                 ("wParamL", wintypes.WORD),
#                 ("wParamH", wintypes.WORD))

# class INPUT(ctypes.Structure):
#     class _INPUT(ctypes.Union):
#         _fields_ = (("ki", KEYBDINPUT),
#                     ("mi", MOUSEINPUT),
#                     ("hi", HARDWAREINPUT))
#     _anonymous_ = ("_input",)
#     _fields_ = (("type",   wintypes.DWORD),
#                 ("_input", _INPUT))

# LPINPUT = ctypes.POINTER(INPUT)

# def _check_count(result, func, args):
#     if result == 0:
#         raise ctypes.WinError(ctypes.get_last_error())
#     return args

# user32.SendInput.errcheck = _check_count
# user32.SendInput.argtypes = (wintypes.UINT, # nInputs
#                              LPINPUT,       # pInputs
#                              ctypes.c_int)  # cbSize

# # Functions

# def PressKey(hexKeyCode):
#     x = INPUT(type=INPUT_KEYBOARD,
#               ki=KEYBDINPUT(wVk=hexKeyCode))
#     user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

# def ReleaseKey(hexKeyCode):
#     x = INPUT(type=INPUT_KEYBOARD,
#               ki=KEYBDINPUT(wVk=hexKeyCode,
#                             dwFlags=KEYEVENTF_KEYUP))
#     user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

# 
# def PressAltTab():
#     PressKey(ALT)
#     PressKey(TAB)
#     ReleaseKey(ALT)
#     ReleaseKey(TAB)