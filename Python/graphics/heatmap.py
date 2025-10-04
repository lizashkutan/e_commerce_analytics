import pandas as pd
import psycopg2
import seaborn as sns
import matplotlib.pyplot as plt

conn = psycopg2.connect(
    dbname="e-commerce",
    user="postgres",
    password="5583liSH_J77",
    host="localhost",
    port="5432"
)

query = """
SELECT created_at
FROM orders
WHERE order_status IN ('оплачен', 'доставлен')
"""
orders = pd.read_sql(query, conn)
conn.close()

# Добавляем день недели и час
orders['weekday'] = orders['created_at'].dt.day_name(locale='ru_RU')
orders['hour'] = orders['created_at'].dt.hour

# Считаем количество заказов по дню недели и часу
heatmap_data = orders.groupby(['weekday', 'hour']).size().unstack(fill_value=0)

days_order = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
heatmap_data = heatmap_data.reindex(days_order)

# Строим heatmap
plt.figure(figsize=(15,6))
sns.heatmap(heatmap_data, cmap="Purples", linewidths=.5, annot=True, fmt='d')
plt.title('Активность заказов по дням недели и часам')
plt.xlabel('Час')
plt.ylabel('День недели')
plt.show()
