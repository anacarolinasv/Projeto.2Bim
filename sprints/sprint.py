import json
import os

class Sprint:
    def __init__(self, id=0, nome="", objetivo="", data_inicio="",
                 data_fim="", projeto_id=0):
        self._id = id
        self._nome = nome
        self._objetivo = objetivo
        self._data_inicio = data_inicio
        self._data_fim = data_fim
        self._projeto_id = projeto_id

    def get_id(self):
        return self._id

    def set_id(self, valor):
        self._id = valor

    def get_nome(self):
        return self._nome

    def set_nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("O nome da sprint nao pode ser vazio.")
        self._nome = valor

    def get_objetivo(self):
        return self._objetivo

    def set_objetivo(self, valor):
        self._objetivo = valor

    def get_data_inicio(self):
        return self._data_inicio

    def set_data_inicio(self, valor):
        self._data_inicio = valor

    def get_data_fim(self):
        return self._data_fim

    def set_data_fim(self, valor):
        self._data_fim = valor

    def get_projeto_id(self):
        return self._projeto_id

    def set_projeto_id(self, valor):
        self._projeto_id = valor

    def to_json(self):
        return {
            "id": self._id,
            "nome": self._nome,
            "objetivo": self._objetivo,
            "data_inicio": self._data_inicio,
            "data_fim": self._data_fim,
            "projeto_id": self._projeto_id,
        }

    @staticmethod
    def from_json(dic):
        return Sprint(
            dic["id"], dic["nome"], dic["objetivo"], dic["data_inicio"],
            dic["data_fim"], dic["projeto_id"],
        )

    def __str__(self):
        return f"Sprint(id={self._id}, nome='{self._nome}', projeto_id={self._projeto_id})"


# ======================================================================
# PERSISTENCIA (DAO)
# ======================================================================
class SprintDAO:
    ARQUIVO = "data/sprints.json"
    objetos = []

    @staticmethod
    def Abrir():
        if not os.path.exists(SprintDAO.ARQUIVO):
            SprintDAO.objetos = []
            return
        with open(SprintDAO.ARQUIVO, "r", encoding="utf-8") as arquivo:
            SprintDAO.objetos = [Sprint.from_json(d) for d in json.load(arquivo)]

    @staticmethod
    def Salvar():
        pasta = os.path.dirname(SprintDAO.ARQUIVO)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)
        with open(SprintDAO.ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump([o.to_json() for o in SprintDAO.objetos], arquivo,
                      ensure_ascii=False, indent=4)

    @staticmethod
    def Inserir(obj):
        SprintDAO.Abrir()
        novo_id = 1 if not SprintDAO.objetos else max(o.get_id() for o in SprintDAO.objetos) + 1
        obj.set_id(novo_id)
        SprintDAO.objetos.append(obj)
        SprintDAO.Salvar()
        return obj

    @staticmethod
    def Listar():
        SprintDAO.Abrir()
        return SprintDAO.objetos

    @staticmethod
    def Listar_Id(id):
        SprintDAO.Abrir()
        for o in SprintDAO.objetos:
            if o.get_id() == id:
                return o
        return None

    @staticmethod
    def Atualizar(obj):
        SprintDAO.Abrir()
        for i, o in enumerate(SprintDAO.objetos):
            if o.get_id() == obj.get_id():
                SprintDAO.objetos[i] = obj
                SprintDAO.Salvar()
                return True
        return False

    @staticmethod
    def Excluir(id):
        SprintDAO.Abrir()
        antes = len(SprintDAO.objetos)
        SprintDAO.objetos = [o for o in SprintDAO.objetos if o.get_id() != id]
        if len(SprintDAO.objetos) < antes:
            SprintDAO.Salvar()
            return True
        return False

    # ---- Pesquisa e associacao ----
    @staticmethod
    def Pesquisar_Por_Nome(termo):
        termo = termo.lower()
        return [o for o in SprintDAO.Listar() if termo in o.get_nome().lower()]

    @staticmethod
    def Listar_Por_Projeto(projeto_id):
        return [o for o in SprintDAO.Listar() if o.get_projeto_id() == projeto_id]
