from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from model import Base


class COTOCompany(Base):

    __tablename__ = "one_to_one_company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    location = Column(String(255))

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


class COTOPhone(Base):

    __tablename__ = 'one_to_one_phone'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    price = Column(Integer)

    company_id = Column(Integer, ForeignKey('one_to_one_company.id'))
    # 设置关联属性，使用的时候类名和属性名
    # relationship 函数在 ORM 中用于构建表之间的关联关系。
    # 与 ForeignKey 不同的是，它定义的关系不属于表定义，而是动态计算的。
    rs_company = relationship("COTOCompany", uselist=False, backref="rs_phone")

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
