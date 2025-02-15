import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = "postgresql://postgres:admin@localhost:5432/netology_db"

engine = sq.create_engine(DSN)
create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()

publisher_input = input("Введите имя или идентификатор автора: ")

# Определяем, является ли ввод числом (идентификатором)
if publisher_input.isdigit():
    publisher_id = int(publisher_input)
    publisher = session.query(Publisher).filter(Publisher.id == publisher_id).first()
else:
    publisher = session.query(Publisher).filter(Publisher.name == publisher_input).first()

if publisher:
    # Выполняем запрос для получения данных о продажах
    sales_data = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
        join(Stock, Book.id == Stock.id_book).\
        join(Shop, Stock.id_shop == Shop.id).\
        join(Sale, Stock.id == Sale.id_stock).\
        filter(Book.id_publisher == publisher.id).all()

    # Выводим результаты
    for title, shop_name, price, date_sale in sales_data:
        print(f"{title} | {shop_name} | {price} | {date_sale.strftime('%d-%m-%Y')}")
else:
    print("Издатель не найден.")

session.close()