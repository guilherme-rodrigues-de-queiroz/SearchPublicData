from fastapi import APIRouter, Query, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from app.repositories.estabelecimento_repository import EstabelecimentoRepository
from app.models.estabelecimento_model import EstabelecimentoFiltroDTO

class EstabelecimentoResponse(BaseModel):
    codigo_unidade: Optional[str] = None
    codigo_cnes: Optional[str] = None
    numero_cpf: Optional[str] = None       
    numero_cnpj: Optional[str] = None      
    nome_razao_social: Optional[str] = None
    nome_fantasia: Optional[str] = None
    nome_logradouro: Optional[str] = None  
    numero_endereco: Optional[str] = None  
    nome_bairro: Optional[str] = None
    codigo_cep: Optional[str] = None       
    numero_telefone: Optional[str] = None  
    nome_email: Optional[str] = None       
    data_atualizacao: Optional[str] = None 

class ListaEstabelecimentosResponse(BaseModel):
    pagina: int
    limite: int
    estabelecimentos: List[EstabelecimentoResponse]

# Cria o router
router = APIRouter(prefix="/estabelecimentos", tags=["Estabelecimentos"])

DB_PATH = "database/cnes_database_completo.db"
estabelecimento_repo = EstabelecimentoRepository(DB_PATH)


@router.get("/listar", response_model=ListaEstabelecimentosResponse, summary="Lista todos os estabelecimentos")
async def listar_estabelecimentos(
    pagina: int = Query(0, ge=0, description="Número da página"),
    limite: int = Query(50, ge=1, le=200, description="Itens por página")
):
    """Retorna a lista de todos os estabelecimentos cadastrados"""
    offset = pagina * limite
    estabelecimentos = await estabelecimento_repo.obter_todas(limite=limite, pagina=offset)

    return {
        "pagina": pagina,
        "limite": limite,
        "estabelecimentos": [est.to_dict() for est in estabelecimentos]
    }


@router.get("/buscar", response_model=ListaEstabelecimentosResponse, 
            summary="Busca estabelecimentos por CPF ou CNPJ")
async def buscar_estabelecimentos(
    cpf_cnpj: Optional[str] = Query(None, description="CPF ou CNPJ para buscar"),
    pagina: int = Query(0, ge=0, description="Número da página"),
    limite: int = Query(50, ge=1, le=200, description="Itens por página")
):

    if not cpf_cnpj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Informe pelo menos um filtro: CPF ou CNPJ"
        )
    
    # filtro = EstabelecimentoFiltroDTO(numero_cpf=cpf, numero_cnpj=cnpj)
    estabelecimentos = await estabelecimento_repo.buscar_com_filtros(cpf_cnpj, limite, pagina*limite)

    if not estabelecimentos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum estabelecimento encontrado com os filtros informados"
        )
    
    return {
        "pagina": pagina,
        "limite": limite,
        "estabelecimentos": [est.to_dict() for est in estabelecimentos]
    }
