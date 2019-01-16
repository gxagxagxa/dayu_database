#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'



class lazy_property(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value
