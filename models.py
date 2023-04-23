import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
import datetime as dt

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(50), unique=True)

    def __str__(self):
        return f'User: {self.name}'


class Book(Base):
    __tablename__ = 'book'
    id = sq.Column(sq.BigInteger, primary_key=True)
    title = sq.Column(sq.String, unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    def __str__(self):
        return f'Note text: {self.title[:15]}'

    publisher_book = relationship('Publisher', backref='book')


class Stock(Base):
    __tablename__ = 'stock'
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    def __str__(self):
        return f'Note text: {self.count}'

    shop_stock = relationship('Shop', backref='stock1')
    book_stock = relationship('Book', backref='stock2')


class Shop(Base):
    __tablename__ = 'shop'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), nullable=False)

    def __str__(self):
        return f'Note text: {self.name}'


class Sale(Base):
    __tablename__ = 'sale'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.FLOAT, nullable=False)
    date_sale = sq.Column(sq.DateTime, default=dt.datetime.now, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    def __str__(self):
        return f'Note text: {self.prise}, {self.date_sale}'

    stock_sale = relationship('Stock', backref='sale')


def recreate_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

