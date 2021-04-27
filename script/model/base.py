"""
note:
    1. Insert, Update, Delete by sql expression cant't be listened by ``events``
    2. attention the differences between in "update" and "update exists"
    3. delete exists, delete where, delete join(left, right, inner)
"""


from sqlalchemy import Column, Integer, DateTime, event, func, ForeignKey
from sqlalchemy.sql.expression import Insert, Update, Delete, Select
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.dialects.mysql import INTEGER

import db.redis_db


class CTimestampMixin(object):
    skip_created_at = 0
    skip_updated_at = 0

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(
        DateTime, default=func.now(),
        server_default=func.now(),
        onupdate=func.now())


class CBase(object):
    """
    1. Column构造函数相关设置
        name：名称
        type_：列类型
        autoincrement：自增
        default：默认值
        index：索引
        nullable：可空
        primary_key：是否主键
    """

    ex_time = 24 * 60 * 60
    no_save_redis = 0

    __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__ = {'always_refresh': True}

    id = Column("id", INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    @classmethod
    def create_table(cls, engine):
        cls.metadata.create_all(engine)

    @classmethod
    def drop_db(cls, engine):
        cls.metadata.drop_all(engine)

    def save(self):
        raise NotImplementedError("save undefined")

    def load(self, data):
        raise NotImplementedError("load undefined")

    def save_to_redis(self):
        to_save = self.save()
        redis_client = db.redis_db.GetRedisConn()
        redis_client.myset(
            "%s:%s" % (self.__table__, self.id),
            to_save,
            ex=self.ex_time,
            serialize=True)

    def load_from_redis(self, unique_id):
        redis_client = db.redis_db.GetRedisConn()
        from_load = redis_client.myget(
            "%s:%s" % (self.__table__, unique_id),
            {},
            serialize=True)
        self.load(from_load)

    def delete_from_redis(self):
        redis_client = db.redis_db.GetRedisConn()
        redis_client.delete("%s:%s" % (self.__table__, self.id))

    def tbl_cols(self):
        return self.__table__.columns

    def to_dict(self):
        return {col.name: getattr(self, col.name, None) for col in self.tbl_cols()}


Base = declarative_base(cls=CBase)


@event.listens_for(CTimestampMixin, 'before_update', propagate=True)
def before_update(mapper, connection, target):
    """
    only listen for operations performed in ``ORM`` mode
    """
    if target.skip_updated_at:
        return
    target.updated_at = func.now()


@event.listens_for(CTimestampMixin, 'before_insert', propagate=True)
def before_insert(mapper, connection, target):
    if target.skip_created_at:
        return
    target.created_at = func.now()
    target.updated_at = func.now()


@event.listens_for(CBase, 'after_update', propagate=True)
def after_update(mapper, connection, target):
    if target.no_save_redis:
        return
    target.save_to_redis()


@event.listens_for(CBase, 'after_insert', propagate=True)
def after_insert(mapper, connection, target):
    if target.no_save_redis:
        return
    target.save_to_redis()


@event.listens_for(CBase, 'after_delete', propagate=True)
def after_delete(mapper, connection, target):
    if target.no_save_redis:
        return
    target.delete_from_redis()


@compiles(Insert)
def insert_for_update(insert, compiler, **kw):
    s = compiler.visit_insert(insert, **kw)
    if 'insert_for_update' in insert.kwargs:
        return s + " ON DUPLICATE KEY UPDATE " + insert.kwargs['insert_for_update']
    return s
