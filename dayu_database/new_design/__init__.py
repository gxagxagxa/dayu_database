#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from globals import _find_current_db, _find_current_session

current_db = lambda: _find_current_db()
session = lambda: _find_current_session()
