import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Stock, Shop, Sale
from models import recreate_tables
import json
import datetime as dt

if __name__ == "__main__":

    engine = sq.create_engine('postgresql://postgres:NetologY@localhost:5432/books')
    recreate_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    with open('tests_data.json', 'r') as f:
        data = json.load(f)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

    publisher_name = input('Введите название издательства:nullable=False ')
    my_query = session.query(Publisher, Book.title, Shop.name, Sale.price, Sale.date_sale).join(Book).join(Stock).join(Shop).join(Sale).filter(Publisher.name == publisher_name).all()

    for item in my_query:
        print(f"{item[1]} | {item[2]} | {item[3]} | {dt.datetime.date(item[4])}")



