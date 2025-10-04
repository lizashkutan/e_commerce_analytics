import pandas as pd
import psycopg2
import plotly.express as px

conn = psycopg2.connect(
    dbname="e-commerce",
    user="postgres",
    password="5583liSH_J77",
    host="localhost",
    port="5432"
)

# Суммарная выручка по городам
query = """
SELECT c.city, 
       SUM(o.total_price) AS revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status IN ('оплачен', 'доставлен')
GROUP BY c.city
ORDER BY revenue DESC
"""
city_sales = pd.read_sql(query, conn)
conn.close()

city_coords = {
    "Москва": [55.7558, 37.6173],
    "Санкт-Петербург": [59.9311, 30.3609],
    "Новосибирск": [55.0084, 82.9357],
    "Краснодар": [45.0355, 38.9753],
    "Екатеринбург": [56.8389, 60.6057],
    "Красноярск": [56.0153, 92.8932],
    "Владивосток": [43.1155, 131.8855],
    "Нижний Новгород": [56.2965, 43.9361],
    "Ростов-на-Дону": [47.2357, 39.7015],
    "Самара": [53.1959, 50.1003],
    "Воронеж": [51.6713, 39.1843],
    "Челябинск": [55.1644, 61.4368],
    "Сочи": [43.5855, 39.7203],
    "Казань": [55.7961, 49.1064]
}

city_sales['lat'] = city_sales['city'].apply(lambda x: city_coords[x][0])
city_sales['lon'] = city_sales['city'].apply(lambda x: city_coords[x][1])

palette = px.colors.sequential.Blues

# Строим карту
fig = px.scatter_mapbox(
    city_sales,
    lat='lat', lon='lon',
    size='revenue',
    color='revenue',
    hover_name='city',
    hover_data={'revenue': ':.2f', 'lat': False, 'lon': False},
    color_continuous_scale=palette,
    size_max=50,
    zoom=3,
    mapbox_style="carto-positron"
)

fig.update_layout(
    title="Выручка по городам",
    title_font=dict(family="DejaVu Sans, Arial, Verdana", size=22, color="#222222"),
    coloraxis_colorbar=dict(title="Выручка (₽)", title_font=dict(family="DejaVu Sans", size=14)),
    font=dict(family="DejaVu Sans, Arial, Verdana", size=12, color="#333333")
)

fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Выручка: %{customdata[0]:,.2f} ₽")

fig.show()
