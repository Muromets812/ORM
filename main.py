import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime as dt
import json

engine = sq.create_engine('postgresql://postgres:NetologY@localhost:5432/books')
Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(50), unique=True)

    def __str__(self):
        return f'User: {self.name}'

    books = relationship('Book', back_populates='publisher')


class Book(Base):
    __tablename__ = 'book'
    id = sq.Column(sq.BigInteger, primary_key=True)
    title = sq.Column(sq.String, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'))

    def __str__(self):
        return f'Note text: {self.title[:15]}'

    publishers = relationship('Publisher', back_populates='books')
    stocks = relationship('Stok', secondary='stock', back_populates='stocks')


class Stock(Base):
    __tablename__ = 'stock'
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'))
    count = sq.Column(sq.Integer, nullable=False)

    def __str__(self):
        return f'Note text: {self.count}'

    sales = relationship('Sale', back_populates='stocks')
    publishers = relationship('Publisher', back_populates='books')


class Shop(Base):
    __tablename__ = 'shop'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), nullable=False)

    def __str__(self):
        return f'Note text: {self.name}'

    stocks = relationship('Stok', secondary='stock', back_populates='stocks')


class Sale(Base):
    __tablename__ = 'sale'
    id = sq.Column(sq.Integer, primary_key=True)
    prise = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.DateTime, default=dt.datetime.now)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('stock.id'))
    count = sq.Column(sq.Integer, nullable=False)

    def __str__(self):
        return f'Note text: {self.prise}'

    stocks = relationship('Stock', back_populates='sales')


if __name__ == "__main__":

    Session = sessionmaker(bind=engine)
    session = Session()
    #session.close()


    def recreate_tables(engine):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)


    recreate_tables(engine)

    with open('tests_data.json') as f:
        data = json.load(f)


    for item in data:
        if item['model'] == 'publisher':
            print(item['fields']['name'])
            insert_item = Publisher(name=item['fields']['name'])
            session.add(insert_item)
            session.commit()


    #i = Publisher(id="1", name="O’Reilly")
    #session.add(i)
    #session.commit()