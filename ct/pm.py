################################################################
# File: pm.py
# Title: PM (Private Message) Manager
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 0.0.3.0
# Bug report: https://github.com/asl97/ct.py
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

### Imports, Standard Modules

import re
import time
import random
import socket

### Variables, Custom & Non-Standard Modules

from . import register
from . import ts
from . import tm


class pm:

    def __init__(self):
        self.rbuf = b""
        self.wbuf = b""
