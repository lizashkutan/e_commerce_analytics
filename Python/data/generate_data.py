import random
import datetime
from faker import Faker
from unidecode import unidecode
import psycopg2
from psycopg2.extras import execute_values

fake = Faker("ru_RU")

# Подключение к БД
conn = psycopg2.connect(
    dbname="e-commerce",
    user="postgres",
    password="5583liSH_J77",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Генерация клиентов
NUM_CUSTOMERS = 10000
customers = []

cities = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Краснодар", "Екатеринбург",
    "Красноярск", "Владивосток", "Нижний Новгород", "Ростов-на-Дону",
    "Самара", "Воронеж", "Челябинск", "Сочи", "Казань"
]

male_names = ["Алексей", "Иван", "Сергей", "Дмитрий", "Андрей", "Александр", "Николай", "Владимир", "Михаил", "Егор",
              "Лев", "Антон", "Елисей", "Ярослав", "Петр"]
female_names = ["Анна", "Елена", "Мария", "Ольга", "Наталья", "Светлана", "Юлия", "Татьяна", "Ирина", "Виктория",
                "Елизавета", "София", "Полина", "Дарья", "Злата", "Алена", "Марина", "Анастасия", "Александра"]

male_surnames = ["Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов", "Васильев", "Новиков", "Морозов", "Фёдоров",
                 "Михайлов"]
female_surnames = [s + "а" for s in male_surnames]

for i in range(NUM_CUSTOMERS):
    gender = random.choice(["male", "female"])
    if gender == "male":
        first_name = random.choice(male_names)
        last_name = random.choice(male_surnames)
    else:
        first_name = random.choice(female_names)
        last_name = random.choice(female_surnames)

    email = f"{unidecode(first_name.lower())}.{unidecode(last_name.lower())}{i}@example.com"
    phone = fake.phone_number()
    city = random.choice(cities)
    customers.append((email, phone, first_name, last_name, city))

execute_values(
    cur,
    "INSERT INTO customers (email, phone, first_name, last_name, city) VALUES %s",
    customers
)
conn.commit()
print("Клиенты вставлены")

# Генерация товаров
NUM_PRODUCTS = 2000
brands_by_category = {
    "Электроника": ["Apple", "Samsung", "Xiaomi", "Huawei", "Realme", "Vivo", "Lenovo", "ASUS"],
    "Одежда": ["ZARA", "H&M", "UNIQLO", "Tommy Hilfiger", "Calvin Klein", "Bershka", "Mango", "befree", "lime",
               "monochrome", "gate31", "sela", "feelz", "look.online", "12storeez"],
    "Обувь": ["Nike", "adidas", "Reebok", "Puma", "ECCO", "Skechers", "New Balance", "Timberland",
              "Dr. Martens", "Salomon", "Converse", "Vans", "Birkenstock"],
    "Бытовая техника": ["Bosch", "Samsung", "LG", "Philips", "Xiaomi", "Redmond", "Tefal",
                        "Bork", "Polaris", "Vitek", "Gorenje"],
    "Красота и здоровье": ["L'Oreal", "Garnier", "Nivea", "Maybelline", "Vichy",
                           "La Roche-Posay", "Bioderma", "Lancôme", "Estée Lauder", "Clarins"],
    "Дом и интерьер": ["IKEA", "Leroy Merlin", "Hoff", "Askona", "Zara Home"]
}

product_templates = {
    "Одежда": ["Футболка", "Платье", "Джинсы", "Куртка", "Худи", "Рубашка"],
    "Обувь": ["Кроссовки", "Ботинки", "Туфли", "Кеды", "Сандалии"],
    "Электроника": ["Смартфон", "Ноутбук", "Планшет", "Телевизор", "Наушники"],
    "Бытовая техника": ["Холодильник", "Стиральная машина", "Чайник", "Микроволновка", "Пылесос"],
    "Красота и здоровье": ["Крем для лица", "Шампунь", "Румяна", "Помада", "Тональный крем"],
    "Дом и интерьер": ["Диван", "Стол", "Кровать", "Ковер", "Шкаф"]
}

products = []
for _ in range(NUM_PRODUCTS):
    category = random.choice(list(brands_by_category.keys()))
    brand = random.choice(brands_by_category[category])
    product_type = random.choice(product_templates[category])

    name = product_type
    price = round(max(200, random.normalvariate(5000, 3000)), 2)
    products.append((name, category, brand, price))

execute_values(
    cur,
    "INSERT INTO products (name, category, brand, price) VALUES %s",
    products
)
conn.commit()
print("Товары вставлены")

# Предзагрузка товаров в память (id → price)
cur.execute("SELECT product_id, price FROM products")
product_map = dict(cur.fetchall())

# Генерация заказов
NUM_ORDERS = 100000
BATCH_SIZE = 1000

payment_methods = ["карта", "СБП", "QR-код"]
statuses = ["оплачен", "доставлен", "отменен", "возвращен"]
delivery_methods = ["курьер", "самовывоз"]

order_number_counter = 1

sql_orders = """
    INSERT INTO orders 
    (order_number, customer_id, order_status, payment_method, delivery_method, total_price, created_at, delivered_at)
    VALUES %s RETURNING order_id
"""
sql_items = "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES %s"

for batch_start in range(0, NUM_ORDERS, BATCH_SIZE):
    orders_batch = []
    items_batch = []
    batch_size = min(BATCH_SIZE, NUM_ORDERS - batch_start)

    for _ in range(batch_size):
        customer_id = random.randint(1, NUM_CUSTOMERS)
        created_at = fake.date_time_between(
            start_date="-365d", end_date="now",
            tzinfo=datetime.timezone(datetime.timedelta(hours=3))
        )
        status = random.choices(statuses, weights=[70, 20, 7, 3])[0]
        payment = random.choices(payment_methods, weights=[60, 30, 10])[0]
        delivery = random.choice(delivery_methods)

        delivered_at = None
        if status == "доставлен":
            delivered_at = created_at + datetime.timedelta(days=random.randint(1, 14))

        total_price = 0
        order_items = []
        for _ in range(random.randint(1, 5)):
            product_id = random.randint(1, NUM_PRODUCTS)
            price = product_map[product_id]
            qty = random.randint(1, 3)
            total_price += price * qty
            order_items.append((product_id, qty, price))

        order_number = f"ORD-{order_number_counter:08d}"
        order_number_counter += 1
        orders_batch.append(
            (order_number, customer_id, status, payment, delivery, round(total_price, 2), created_at, delivered_at)
        )
        items_batch.append(order_items)

    # вставляем заказы и получаем order_id
    execute_values(cur, sql_orders, orders_batch)
    order_ids = [row[0] for row in cur.fetchall()]

    # вставляем позиции
    order_items_all = []
    for oid, items in zip(order_ids, items_batch):
        for product_id, qty, price in items:
            order_items_all.append((oid, product_id, qty, price))

    execute_values(cur, sql_items, order_items_all)
    conn.commit()

    print(f"Вставлено заказов: {batch_start + batch_size}/{NUM_ORDERS}")

cur.close()
conn.close()
print("Генерация завершена")