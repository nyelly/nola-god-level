from pydantic import BaseModel
from datetime import datetime
from typing import List

class KPIResponse(BaseModel):
    total_vendas: int
    faturamento_total: float
    ticket_medio: float
    total_descontos: float

class SalesTrend(BaseModel):
    data: datetime
    valor: float

class TopProductResponse(BaseModel):
    produto: str
    vezes_vendido: int
    receita_total: float

class ChannelPerformance(BaseModel):
    canal: str
    total_vendas: int
    faturamento: float

class APIResponse(BaseModel):
    success: bool
    data: dict
    message: str = ""