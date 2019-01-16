#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import threading

from utils import lazy_property


class DayuDatabase(object):
    def __new__(cls):
        from globals import _DATABASE_INSTANCE
        current_thread = '{thread}'.format(thread=threading.current_thread().name)
        if current_thread in _DATABASE_INSTANCE:
            return _DATABASE_INSTANCE.get(current_thread, None)

        instance = super(DayuDatabase, cls).__new__(cls)
        _DATABASE_INSTANCE[current_thread] = instance
        return instance

    def __init__(self):
        super(DayuDatabase, self).__init__()
        from config import DayuDatabaseConfig
        self.config = DayuDatabaseConfig()
        self.engine = None
        self.__session_maker = None

    def connect(self, ip=None, port=None, user=None, password=None, database=None):
        print 'connecting'
        # from sqlalchemy import create_engine
        # self.engine = create_engine()

    def disconnect(self):
        pass

    @lazy_property
    def session(self):
        return
