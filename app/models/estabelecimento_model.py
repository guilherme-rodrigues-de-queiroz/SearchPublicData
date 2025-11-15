from typing import Optional

class Estabelecimento:
    """Model que representa um estabelecimento no banco de dados"""
    def __init__(self, codigo_unidade: str, codigo_cnes: str, numero_cpf: str, numero_cnpj: str, nome_razao_social: str, nome_fantasia: str, nome_logradouro: str, numero_endereco: str, nome_bairro: str, codigo_cep: str, numero_telefone: str, nome_email: str, data_atualizacao: str):
        self.codigo_unidade = codigo_unidade
        self.codigo_cnes = codigo_cnes
        self.numero_cpf = numero_cpf
        self.numero_cnpj = numero_cnpj
        self.nome_razao_social = nome_razao_social
        self.nome_fantasia = nome_fantasia
        self.nome_logradouro = nome_logradouro
        self.numero_endereco = numero_endereco
        self.nome_bairro = nome_bairro
        self.codigo_cep = codigo_cep
        self.numero_telefone = numero_telefone
        self.nome_email = nome_email
        self.data_atualizacao = data_atualizacao
    
    @staticmethod
    def from_db_row(row: tuple) -> 'Estabelecimento':
        """Cria uma instância de Estabelecimento a partir de uma linha do banco"""
        return Estabelecimento(
            codigo_unidade=row[0],
            codigo_cnes=row[1],
            numero_cpf=row[2],
            numero_cnpj=row[3],
            nome_razao_social=row[4],
            nome_fantasia=row[5],
            nome_logradouro=row[6],
            numero_endereco=row[7],
            nome_bairro=row[8],
            codigo_cep=row[9],
            numero_telefone=row[10],
            nome_email=row[11],
            data_atualizacao=row[12]
        )

    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            "codigo_unidade": self.codigo_unidade,
            "codigo_cnes": self.codigo_cnes,
            "numero_cpf": self.numero_cpf,
            "numero_cnpj": self.numero_cnpj,
            "nome_razao_social": self.nome_razao_social,
            "nome_fantasia": self.nome_fantasia,
            "nome_logradouro": self.nome_logradouro,
            "numero_endereco": self.numero_endereco,
            "nome_bairro": self.nome_bairro,
            "codigo_cep": self.codigo_cep,
            "numero_telefone": self.numero_telefone,
            "nome_email": self.nome_email,
            "data_atualizacao": self.data_atualizacao,
        }


class EstabelecimentoFiltroDTO:
    """DTO para filtro de busca"""
    def __init__(
        self,
        numero_cpf: Optional[str] = None,
        numero_cnpj: Optional[str] = None,
    ):
        self.numero_cpf = numero_cpf
        self.numero_cnpj = numero_cnpj