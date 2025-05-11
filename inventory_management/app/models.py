from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import validates

from app.database import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

    @validates('price')
    def validate_price(self, key, value):
        if value < 0:
            ValueError('Price cannot be negative')
        return value

    @validates('quantity')
    def validate_quantity(self, key, value):
        if value < 0:
            ValueError('Price cannot be negative')
        return value
