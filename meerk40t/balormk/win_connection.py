"""
Galvo Win Connection

Performs the required interactions with the Galvo backend through pyusb and libusb.
"""

import ctypes
import ctypes.wintypes as wintypes
from ctypes import windll

LPDWORD = ctypes.POINTER(wintypes.DWORD)
LPOVERLAPPED = wintypes.LPVOID


class WinConnection:
    def __init__(self, channel):
        self.channel = channel
        self.devices = {}
        self.interface = {}
        self.backend_error_code = None
        self.timeout = 100
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
