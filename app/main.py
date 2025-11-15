from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.controllers import estabelecimento_controller

# Cria a aplicação FastAPI
app = FastAPI(
    title="SearchPublicData API",
    description="API para consulta de dados públicos (CNES)",
    version="1.0.0",
    docs_url=None,  # Desabilita o Swagger padrão
    redoc_url=None  # Desabilita o ReDoc padrão
)

# Inclui os controllers (routers)
app.include_router(estabelecimento_controller.router)

# Rota principal
@app.get("/", tags=["Root"])
async def root():
    return {
        "mensagem": "Bem-vindo à SearchPublicData API",
        "documentacao": "/docs"
    }

# Rota de healthcheck
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

# Configura o Scalar para documentação
@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )