from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)  # integer primary key will be autoincremented by default
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))

    def __repr__(self) -> str:
        return f"User(user_id {self.user_id!r}, name={self.fist_name!r}, surname={self.last_name!r})"
