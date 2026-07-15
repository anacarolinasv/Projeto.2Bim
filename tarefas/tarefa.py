import json
import os
from enum import Enum


class StatusTarefa(Enum):
    """Situacao de uma tarefa no fluxo de trabalho."""

    A_FAZER = "A_FAZER"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDA = "CONCLUIDA"


class Prioridade(Enum):
    """Prioridade de uma tarefa."""

    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"

class Tarefa:
    def __init__(self, id=0, titulo="", descricao="", status=StatusTarefa.A_FAZER,
                 prioridade=Prioridade.MEDIA, data_criacao="", prazo="",
                 sprint_id=0, responsavel_id=0, categoria_id=0):
        self._id = id
        self._titulo = titulo
        self._descricao = descricao
        self._status = status
        self._prioridade = prioridade
        self._data_criacao = data_criacao
        self._prazo = prazo
        self._sprint_id = sprint_id
        self._responsavel_id = responsavel_id
        self._categoria_id = categoria_id

    def get_id(self):
        return self._id

    def set_id(self, valor):
        self._id = valor

    def get_titulo(self):
        return self._titulo

    def set_titulo(self, valor):
        if not valor or not valor.strip():
            raise ValueError("O titulo da tarefa nao pode ser vazio.")
        self._titulo = valor

    def get_descricao(self):
        return self._descricao

    def set_descricao(self, valor):
        self._descricao = valor

    def get_status(self):
        return self._status

    def set_status(self, valor):
        self._status = valor

    def get_prioridade(self):
        return self._prioridade

    def set_prioridade(self, valor):
        self._prioridade = valor

    def get_data_criacao(self):
        return self._data_criacao

    def set_data_criacao(self, valor):
        self._data_criacao = valor

    def get_prazo(self):
        return self._prazo

    def set_prazo(self, valor):
        self._prazo = valor

    def get_sprint_id(self):
        return self._sprint_id

    def set_sprint_id(self, valor):
        self._sprint_id = valor

    def get_responsavel_id(self):
        return self._responsavel_id

    def set_responsavel_id(self, valor):
        self._responsavel_id = valor

    def get_categoria_id(self):
        return self._categoria_id

    def set_categoria_id(self, valor):
        self._categoria_id = valor

    def concluir(self):
        self._status = StatusTarefa.CONCLUIDA

    def to_json(self):
        return {
            "id": self._id,
            "titulo": self._titulo,
            "descricao": self._descricao,
            "status": self._status.value,
            "prioridade": self._prioridade.value,
            "data_criacao": self._data_criacao,
            "prazo": self._prazo,
            "sprint_id": self._sprint_id,
            "responsavel_id": self._responsavel_id,
            "categoria_id": self._categoria_id,
        }

    @staticmethod
    def from_json(dic):
        return Tarefa(
            dic["id"], dic["titulo"], dic["descricao"],
            StatusTarefa(dic["status"]), Prioridade(dic["prioridade"]),
            dic["data_criacao"], dic["prazo"], dic["sprint_id"],
            dic["responsavel_id"], dic["categoria_id"],
        )

    def __str__(self):
        return f"Tarefa(id={self._id}, titulo='{self._titulo}', status={self._status.value})"


# ======================================================================
# PERSISTENCIA (DAO)
# ======================================================================
class TarefaDAO:
    ARQUIVO = "data/tarefas.json"
    objetos = []

    @staticmethod
    def Abrir():
        if not os.path.exists(TarefaDAO.ARQUIVO):
            TarefaDAO.objetos = []
            return
        with open(TarefaDAO.ARQUIVO, "r", encoding="utf-8") as arquivo:
            TarefaDAO.objetos = [Tarefa.from_json(d) for d in json.load(arquivo)]

    @staticmethod
    def Salvar():
        pasta = os.path.dirname(TarefaDAO.ARQUIVO)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)
        with open(TarefaDAO.ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump([o.to_json() for o in TarefaDAO.objetos], arquivo,
                      ensure_ascii=False, indent=4)

    @staticmethod
    def Inserir(obj):
        TarefaDAO.Abrir()
        novo_id = 1 if not TarefaDAO.objetos else max(o.get_id() for o in TarefaDAO.objetos) + 1
        obj.set_id(novo_id)
        TarefaDAO.objetos.append(obj)
        TarefaDAO.Salvar()
        return obj

    @staticmethod
    def Listar():
        TarefaDAO.Abrir()
        return TarefaDAO.objetos

    @staticmethod
    def Listar_Id(id):
        TarefaDAO.Abrir()
        for o in TarefaDAO.objetos:
            if o.get_id() == id:
                return o
        return None

    @staticmethod
    def Atualizar(obj):
        TarefaDAO.Abrir()
        for i, o in enumerate(TarefaDAO.objetos):
            if o.get_id() == obj.get_id():
                TarefaDAO.objetos[i] = obj
                TarefaDAO.Salvar()
                return True
        return False

    @staticmethod
    def Excluir(id):
        TarefaDAO.Abrir()
        antes = len(TarefaDAO.objetos)
        TarefaDAO.objetos = [o for o in TarefaDAO.objetos if o.get_id() != id]
        if len(TarefaDAO.objetos) < antes:
            TarefaDAO.Salvar()
            return True
        return False

    # ---- Pesquisa e associacao ----
    @staticmethod
    def Pesquisar_Por_Titulo(termo):
        termo = termo.lower()
        return [o for o in TarefaDAO.Listar() if termo in o.get_titulo().lower()]

    @staticmethod
    def Listar_Por_Sprint(sprint_id):
        return [o for o in TarefaDAO.Listar() if o.get_sprint_id() == sprint_id]

    @staticmethod
    def Listar_Por_Responsavel(responsavel_id):
        return [o for o in TarefaDAO.Listar() if o.get_responsavel_id() == responsavel_id]

    @staticmethod
    def Listar_Por_Categoria(categoria_id):
        return [o for o in TarefaDAO.Listar() if o.get_categoria_id() == categoria_id]
