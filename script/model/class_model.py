
from sqlalchemy import Column, Integer, String

from model import Base, CTimestampMixin


class CClassModel(Base, CTimestampMixin):
    __tablename__ = "test_class"

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
