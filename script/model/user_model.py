from sqlalchemy import Column, Integer, String

from model import Base, CTimestampMixin


class CUserModel(CTimestampMixin, Base):
    __tablename__ = "test_user"

    class_id = Column(Integer, nullable=False, comment="班级id")
    name = Column(String(50), nullable=False, comment="用户名称")
    age = Column(Integer, default=0, comment="年龄")
    addr = Column(String(255), nullable=True, comment="地址")
    tele = Column(String(50), unique=True, nullable=True, comment="手机号")

    def __repr__(self):
        return f"<{self.id}.{self.name}> in {self.__tablename__}"

    def save(self):
        to_save = {
            "id": self.id,
            "name": self.name,
            "addr": self.addr,
            "tele": self.tele
        }
        return to_save

    def load(self, data):
        if not data:
            return
        self.id = data["id"]
        self.name = data["name"]
        self.addr = data["addr"]
        self.tele = data["tele"]

    def serialize_simple(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def serialize_detail(self):
        return {
            "id": self.id,
            "name": self.name,
            "addr": self.addr,
            "tele": self.tele,
        }
