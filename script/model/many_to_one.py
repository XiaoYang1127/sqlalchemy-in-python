from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from model import Base


class CMTOCompany(Base):

    __tablename__ = "many_to_one_company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    location = Column(String(255))

    # 设置外键的时候，使用的是表名和表列
    phone_id = Column(Integer, ForeignKey("many_to_one_phone.id"))

    # 设置关联属性，使用的时候类名和属性名
    # relationship 函数在 ORM 中用于构建表之间的关联关系。
    # 与 ForeignKey 不同的是，它定义的关系不属于表定义，而是动态计算的。
    rs_phone = relationship("CMTOPhone", backref="rs_company")

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


class CMTOPhone(Base):

    __tablename__ = 'many_to_one_phone'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    price = Column(Integer)

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
