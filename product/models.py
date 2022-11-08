from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from database import Base


class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True)  # integer primary key will be autoincremented by default
    title = Column(String(255), unique=True, nullable=False)
    body = Column(String(255))
    price = Column(Integer)
    image_url = Column(String)
    category = Column(String)


    def __repr__(self) -> str:
        return f"Product(title= {self.title!r}, name={self.body!r}, surname={self.price!r})"


