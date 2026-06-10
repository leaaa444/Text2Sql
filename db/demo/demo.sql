DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT,
    email TEXT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    order_date DATE NOT NULL,
    status TEXT
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL
);

INSERT INTO customers (name, city, email) VALUES
    ('Ana Anic', 'Beograd', 'ana@example.com'),
    ('Marko Markovic', 'Novi Sad', 'marko@example.com'),
    ('Jovana Jovanovic', 'Nis', 'jovana@example.com'),
    ('Petar Petrovic', 'Beograd', 'petar@example.com');

INSERT INTO products (name, category, price) VALUES
    ('Laptop', 'Elektronika', 1200.00),
    ('Mis', 'Elektronika', 25.00),
    ('Tastatura', 'Elektronika', 45.00),
    ('Knjiga SQL', 'Knjige', 30.00),
    ('Monitor', 'Elektronika', 300.00);

INSERT INTO orders (customer_id, order_date, status) VALUES
    (1, '2026-01-15', 'isporuceno'),
    (1, '2026-02-03', 'isporuceno'),
    (2, '2026-02-20', 'u obradi'),
    (3, '2026-03-01', 'isporuceno'),
    (4, '2026-03-10', 'otkazano');

INSERT INTO order_items (order_id, product_id, quantity) VALUES
    (1, 1, 1),
    (1, 2, 2),
    (2, 4, 3),
    (3, 5, 1),
    (3, 3, 1),
    (4, 2, 5),
    (5, 1, 1);
