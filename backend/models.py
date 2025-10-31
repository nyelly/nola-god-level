from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Date, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    name = Column(String(255), nullable=False)
    city = Column(String(100))
    state = Column(String(2))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    name = Column(String(100), nullable=False)
    type = Column(String(1))  # P=Presencial, D=Delivery
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String(500), nullable=False)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    name = Column(String(200), nullable=False)
    type = Column(String(1), default='P')  # P=Produto, I=Item

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100))
    email = Column(String(100))
    phone_number = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    customer_name = Column(String(100))
    sale_status_desc = Column(String(100), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    total_amount_items = Column(DECIMAL(10, 2), nullable=False)
    total_discount = Column(DECIMAL(10, 2), default=0)
    delivery_fee = Column(DECIMAL(10, 2), default=0)
    value_paid = Column(DECIMAL(10, 2), default=0)
    production_seconds = Column(Integer)
    delivery_seconds = Column(Integer)

class ProductSale(Base):
    __tablename__ = "product_sales"
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

# Modelos para as Views Materializadas
class DailyMetric(Base):
    __tablename__ = "mv_daily_metrics"
    data = Column(Date, primary_key=True)
    store_id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, primary_key=True)
    total_vendas = Column(Integer)
    faturamento_total = Column(DECIMAL(10, 2))
    ticket_medio = Column(DECIMAL(10, 2))
    valor_produtos = Column(DECIMAL(10, 2))
    total_descontos = Column(DECIMAL(10, 2))
    total_entregas = Column(DECIMAL(10, 2))

class TopProduct(Base):
    __tablename__ = "mv_top_products"
    product_id = Column(Integer, primary_key=True)
    produto = Column(String(500))
    categoria = Column(String(200))
    vezes_vendido = Column(Integer)
    quantidade_vendida = Column(Float)
    receita_total = Column(DECIMAL(10, 2))