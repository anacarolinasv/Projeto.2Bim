import json
import os
from enum import Enum


class StatusProjeto(Enum):
    """Situacao de um projeto."""

    ATIVO = "ATIVO"
    CONCLUIDO = "CONCLUIDO"
    ARQUIVADO = "ARQUIVADO"

class Projeto:
    """Projeto. Relacionamento 1 -> N: possui varias Tarefas.
    Associacao N -> 1: pertence a uma Equipe (equipe_id)."""

    def __init__(self, id=0, nome="", descricao="", data_inicio="",
                 data_fim="", status=StatusProjeto.ATIVO, equipe_id=0):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._data_inicio = data_inicio
        self._data_fim = data_fim
        self._status = status
        self._equipe_id = equipe_id

    def get_id(self):
        return self._id

    def set_id(self, valor):
        self._id = valor

    def get_nome(self):
        return self._nome

    def set_nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("O nome do projeto nao pode ser vazio.")
        self._nome = valor

    def get_descricao(self):
        return self._descricao

    def set_descricao(self, valor):
        self._descricao = valor

    def get_data_inicio(self):
        return self._data_inicio

    def set_data_inicio(self, valor):
        self._data_inicio = valor

    def get_data_fim(self):
        return self._data_fim

    def set_data_fim(self, valor):
        self._data_fim = valor

    def get_status(self):
        return self._status

    def set_status(self, valor):
        self._status = valor

    def get_equipe_id(self):
        return self._equipe_id

    def set_equipe_id(self, valor):
        self._equipe_id = valor

    def to_json(self):
        return {
            "id": self._id,
            "nome": self._nome,
            "descricao": self._descricao,
            "data_inicio": self._data_inicio,
            "data_fim": self._data_fim,
            "status": self._status.value,
            "equipe_id": self._equipe_id,
        }

    @staticmethod
    def from_json(dic):
        return Projeto(
            dic["id"], dic["nome"], dic["descricao"], dic["data_inicio"],
            dic["data_fim"], StatusProjeto(dic["status"]), dic["equipe_id"],
        )

    def __str__(self):
        return f"Projeto(id={self._id}, nome='{self._nome}', status={self._status.value})"


# ======================================================================
# PERSISTENCIA (DAO)
# ======================================================================
class ProjetoDAO:
    ARQUIVO = "data/projetos.json"
    objetos = []

    @staticmethod
    def Abrir():
        if not os.path.exists(ProjetoDAO.ARQUIVO):
            ProjetoDAO.objetos = []
            return
        with open(ProjetoDAO.ARQUIVO, "r", encoding="utf-8") as arquivo:
            ProjetoDAO.objetos = [Projeto.from_json(d) for d in json.load(arquivo)]

    @staticmethod
    def Salvar():
        pasta = os.path.dirname(ProjetoDAO.ARQUIVO)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)
        with open(ProjetoDAO.ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump([o.to_json() for o in ProjetoDAO.objetos], arquivo,
                      ensure_ascii=False, indent=4)

    @staticmethod
    def Inserir(obj):
        ProjetoDAO.Abrir()
        novo_id = 1 if not ProjetoDAO.objetos else max(o.get_id() for o in ProjetoDAO.objetos) + 1
        obj.set_id(novo_id)
        ProjetoDAO.objetos.append(obj)
        ProjetoDAO.Salvar()
        return obj

    @staticmethod
    def Listar():
        ProjetoDAO.Abrir()
        return ProjetoDAO.objetos

    @staticmethod
    def Listar_Id(id):
        ProjetoDAO.Abrir()
        for o in ProjetoDAO.objetos:
            if o.get_id() == id:
                return o
        return None

    @staticmethod
    def Atualizar(obj):
        ProjetoDAO.Abrir()
        for i, o in enumerate(ProjetoDAO.objetos):
            if o.get_id() == obj.get_id():
                ProjetoDAO.objetos[i] = obj
                ProjetoDAO.Salvar()
                return True
        return False

    @staticmethod
    def Excluir(id):
        ProjetoDAO.Abrir()
        antes = len(ProjetoDAO.objetos)
        ProjetoDAO.objetos = [o for o in ProjetoDAO.objetos if o.get_id() != id]
        if len(ProjetoDAO.objetos) < antes:
            ProjetoDAO.Salvar()
            return True
        return False

    # ---- Pesquisa e associacao ----
    @staticmethod
    def Pesquisar_Por_Nome(termo):
        termo = termo.lower()
        return [o for o in ProjetoDAO.Listar() if termo in o.get_nome().lower()]

    @staticmethod
    def Listar_Por_Equipe(equipe_id):
        return [o for o in ProjetoDAO.Listar() if o.get_equipe_id() == equipe_id]
