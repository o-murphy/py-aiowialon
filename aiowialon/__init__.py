#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import flags

from .api import Wialon, WialonError, WialonEvents, WialonEvent
# Silence potential warnings from static analysis tools:
assert Wialon
assert WialonError

__author__ = "o-murphy"
__copyright__ = (
    "Copyright 2013-2016, Gurtam; ",
    "Copyright 2022 Dmytro Yaroshenko; "
)

__credits__ = [
    "Alex Chernetsky",
    "Aleksey Shmigelski",
    "Mike Turchunovich",
    "Dmytro Yaroshenko",
]
__version__ = "1.2.5"

__all__ = ["Wialon"]
