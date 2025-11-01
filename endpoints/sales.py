from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from schemas import APIResponse, TopProductResponse

router = APIRouter()

@router.get("/top-products", response_model=APIResponse)
def get_top_products(db: Session = Depends(get_db)):
    query = text("""
        SELECT produto, vezes_vendido, receita_total
        FROM mv_top_products 
        ORDER BY vezes_vendido DESC 
        LIMIT 10
    """)
    results = db.execute(query).fetchall()
    
    products = [
        {"produto": r[0], "vezes_vendido": r[1], "receita_total": float(r[2])}
        for r in results
    ]
    
    return APIResponse(success=True, data={"products": products})

@router.get("/channels", response_model=APIResponse)
def get_channel_performance(db: Session = Depends(get_db)):
    query = text("""
        SELECT c.name as canal, 
               COUNT(*) as total_vendas,
               SUM(s.total_amount) as faturamento
        FROM sales s
        JOIN channels c ON c.id = s.channel_id
        WHERE s.sale_status_desc = 'COMPLETED'
        AND s.created_at >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY c.name
        ORDER BY faturamento DESC
    """)
    results = db.execute(query).fetchall()
    
    channels = [
        {"canal": r[0], "total_vendas": r[1], "faturamento": float(r[2])}
        for r in results
    ]
    
    return APIResponse(success=True, data={"channels": channels})