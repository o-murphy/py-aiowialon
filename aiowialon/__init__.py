#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import flags

from .api import Wialon, WialonError, WialonEvents, WialonEvent
# Silence potential warnings from static analysis tools:
assert Wialon
assert WialonError

__author__ = "o-murphy"
__copyright__ = ("Copyright 2013-2016, Gurtam; ",)

__credits__ = ["Alex Chernetsky", "Aleksey Shmigelski", "Mike Turchunovich"]
__version__ = "1.2.1"

__all__ = ["Wialon"]
