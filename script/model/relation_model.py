from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from model import Base


class CUser(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(50))
    age = Column('age', Integer)

    # 添加角色id外键(关联到Role表的id属性)
    role_id = Column('role_id', Integer, ForeignKey('roles.id'))
    # 添加同表外键
    second_role_id = Column('second_role_id', Integer, ForeignKey('roles.id'))

    # 添加关系属性，关联到role_id外键上
    role = relationship('CRole', foreign_keys='CUser.role_id', backref='User_role_id')
    # 添加关系属性，关联到second_role_id外键上
    second_role = relationship('CRole', foreign_keys='CUser.second_role_id',
                               backref='User_second_role_id')

    def __repr__(self):
        return f"<{self.id}.{self.name}> in {self.__tablename__}"

    def save(self):
        to_save = {
            "id": self.id,
            "name": self.name,
            "age": self.age,
        }
        return to_save

    def load(self, data):
        if not data:
            return
        self.id = data["id"]
        self.name = data["name"]
        self.age = data["age"]


class CRole(Base):
    __tablename__ = 'roles'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(50))

    # 添加关系属性，关联到User.role_id属性上
    users = relationship("CUser", foreign_keys='CUser.role_id', backref="Role_users")
    # 添加关系属性，关联到User.second_role_id属性上
    second_users = relationship(
        "CUser", foreign_keys='CUser.second_role_id', backref="Role_second_users")

    def __repr__(self):
        return f"<{self.id}.{self.name}> in {self.__tablename__}"

    def save(self):
        to_save = {
            "id": self.id,
            "name": self.name,
        }
        return to_save

    def load(self, data):
        if not data:
            return
        self.id = data["id"]
        self.name = data["name"]
