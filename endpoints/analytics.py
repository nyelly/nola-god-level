from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from schemas import APIResponse

router = APIRouter()

@router.get("/trends", response_model=APIResponse)
def get_sales_trends(db: Session = Depends(get_db)):
    query = text("""
        SELECT DATE(created_at) as data,
               SUM(total_amount) as valor
        FROM sales
        WHERE sale_status_desc = 'COMPLETED'
        AND created_at >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY DATE(created_at)
        ORDER BY data
    """)
    results = db.execute(query).fetchall()
    
    trends = [{"data": r[0], "valor": float(r[1])} for r in results]
    
    return APIResponse(success=True, data={"trends": trends})