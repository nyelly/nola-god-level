from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import kpis, sales, analytics, products, stores

app = FastAPI(title="Nola Analytics API", version="1.0.0")

# Configurar CORS para o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar TODOS os endpoints
app.include_router(kpis.router, prefix="/api/kpis", tags=["KPIs"])
app.include_router(sales.router, prefix="/api/sales", tags=["Sales"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(stores.router, prefix="/api/stores", tags=["Stores"])

@app.get("/")
def read_root():
    return {"message": "Nola Analytics API - Sistema de Analytics para Restaurantes"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "nola-analytics-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)