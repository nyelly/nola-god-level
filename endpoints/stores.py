from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from schemas import APIResponse

router = APIRouter()

@router.get("/list", response_model=APIResponse)
def get_stores(db: Session = Depends(get_db)):
    query = text("""
        SELECT id, name, city, state, is_active
        FROM stores
        ORDER BY name
    """)
    results = db.execute(query).fetchall()
    
    stores = [
        {"id": r[0], "nome": r[1], "cidade": r[2], "estado": r[3], "ativo": r[4]}
        for r in results
    ]
    
    return APIResponse(success=True, data={"stores": stores})

@router.get("/performance", response_model=APIResponse)
def get_stores_performance(db: Session = Depends(get_db)):
    query = text("""
        SELECT s.name as loja,
               COUNT(*) as total_vendas,
               SUM(sa.total_amount) as faturamento,
               AVG(sa.total_amount) as ticket_medio
        FROM sales sa
        JOIN stores s ON s.id = sa.store_id
        WHERE sa.sale_status_desc = 'COMPLETED'
        AND sa.created_at >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY s.name
        ORDER BY faturamento DESC
    """)
    results = db.execute(query).fetchall()
    
    performance = [
        {
            "loja": r[0], 
            "total_vendas": r[1], 
            "faturamento": float(r[2] or 0),
            "ticket_medio": float(r[3] or 0)
        }
        for r in results
    ]
    
    return APIResponse(success=True, data={"performance": performance})