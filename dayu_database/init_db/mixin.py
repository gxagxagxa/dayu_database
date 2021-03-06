#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import itertools

__author__ = 'andyguo'

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, func
from sqlalchemy.orm import deferred, relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import JSONB
from dayu_database.util import current_user_name


class TimestampMixin(object):
    '''
    让class 具备created_time 和 updated_time 这两个属性
    '''

    @declared_attr
    def created_time(cls):
        return deferred(Column(DateTime(timezone=False), server_default=func.now()))

    @declared_attr
    def updated_time(cls):
        return deferred(Column(DateTime(timezone=False), onupdate=func.now()))


class UserMixin(object):
    '''
    让class 具备 created_by 和 updated_by 这两个属性。分别用来记录由谁创建、由谁更新的
    '''

    @declared_attr
    def created_by_name(cls):
        return deferred(Column(String, default=current_user_name()))

    @declared_attr
    def created_by(cls):
        return relationship('USER', primaryjoin='foreign({}.created_by_name) == remote(USER.name)'.format(cls.__name__))

    @declared_attr
    def updated_by_name(cls):
        return deferred(Column(String))

    @declared_attr
    def updated_by(cls):
        return relationship('USER', primaryjoin='foreign({}.updated_by_name) == remote(USER.name)'.format(cls.__name__))


class ExtraDataMixin(object):
    '''
    让class 具备 extra_data 和 debug_data 这两个jsonb 格式的属性。
    通常推荐常用的信息，放入extra_data （例如，sub_level 的文件路径信息就存放在extra_data）
    调试信息、代码信息、错误信息这些只有开发人员需要的信息，推荐放入 debug_data 中。
    （如果信息量很大，并且不需要进场读取，推荐创建INFO，然后hook 到orm 上）
    '''

    @declared_attr
    def extra_data(cls):
        return deferred(Column(JSONB, default=lambda: {}))

    @declared_attr
    def debug_data(cls):
        return deferred(Column(JSONB, default=lambda: {}))


class TypeMixin(object):
    '''
    让class 具备 type_group 和type 的属性
    '''

    @declared_attr
    def type_group_name(cls):
        return deferred(Column(String))

    @declared_attr
    def type_name(cls):
        return deferred(Column(String))

    @declared_attr
    def type_group(cls):
        return relationship('TYPE_GROUP',
                            primaryjoin='foreign({}.type_group_name) == remote(TYPE_GROUP.name)'.format(cls.__name__),
                            backref=backref('{}s'.format(cls.__name__.lower()),
                                            lazy='dynamic'))

    @declared_attr
    def type(cls):
        return relationship('TYPE',
                            primaryjoin='foreign({}.type_name) == remote(TYPE.name)'.format(cls.__name__),
                            backref=backref('{}s'.format(cls.__name__.lower()),
                                            lazy='dynamic'))


class DiskPathMixin(object):
    '''
    让class 具备从orm 转换到DiskPath 的能力
    '''

    _cache_publish_disk_path = None
    _cache_work_disk_path = None
    _cache_cache_disk_path = None

    @declared_attr
    def path_data(cls):
        return deferred(Column(JSONB, default=lambda: {}))


class WorkflowMixin(object):
    # @declared_attr
    # def workflow_config_name(cls):
    #     return Column(String, index=True)

    @declared_attr
    def pipeline_config_name(cls):
        return Column(String)


class DepthMixin(object):
    '''
    用于实现数据库树状层级结构的重要mixin class！
    '''

    # 用来记录当前orm 所处的层级深度
    depth = Column(Integer, default=0, index=True)
    # 根据项目对应的 DB_CONFIG 来判断，当前深度的orm 应该对应制作中的什么含义（如PROJECT、ASSET、SHOT、RESOURCE、VERSION……）
    meaning = Column(String, index=True)

    @declared_attr
    def db_config_name(cls):
        return Column(String)

    @declared_attr
    def storage_config_name(cls):
        return Column(String)

    parent_id = Column(BigInteger, index=True)
    top_id = Column(BigInteger, index=True)


class ClueMixin(object):
    '''
    提供metadata 信息和其他环节信息匹配的mixin。
    这些线索对应了不同的环节。用户只需要录入信息，之后的匹配会动态的通过数据库查询得到。无需手动建立metadata 和shot 之间的关联。
    '''

    @declared_attr
    def cam_clue(cls):
        # cam_clue 用来记录onset 摄影机的reel name
        return deferred(Column(JSONB, default=[]))

    @declared_attr
    def scene_clue(cls):
        # scene_clue, shot_clue, take_clue 是记录现场拍摄、剪辑师习惯的场、镜、次号
        return deferred(Column(JSONB, default=[]))

    @declared_attr
    def shot_clue(cls):
        # scene_clue, shot_clue, take_clue 是记录现场拍摄、剪辑师习惯的场、镜、次号
        return deferred(Column(JSONB, default=[]))

    @declared_attr
    def take_clue(cls):
        # scene_clue, shot_clue, take_clue 是记录现场拍摄、剪辑师习惯的场、镜、次号
        return deferred(Column(JSONB, default=[]))

    @declared_attr
    def vfx_clue(cls):
        # vfx_clue 记录VFX 对应的shot、asset、sequence 之类的编号
        return deferred(Column(JSONB, default=[]))

    @declared_attr
    def di_clue(cls):
        # di_clue 记录DI 需要的信息（暂时没有）
        return deferred(Column(JSONB, default=[]))


class InfoMixin(object):
    '''
    让class 可以被INFO 挂靠
    '''
    pass


class NoteMixin(object):
    '''
    让class 可以被NOTE 挂靠
    '''
    pass


class SymbolMixin(object):
    '''
    让class 可以拥有symbol 的属性
    '''
    pass


class JobMixin(object):
    '''
    让class 可以提交job 到任务中心。通常情况下是VERSION、DAILIES 这样meaning 的FOLDER 可以继承这个mixin class。
    '''
    pass


class CloudMixin(object):
    @declared_attr
    def cloud_table(cls):
        # cloud_table 记录与云端对应的table 名称（通常是shotgun、ftrack 之类）
        return deferred(Column(String))

    @declared_attr
    def cloud_id(cls):
        # cloud_id 记录与云端对应的entity id（通常是shotgun、ftrack 之类）
        return deferred(Column(Integer))
