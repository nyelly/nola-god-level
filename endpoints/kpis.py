from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from schemas import KPIResponse, APIResponse
router = APIRouter()

@router.get("/daily", response_model=APIResponse)
def get_daily_kpis(db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            SUM(total_vendas) as total_vendas,
            SUM(faturamento_total) as faturamento_total,
            AVG(ticket_medio) as ticket_medio,
            SUM(total_descontos) as total_descontos
        FROM mv_daily_metrics 
        WHERE data = CURRENT_DATE
    """)
    result = db.execute(query).fetchone()
    
    return APIResponse(
        success=True,
        data={
            "total_vendas": result[0] or 0,
            "faturamento_total": float(result[1] or 0),
            "ticket_medio": float(result[2] or 0),
            "total_descontos": float(result[3] or 0)
        }
    )

@router.get("/summary", response_model=APIResponse)
def get_kpi_summary(db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            COUNT(*) as total_vendas,
            SUM(total_amount) as faturamento_total,
            AVG(total_amount) as ticket_medio
        FROM sales 
        WHERE sale_status_desc = 'COMPLETED'
        AND created_at >= CURRENT_DATE - INTERVAL '30 days'
    """)
    result = db.execute(query).fetchone()
    
    return APIResponse(
        success=True,
        data={
            "total_vendas": result[0] or 0,
            "faturamento_total": float(result[1] or 0),
            "ticket_medio": float(result[2] or 0)
        }
    )