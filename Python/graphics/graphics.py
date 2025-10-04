import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

# Настройки графиков
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Подключение к базе
conn = psycopg2.connect(
    dbname="e-commerce",
    user="postgres",
    password="5583liSH_J77",
    host="localhost",
    port="5432"
)

# 1. Динамика выручки и заказов по месяцам
query_trends = """
SELECT
    date_trunc('month', created_at) AS month,
    SUM(total_price) AS revenue,
    COUNT(*) AS orders_count
FROM orders
WHERE order_status = 'доставлен'
GROUP BY 1
ORDER BY 1;
"""

df_trends = pd.read_sql(query_trends, conn)

# Форматируем месяц для подписи
df_trends['month_label'] = df_trends['month'].dt.strftime('%b %Y')

# 2. Топ-10 категорий по количеству проданных товаров
query_top_categories = """
SELECT
    p.category,
    SUM(oi.quantity) AS total_quantity
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'доставлен'
GROUP BY p.category
ORDER BY total_quantity DESC
LIMIT 10;
"""

df_top_categories = pd.read_sql(query_top_categories, conn)
conn.close()

# Функция для форматирования оси Y
def y_formatter(x, pos):
    if x >= 1_000_000:
        return f'{x/1_000_000:.1f} млн'
    elif x >= 1_000:
        return f'{x/1_000:.0f} тыс'
    else:
        return f'{x:.0f}'

# График 1: Выручка по месяцам
plt.figure(figsize=(14, 6))
plt.plot(df_trends['month_label'], df_trends['revenue'], marker='o', color='teal')
plt.title("Динамика выручки по месяцам", fontsize=16)
plt.xlabel("Месяц", fontsize=12)
plt.ylabel("Выручка", fontsize=12)
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(y_formatter))
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# График 2: Количество заказов по месяцам
plt.figure(figsize=(14, 6))
plt.plot(df_trends['month_label'], df_trends['orders_count'], marker='o', color='orange')
plt.title("Динамика количества заказов по месяцам", fontsize=16)
plt.xlabel("Месяц", fontsize=12)
plt.ylabel("Количество заказов", fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# График 3: Топ категорий по количеству проданных товаров
plt.figure(figsize=(10, 6))
sns.barplot(
    x='total_quantity',
    y='category',
    data=df_top_categories,
    palette='coolwarm'
)
plt.title("Топ категорий по количеству проданных товаров", fontsize=16)
plt.xlabel("Количество проданных товаров", fontsize=12)
plt.ylabel("Категория", fontsize=12)
plt.tight_layout()
plt.show()
