"""
Galvo Win Connection

Performs the required interactions with the Galvo backend through pyusb and libusb.
"""

import ctypes
import ctypes.wintypes as wintypes
from ctypes import windll

LPDWORD = ctypes.POINTER(wintypes.DWORD)
LPOVERLAPPED = wintypes.LPVOID
LPSECURITY_ATTRIBUTES = wintypes.LPVOID


class WinConnection:
    def __init__(self, channel):
        self.channel = channel
        self.timeout = 100
        self.handle = None
        self.DeviceIoControl_Fn = windll.kernel32.DeviceIoControl
        self.DeviceIoControl_Fn.argtypes = [
            wintypes.HANDLE,  # _In_          HANDLE hDevice
            wintypes.DWORD,  # _In_          DWORD dwIoControlCode
            wintypes.LPVOID,  # _In_opt_      LPVOID lpInBuffer
            wintypes.DWORD,  # _In_          DWORD nInBufferSize
            wintypes.LPVOID,  # _Out_opt_     LPVOID lpOutBuffer
            wintypes.DWORD,  # _In_          DWORD nOutBufferSize
            LPDWORD,  # _Out_opt_     LPDWORD lpBytesReturned
            LPOVERLAPPED,
        ]  # _Inout_opt_   LPOVERLAPPED lpOverlapped
        self.CreateMutexW_Fn = windll.kernel32.CreateMutexW
        self.CreateMutexW.argtypes = [
            LPSECURITY_ATTRIBUTES,  # _In_opt_      LPSECURITY_ATTRIBUTES lpSecurityAttributes
            wintypes.DWORD,  # _In_          DWORD dwCreationDisposition
            wintypes.HANDLE]  # _In_opt_      HANDLE hTemplateFile
        self.CreateFile_Fn.restype = wintypes.HANDLE

    def open(self, handle, data):
        self.handle = windll.kernel32.CreateMutexW(LPSECURITY_ATTRIBUTES, 0, "Mio_MutexDevio")

    def close(self):
        windll.kernel32.CloseHandle(self.handle)

    def command(self, handle, data):
        dwBytesReturned = wintypes.DWORD(0)
        lpBytesReturned = ctypes.byref(dwBytesReturned)
        outbuf = None
        status = self.DeviceIoControl_Fn(
            handle, 0x99982010, data, 0xC, outbuf, 6, lpBytesReturned, None
        )
        return status

    def send_list(self, handle, data):
        dwBytesReturned = wintypes.DWORD(0)
        lpBytesReturned = ctypes.byref(dwBytesReturned)
        outbuf = None
        status = self.DeviceIoControl_Fn(
            handle, 0x99982018, data, 0xC00, outbuf, 6, lpBytesReturned, None
        )
        return status
