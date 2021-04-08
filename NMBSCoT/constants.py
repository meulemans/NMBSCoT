#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""NMBS Cursor-on-Target Constants."""

import logging
import os
import json

if bool(os.environ.get("DEBUG")):
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = logging.Formatter(
        ('%(asctime)s nmbscot %(levelname)s %(name)s.%(funcName)s:%(lineno)d '
         ' - %(message)s'))
    logging.debug('nmbscot Debugging Enabled via DEBUG Environment Variable.')
else:
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = logging.Formatter(
        ('%(asctime)s nmbsxcot %(levelname)s - %(message)s'))

DEFAULT_INTERVAL: int = 25
DEFAULT_STALE: int = 25
