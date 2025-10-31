from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from schemas import APIResponse

router = APIRouter()

@router.get("/categories", response_model=APIResponse)
def get_categories(db: Session = Depends(get_db)):
    query = text("""
        SELECT name, COUNT(*) as total_produtos
        FROM categories 
        WHERE type = 'P'
        GROUP BY name
        ORDER BY total_produtos DESC
    """)
    results = db.execute(query).fetchall()
    
    categories = [
        {"categoria": r[0], "total_produtos": r[1]}
        for r in results
    ]
    
    return APIResponse(success=True, data={"categories": categories})

@router.get("/top-items", response_model=APIResponse)
def get_top_items(db: Session = Depends(get_db)):
    query = text("""
        SELECT i.name as item, 
               COUNT(*) as vezes_adicionado,
               SUM(ips.additional_price) as receita_gerada
        FROM item_product_sales ips
        JOIN items i ON i.id = ips.item_id
        GROUP BY i.name
        ORDER BY vezes_adicionado DESC
        LIMIT 15
    """)
    results = db.execute(query).fetchall()
    
    items = [
        {"item": r[0], "vezes_adicionado": r[1], "receita_gerada": float(r[2] or 0)}
        for r in results
    ]
    
    return APIResponse(success=True, data={"items": items})