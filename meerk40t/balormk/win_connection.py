"""
Galvo Win Connection

Performs the required interactions with the Galvo backend through pyusb and libusb.
"""


class WinConnection:
    def __init__(self, channel):
        self.channel = channel
        self.devices = {}
        self.interface = {}
        self.backend_error_code = None
        self.timeout = 100
