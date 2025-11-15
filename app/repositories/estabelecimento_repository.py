from pprint import pp
import aiosqlite
from typing import List, Optional
from app.models.estabelecimento_model import Estabelecimento, EstabelecimentoFiltroDTO
import re

class EstabelecimentoRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    async def obter_todas(self, limite: int = 200, pagina: int = 0) -> List[Estabelecimento]:
        """
        Busca todas as empresas com paginação.
        Note o mapeamento: campos do banco (maiúsculos) -> atributos Python
        """
        async with aiosqlite.connect(self.db_path) as db:
            query = """
                SELECT 
                    CODIGO_UNIDADE, CODIGO_CNES, NUMERO_CPF, NUMERO_CNPJ,
                    NOME_RAZAO_SOCIAL, NOME_FANTASIA, NOME_LOGRADOURO,
                    NUMERO_ENDERECO, NOME_BAIRRO, CODIGO_CEP, 
                    NUMERO_TELEFONE, NOME_EMAIL, DATA_ATUALIZACAO
                FROM Estabelecimento
                LIMIT ? OFFSET ?
            """
            async with db.execute(query, (limite, pagina)) as cursor:
                rows = await cursor.fetchall()
                return [Estabelecimento.from_db_row(row) for row in rows]
    
    async def buscar_com_filtros(self, cpf_cnpj: str=None, limite: int = 200, pagina: int = 0) -> List[Estabelecimento]:
        """
        Busca empresas com filtros dinâmicos.
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.set_trace_callback(print)
            conditions = ["NUMERO_CNPJ", "NUMERO_CNPJ_MANTENEDORA", "NUMERO_CPF"]
            if cpf_cnpj is None:
                where_clause = "1=1"
            else:
                where_clause = " OR ".join(condition + f" LIKE '%{cpf_cnpj}%'" for condition in conditions)
            
            # To implement
            # {", ".join(key.upper() for key in Estabelecimento.__dict__.keys() if not (key.startswith("__") or key.endswith("__")) and not callable(getattr(Estabelecimento, key)))}
            query = f"""
                SELECT 
                    CODIGO_UNIDADE, CODIGO_CNES, NUMERO_CPF, NUMERO_CNPJ,
                    NOME_RAZAO_SOCIAL, NOME_FANTASIA, NOME_LOGRADOURO,
                    NUMERO_ENDERECO, NOME_BAIRRO, CODIGO_CEP, 
                    NUMERO_TELEFONE, NOME_EMAIL, DATA_ATUALIZACAO
                FROM Estabelecimento
                WHERE {where_clause}
                LIMIT ? OFFSET ?
            """
            
            params = [limite, pagina]
            
            print(params)
            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                # pp(rows)
                await db.set_trace_callback(None)
                return [Estabelecimento.from_db_row(row) for row in rows]