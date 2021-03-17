from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from model import Base


class CCompany(Base):

    __tablename__ = "company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    location = Column(String(20))

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


class CPhone(Base):

    __tablename__ = 'phone'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    price = Column(Integer)

    # 设置外键的时候，使用的是表名和表列
    company_id = Column(Integer, ForeignKey("company.id"))
    # 设置关联属性，使用的时候类名和属性名
    # relationship 函数在 ORM 中用于构建表之间的关联关系。
    # 与 ForeignKey 不同的是，它定义的关系不属于表定义，而是动态计算的。
    company = relationship("CCompany", backref="phone_of_company")
    # company2 = relationship("CCompany", foreign_keys='CCompany.id', backref="phone_of_company2")

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
