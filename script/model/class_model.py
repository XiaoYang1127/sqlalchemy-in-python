
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import model.base


CBase = declarative_base()


class CClassModel(model.base.CBase, CBase):
    __tablename__ = "test_class"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment="班级id")
    name = Column(String(50), nullable=False, comment="班级名称")

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

    def serialize_simple(self):
        return {
            "id": self.id,
            "name": self.name
        }
