-- =============================================
-- NOLA ANALYTICS - SCRIPT COMPLETO DO BANCO
-- =============================================

-- 1. CRIAR DATABASE E USUÁRIO
CREATE DATABASE nola_analytics;
\c nola_analytics;

CREATE USER nola_user WITH PASSWORD 'nola123';
GRANT ALL PRIVILEGES ON DATABASE nola_analytics TO nola_user;

-- 2. TABELAS PRINCIPAIS
CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sub_brands (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER REFERENCES brands(id),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER REFERENCES brands(id),
    sub_brand_id INTEGER REFERENCES sub_brands(id),
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(2),
    district VARCHAR(100),
    address_street VARCHAR(200),
    address_number INTEGER,
    zipcode VARCHAR(10),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    is_active BOOLEAN DEFAULT true,
    is_own BOOLEAN DEFAULT false,
    is_holding BOOLEAN DEFAULT false,
    creation_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE channels (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER REFERENCES brands(id),
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    type CHAR(1) CHECK (type IN ('P', 'D')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER REFERENCES brands(id),
    sub_brand_id INTEGER REFERENCES sub_brands(id),
    name VARCHAR(200) NOT NULL,
    type CHAR(1) DEFAULT 'P',
    pos_uuid VARCHAR(100),
    deleted_at TIMESTAMP
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER REFERENCES brands(id),
    sub_brand_id INTEGER REFERENCES sub_brands(id),
    category_id INTEGER REFERENCES categories(id),
    name VARCHAR(500) NOT NULL,
    pos_uuid VARCHAR(100),
    deleted_at TIMESTAMP
);

CREATE TABLE option_groups (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER REFERENCES brands(id),
    sub_brand_id INTEGER REFERENCES sub_brands(id),
    category_id INTEGER REFERENCES categories(id),
    name VARCHAR(500) NOT NULL,
    pos_uuid VARCHAR(100),
    deleted_at TIMESTAMP
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER REFERENCES brands(id),
    sub_brand_id INTEGER REFERENCES sub_brands(id),
    category_id INTEGER REFERENCES categories(id),
    name VARCHAR(500) NOT NULL,
    pos_uuid VARCHAR(100),
    deleted_at TIMESTAMP
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    phone_number VARCHAR(50),
    cpf VARCHAR(100),
    birth_date DATE,
    gender VARCHAR(10),
    store_id INTEGER REFERENCES stores(id),
    sub_brand_id INTEGER REFERENCES sub_brands(id),
    registration_origin VARCHAR(20),
    agree_terms BOOLEAN DEFAULT false,
    receive_promotions_email BOOLEAN DEFAULT false,
    receive_promotions_sms BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    store_id INTEGER NOT NULL REFERENCES stores(id),
    sub_brand_id INTEGER REFERENCES sub_brands(id),
    customer_id INTEGER REFERENCES customers(id),
    channel_id INTEGER NOT NULL REFERENCES channels(id),
    cod_sale1 VARCHAR(100),
    cod_sale2 VARCHAR(100),
    created_at TIMESTAMP NOT NULL,
    customer_name VARCHAR(100),
    sale_status_desc VARCHAR(100) NOT NULL,
    total_amount_items DECIMAL(10,2) NOT NULL,
    total_discount DECIMAL(10,2) DEFAULT 0,
    total_increase DECIMAL(10,2) DEFAULT 0,
    delivery_fee DECIMAL(10,2) DEFAULT 0,
    service_tax_fee DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    value_paid DECIMAL(10,2) DEFAULT 0,
    production_seconds INTEGER,
    delivery_seconds INTEGER,
    people_quantity INTEGER,
    discount_reason VARCHAR(300),
    increase_reason VARCHAR(300),
    origin VARCHAR(100) DEFAULT 'POS'
);

CREATE TABLE product_sales (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity FLOAT NOT NULL,
    base_price FLOAT NOT NULL,
    total_price FLOAT NOT NULL,
    observations VARCHAR(300)
);

CREATE TABLE item_product_sales (
    id SERIAL PRIMARY KEY,
    product_sale_id INTEGER NOT NULL REFERENCES product_sales(id) ON DELETE CASCADE,
    item_id INTEGER NOT NULL REFERENCES items(id),
    option_group_id INTEGER REFERENCES option_groups(id),
    quantity FLOAT NOT NULL,
    additional_price FLOAT NOT NULL,
    price FLOAT NOT NULL,
    amount FLOAT DEFAULT 1,
    observations VARCHAR(300)
);

CREATE TABLE item_item_product_sales (
    id SERIAL PRIMARY KEY,
    item_product_sale_id INTEGER NOT NULL REFERENCES item_product_sales(id) ON DELETE CASCADE,
    item_id INTEGER NOT NULL REFERENCES items(id),
    option_group_id INTEGER REFERENCES option_groups(id),
    quantity FLOAT NOT NULL,
    additional_price FLOAT NOT NULL,
    price FLOAT NOT NULL,
    amount FLOAT DEFAULT 1
);

CREATE TABLE delivery_sales (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
    courier_id VARCHAR(100),
    courier_name VARCHAR(100),
    courier_phone VARCHAR(100),
    courier_type VARCHAR(100),
    delivered_by VARCHAR(100),
    delivery_type VARCHAR(100),
    status VARCHAR(100),
    delivery_fee FLOAT,
    courier_fee FLOAT,
    timing VARCHAR(100),
    mode VARCHAR(100)
);

CREATE TABLE delivery_addresses (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
    delivery_sale_id INTEGER REFERENCES delivery_sales(id) ON DELETE CASCADE,
    street VARCHAR(200),
    number VARCHAR(20),
    complement VARCHAR(200),
    formatted_address VARCHAR(500),
    neighborhood VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    reference VARCHAR(300),
    latitude FLOAT,
    longitude FLOAT
);

CREATE TABLE payment_types (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER REFERENCES brands(id),
    description VARCHAR(100) NOT NULL
);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
    payment_type_id INTEGER REFERENCES payment_types(id),
    value DECIMAL(10,2) NOT NULL,
    is_online BOOLEAN DEFAULT false,
    description VARCHAR(100),
    currency VARCHAR(10) DEFAULT 'BRL'
);

CREATE TABLE coupons (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER REFERENCES brands(id),
    code VARCHAR(50) NOT NULL,
    discount_type VARCHAR(1),
    discount_value DECIMAL(10,2),
    is_active BOOLEAN DEFAULT true,
    valid_from TIMESTAMP,
    valid_until TIMESTAMP
);

CREATE TABLE coupon_sales (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER REFERENCES sales(id) ON DELETE CASCADE,
    coupon_id INTEGER REFERENCES coupons(id),
    value FLOAT,
    target VARCHAR(100),
    sponsorship VARCHAR(100)
);

-- 3. DADOS DE EXEMPLO
INSERT INTO brands (name) VALUES 
('Nola Burgers'),
('Nola Pizza'),
('Nola Café');

INSERT INTO sub_brands (brand_id, name) VALUES 
(1, 'Nola Burgers Premium'),
(1, 'Nola Burgers Express'),
(2, 'Nola Pizza Artesanal');

INSERT INTO stores (brand_id, sub_brand_id, name, city, state, is_active) VALUES 
(1, 1, 'Nola Paulista', 'São Paulo', 'SP', true),
(1, 1, 'Nola Ipanema', 'Rio de Janeiro', 'RJ', true),
(1, 2, 'Nola Savassi', 'Belo Horizonte', 'MG', true),
(1, 2, 'Nola Batel', 'Curitiba', 'PR', true),
(2, 3, 'Nola Pizza Centro', 'São Paulo', 'SP', true);

INSERT INTO channels (brand_id, name, description, type) VALUES 
(1, 'Balcão', 'Vendas no balcão', 'P'),
(1, 'iFood', 'Delivery iFood', 'D'),
(1, 'Rappi', 'Delivery Rappi', 'D'),
(1, 'WhatsApp', 'Pedidos WhatsApp', 'D'),
(1, 'App Próprio', 'Nosso aplicativo', 'D'),
(2, 'Balcão', 'Vendas no balcão', 'P'),
(2, 'iFood', 'Delivery iFood', 'D');

INSERT INTO categories (brand_id, name, type) VALUES 
(1, 'Lanches', 'P'),
(1, 'Bebidas', 'P'),
(1, 'Sobremesas', 'P'),
(1, 'Acompanhamentos', 'P'),
(1, 'Combos', 'P'),
(1, 'Adicionais', 'I'),
(1, 'Remover', 'I'),
(2, 'Pizzas', 'P'),
(2, 'Bebidas', 'P'),
(2, 'Massas', 'P');

INSERT INTO products (brand_id, category_id, name) VALUES 
(1, 1, 'Hambúrguer Clássico'),
(1, 1, 'Hambúrguer Especial'),
(1, 1, 'Cheeseburguer'),
(1, 1, 'X-Bacon'),
(1, 1, 'X-Tudo'),
(1, 2, 'Refrigerante 500ml'),
(1, 2, 'Suco Natural 300ml'),
(1, 2, 'Água 500ml'),
(1, 3, 'Brownie'),
(1, 3, 'Sorvete'),
(1, 4, 'Batata Frita Média'),
(1, 4, 'Batata Frita Grande'),
(1, 4, 'Onion Rings'),
(1, 5, 'Combo Casal'),
(1, 5, 'Combo Família'),
(2, 8, 'Pizza Margherita'),
(2, 8, 'Pizza Calabresa'),
(2, 8, 'Pizza Quatro Queijos'),
(2, 9, 'Refrigerante 2L'),
(2, 10, 'Espaguete à Bolonhesa');

INSERT INTO items (brand_id, category_id, name) VALUES 
(1, 6, 'Bacon Extra'),
(1, 6, 'Queijo Extra'),
(1, 6, 'Cheddar'),
(1, 6, 'Catupiry'),
(1, 6, 'Ovo'),
(1, 6, 'Alface'),
(1, 6, 'Tomate'),
(1, 6, 'Cebola'),
(1, 6, 'Picles'),
(1, 6, 'Maionese'),
(1, 7, 'Sem Cebola'),
(1, 7, 'Sem Picles'),
(1, 7, 'Sem Maionese'),
(1, 7, 'Pão sem Gergelim'),
(2, 6, 'Borda Recheada'),
(2, 6, 'Extra Queijo'),
(2, 6, 'Bacon'),
(2, 6, 'Azeitonas');

INSERT INTO option_groups (brand_id, name) VALUES 
(1, 'Adicionais'),
(1, 'Remover Ingredientes'),
(1, 'Modo de Preparo'),
(2, 'Adicionais Pizza'),
(2, 'Borda');

INSERT INTO payment_types (brand_id, description) VALUES 
(1, 'Dinheiro'),
(1, 'Cartão Débito'),
(1, 'Cartão Crédito'),
(1, 'PIX'),
(1, 'Vale Refeição'),
(2, 'Dinheiro'),
(2, 'Cartão Débito'),
(2, 'Cartão Crédito'),
(2, 'PIX');

INSERT INTO customers (customer_name, email, phone_number, store_id) VALUES 
('João Silva', 'joao.silva@email.com', '(11) 99999-1111', 1),
('Maria Santos', 'maria.santos@email.com', '(11) 99999-2222', 1),
('Pedro Oliveira', 'pedro.oliveira@email.com', '(21) 99999-3333', 2),
('Ana Costa', 'ana.costa@email.com', '(31) 99999-4444', 3),
('Carlos Souza', 'carlos.souza@email.com', '(41) 99999-5555', 4);

INSERT INTO coupons (brand_id, code, discount_type, discount_value, is_active) VALUES 
(1, 'NOLA10', 'p', 10.00, true),
(1, 'PRIMEIRA10', 'f', 10.00, true),
(1, 'BURGER20', 'p', 20.00, true),
(2, 'PIZZA15', 'p', 15.00, true);

-- 4. ÍNDICES PARA PERFORMANCE
CREATE INDEX idx_sales_created_at ON sales(created_at);
CREATE INDEX idx_sales_channel_id ON sales(channel_id);
CREATE INDEX idx_sales_store_id ON sales(store_id);
CREATE INDEX idx_sales_status ON sales(sale_status_desc);
CREATE INDEX idx_sales_date_status ON sales(created_at, sale_status_desc);
CREATE INDEX idx_sales_complete_performance ON sales(created_at, channel_id, store_id) WHERE sale_status_desc = 'COMPLETED';

CREATE INDEX idx_product_sales_sale_id ON product_sales(sale_id);
CREATE INDEX idx_product_sales_product_id ON product_sales(product_id);
CREATE INDEX idx_item_product_sales_product ON item_product_sales(product_sale_id, item_id);

CREATE INDEX idx_stores_brand_id ON stores(brand_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_customers_store_id ON customers(store_id);

-- 5. VIEWS MATERIALIZADAS
CREATE MATERIALIZED VIEW mv_daily_metrics AS
SELECT 
    DATE(s.created_at) as data,
    s.store_id,
    s.channel_id,
    COUNT(*) as total_vendas,
    SUM(s.total_amount) as faturamento_total,
    AVG(s.total_amount) as ticket_medio,
    SUM(s.total_discount) as total_descontos,
    SUM(s.delivery_fee) as total_entregas,
    COUNT(s.delivery_seconds) as vendas_com_entrega,
    AVG(s.production_seconds) as tempo_medio_preparo,
    AVG(s.delivery_seconds) as tempo_medio_entrega
FROM sales s
WHERE s.sale_status_desc = 'COMPLETED'
GROUP BY DATE(s.created_at), s.store_id, s.channel_id;

CREATE MATERIALIZED VIEW mv_top_products AS
SELECT 
    p.id as product_id,
    p.name as produto,
    c.name as categoria,
    COUNT(ps.id) as vezes_vendido,
    SUM(ps.quantity) as quantidade_vendida,
    SUM(ps.total_price) as receita_total,
    AVG(ps.total_price / ps.quantity) as preco_medio_unitario
FROM products p
JOIN product_sales ps ON ps.product_id = p.id
JOIN sales s ON s.id = ps.sale_id
JOIN categories c ON c.id = p.category_id
WHERE s.sale_status_desc = 'COMPLETED'
GROUP BY p.id, p.name, c.name;

CREATE UNIQUE INDEX idx_mv_daily_metrics ON mv_daily_metrics(data, store_id, channel_id);
CREATE UNIQUE INDEX idx_mv_top_products ON mv_top_products(product_id);

-- 6. PERMISSÕES FINAIS
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nola_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO nola_user;

-- 7. DADOS DE EXEMPLO DE VENDAS (20 vendas de exemplo)
INSERT INTO sales (store_id, channel_id, customer_id, created_at, customer_name, sale_status_desc, total_amount_items, total_amount, value_paid, production_seconds, delivery_seconds) VALUES 
(1, 2, 1, '2024-01-15 12:30:00', 'João Silva', 'COMPLETED', 45.00, 50.00, 50.00, 900, 1800),
(1, 1, 2, '2024-01-15 13:15:00', 'Maria Santos', 'COMPLETED', 38.00, 38.00, 38.00, 720, NULL),
(2, 3, 3, '2024-01-15 19:45:00', 'Pedro Oliveira', 'COMPLETED', 67.00, 72.00, 72.00, 1100, 2100),
(1, 2, NULL, '2024-01-16 20:30:00', 'Cliente Não Identificado', 'COMPLETED', 52.00, 57.00, 57.00, 950, 1950),
(3, 1, 4, '2024-01-16 12:00:00', 'Ana Costa', 'COMPLETED', 41.00, 41.00, 41.00, 800, NULL);

INSERT INTO product_sales (sale_id, product_id, quantity, base_price, total_price) VALUES 
(1, 1, 1, 25.00, 25.00),
(1, 11, 1, 12.00, 12.00),
(1, 6, 1, 8.00, 8.00),
(2, 2, 1, 30.00, 30.00),
(2, 8, 1, 5.00, 5.00),
(2, 9, 1, 8.00, 8.00),
(3, 4, 1, 35.00, 35.00),
(3, 12, 1, 18.00, 18.00),
(3, 6, 2, 8.00, 16.00),
(4, 5, 1, 40.00, 40.00),
(4, 11, 1, 12.00, 12.00),
(5, 3, 1, 28.00, 28.00),
(5, 11, 1, 12.00, 12.00),
(5, 7, 1, 10.00, 10.00);

INSERT INTO item_product_sales (product_sale_id, item_id, option_group_id, quantity, additional_price, price) VALUES 
(1, 1, 1, 1, 5.00, 5.00),
(1, 3, 1, 1, 4.00, 4.00),
(4, 1, 1, 1, 5.00, 5.00),
(7, 2, 1, 1, 4.00, 4.00),
(10, 1, 1, 1, 5.00, 5.00);

INSERT INTO payments (sale_id, payment_type_id, value, is_online) VALUES 
(1, 4, 50.00, true),
(2, 1, 38.00, false),
(3, 3, 72.00, true),
(4, 4, 57.00, true),
(5, 2, 41.00, false);

INSERT INTO delivery_sales (sale_id, courier_name, delivery_type, status, delivery_fee) VALUES 
(1, 'iFood', 'EXPRESS', 'ENTREGUE', 5.00),
(3, 'Rappi', 'NORMAL', 'ENTREGUE', 5.00),
(4, 'iFood', 'EXPRESS', 'ENTREGUE', 5.00);

INSERT INTO delivery_addresses (sale_id, street, number, neighborhood, city, state, postal_code) VALUES 
(1, 'Av. Paulista', '1000', 'Bela Vista', 'São Paulo', 'SP', '01310-100'),
(3, 'Rua Visconde de Pirajá', '500', 'Ipanema', 'Rio de Janeiro', 'RJ', '22410-002'),
(4, 'Rua Augusta', '2000', 'Consolação', 'São Paulo', 'SP', '01304-000');

-- ATUALIZAR VIEWS MATERIALIZADAS
REFRESH MATERIALIZED VIEW mv_daily_metrics;
REFRESH MATERIALIZED VIEW mv_top_products;

-- MENSAGEM FINAL
SELECT '🎉 BANCO NOLA ANALYTICS CRIADO COM SUCESSO!' as status;
SELECT '📊 ' || COUNT(*) || ' marcas inseridas' FROM brands;
SELECT '🏪 ' || COUNT(*) || ' lojas criadas' FROM stores;
SELECT '🛒 ' || COUNT(*) || ' produtos cadastrados' FROM products;
SELECT '📈 ' || COUNT(*) || ' vendas de exemplo' FROM sales;