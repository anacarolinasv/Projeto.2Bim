import json
import os

# ======================================================================
class Equipe:
    def __init__(self, id=0, nome="", descricao="", lider_id=0):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._lider_id = lider_id

    def get_id(self):
        return self._id

    def set_id(self, valor):
        self._id = valor

    def get_nome(self):
        return self._nome

    def set_nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("O nome da equipe nao pode ser vazio.")
        self._nome = valor

    def get_descricao(self):
        return self._descricao

    def set_descricao(self, valor):
        self._descricao = valor

    def get_lider_id(self):
        return self._lider_id

    def set_lider_id(self, valor):
        self._lider_id = valor

    def to_json(self):
        return {
            "id": self._id,
            "nome": self._nome,
            "descricao": self._descricao,
            "lider_id": self._lider_id,
        }

    @staticmethod
    def from_json(dic):
        return Equipe(dic["id"], dic["nome"], dic["descricao"], dic["lider_id"])

    def __str__(self):
        return f"Equipe(id={self._id}, nome='{self._nome}')"


# ======================================================================
# PERSISTENCIA (DAO)
# ======================================================================
class EquipeDAO:
    ARQUIVO = "data/equipes.json"
    objetos = []

    @staticmethod
    def Abrir():
        if not os.path.exists(EquipeDAO.ARQUIVO):
            EquipeDAO.objetos = []
            return
        with open(EquipeDAO.ARQUIVO, "r", encoding="utf-8") as arquivo:
            EquipeDAO.objetos = [Equipe.from_json(d) for d in json.load(arquivo)]

    @staticmethod
    def Salvar():
        pasta = os.path.dirname(EquipeDAO.ARQUIVO)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)
        with open(EquipeDAO.ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump([o.to_json() for o in EquipeDAO.objetos], arquivo,
                      ensure_ascii=False, indent=4)

    @staticmethod
    def Inserir(obj):
        EquipeDAO.Abrir()
        novo_id = 1 if not EquipeDAO.objetos else max(o.get_id() for o in EquipeDAO.objetos) + 1
        obj.set_id(novo_id)
        EquipeDAO.objetos.append(obj)
        EquipeDAO.Salvar()
        return obj

    @staticmethod
    def Listar():
        EquipeDAO.Abrir()
        return EquipeDAO.objetos

    @staticmethod
    def Listar_Id(id):
        EquipeDAO.Abrir()
        for o in EquipeDAO.objetos:
            if o.get_id() == id:
                return o
        return None

    @staticmethod
    def Atualizar(obj):
        EquipeDAO.Abrir()
        for i, o in enumerate(EquipeDAO.objetos):
            if o.get_id() == obj.get_id():
                EquipeDAO.objetos[i] = obj
                EquipeDAO.Salvar()
                return True
        return False

    @staticmethod
    def Excluir(id):
        EquipeDAO.Abrir()
        antes = len(EquipeDAO.objetos)
        EquipeDAO.objetos = [o for o in EquipeDAO.objetos if o.get_id() != id]
        if len(EquipeDAO.objetos) < antes:
            EquipeDAO.Salvar()
            return True
        return False

    # ---- Pesquisa e associacao ----
    @staticmethod
    def Pesquisar_Por_Nome(termo):
        termo = termo.lower()
        return [o for o in EquipeDAO.Listar() if termo in o.get_nome().lower()]

    @staticmethod
    def Listar_Por_Lider(lider_id):
        return [o for o in EquipeDAO.Listar() if o.get_lider_id() == lider_id]
