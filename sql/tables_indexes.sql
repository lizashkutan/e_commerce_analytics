-- Клиенты
CREATE TABLE customers (
  customer_id SERIAL PRIMARY KEY,
  email TEXT UNIQUE,
  phone TEXT,
  first_name TEXT,
  last_name TEXT,
  city TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Товары
CREATE TABLE products (
  product_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT,
  brand TEXT,
  price NUMERIC(12,2) NOT NULL
);

-- Заказы
CREATE TABLE orders (
  order_id BIGSERIAL PRIMARY KEY,
  order_number TEXT UNIQUE,
  customer_id INTEGER REFERENCES customers(customer_id),
  order_status TEXT,      
  payment_method TEXT,     
  delivery_method TEXT,    
  total_price NUMERIC(12,2),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  delivered_at TIMESTAMP WITH TIME ZONE
);

-- Позиции заказа
CREATE TABLE order_items (
  order_item_id BIGSERIAL PRIMARY KEY,
  order_id BIGINT REFERENCES orders(order_id) ON DELETE CASCADE,
  product_id INTEGER REFERENCES products(product_id),
  quantity INTEGER NOT NULL,
  unit_price NUMERIC(12,2) NOT NULL
);


CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_orders_payment_method ON orders(payment_method);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orderitems_product ON order_items(product_id);
