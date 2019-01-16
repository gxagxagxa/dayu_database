#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import threading

_DATABASE_INSTANCE = {}


def _find_current_db():
    return _DATABASE_INSTANCE.get(threading.current_thread().name, None)


def _find_current_session():
    db = _find_current_db()
    if db:
        return db.session
    return None

