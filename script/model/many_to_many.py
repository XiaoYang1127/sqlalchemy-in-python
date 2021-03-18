from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from model import Base


association_table = Table(
    'association',
    Base.metadata,
    Column('cid', Integer, ForeignKey('many_to_many_company.id')),
    Column('sid', Integer, ForeignKey('many_to_many_phone.id'))
)


class CMTMCompany(Base):

    __tablename__ = "many_to_many_company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    location = Column(String(255))

    rs_phone = relationship("CMTMPhone", secondary=association_table,
                            backref="rs_company", lazy="dynamic")

    # 给反向引用backref加lazy属性
    # rs_phone1 = relationship("CMTMPhone", secondaryjoin=registrations,
    #                          backref=backref("rs_company", lazy="dynamic"), lazy="dynamic")

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


class CMTMPhone(Base):

    __tablename__ = 'many_to_many_phone'

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
