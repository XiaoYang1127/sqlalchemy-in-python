from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from model import Base

"""
    lazy=select
        访问到属性的时候，就会全部加载该属性的数据
    lazy=joined
        在对关联的两个表进行join操作，从而获取到所有相关的对象
    lazy=dynamic
        在访问属性的时候，并没有在内存中加载数据，而是返回一个query对象, 需要执行相应方法才可以获取对象，比如.all()
"""


class COTMCompany(Base):

    __tablename__ = "one_to_many_company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    location = Column(String(255))

    # 设置关联属性，使用的时候类名和属性名
    # relationship 函数在 ORM 中用于构建表之间的关联关系。
    # 与 ForeignKey 不同的是，它定义的关系不属于表定义，而是动态计算的。
    rs_phone = relationship("COTMPhone", backref="rs_company")

    def __repr__(self):
        return f"<{self.id}.{self.name}> in {self.__tablename__}"

    def save(self):
        to_save = {
            "id": self.id,
            "name": self.name,
            "location": self.location,
        }
        return to_save

    def load(self, data):
        if not data:
            return
        self.id = data["id"]
        self.name = data["name"]
        self.location = data["location"]


class COTMPhone(Base):

    __tablename__ = 'one_to_many_phone'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    price = Column(Integer)

    # 设置外键的时候，使用的是表名和表列
    company_id = Column(Integer, ForeignKey("one_to_many_company.id"))

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
