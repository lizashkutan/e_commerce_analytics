import pandas as pd
from sqlalchemy import create_engine

# Подключаемся к базе
engine = create_engine("postgresql+psycopg2://postgres:5583liSH_J77@localhost:5432/e-commerce")

# Загружаем таблицы
orders_df = pd.read_sql("SELECT * FROM orders", engine)
order_items_df = pd.read_sql("SELECT * FROM order_items", engine)
customers_df = pd.read_sql("SELECT * FROM customers", engine)
products_df = pd.read_sql("SELECT * FROM products", engine)

def to_date(df, column_name):
    if column_name in df.columns:
        df[column_name] = pd.to_datetime(df[column_name], errors='coerce') \
                            .dt.tz_localize(None) \
                            .dt.date

to_date(orders_df, 'created_at')
to_date(orders_df, 'delivered_at')
to_date(customers_df, 'created_at')

# Записываем в Excel
with pd.ExcelWriter("ecommerce.xlsx", engine='xlsxwriter', datetime_format='dd.mm.yyyy') as writer:
    orders_df.to_excel(writer, sheet_name="Orders", index=False)
    order_items_df.to_excel(writer, sheet_name="OrderItems", index=False)
    customers_df.to_excel(writer, sheet_name="Customers", index=False)
    products_df.to_excel(writer, sheet_name="Products", index=False)

print("Данные успешно экспортированы в ecommerce.xlsx")

