import json
import os

class Categoria:
    def __init__(self, id=0, nome="", cor="#CCCCCC"):
        self._id = id
        self._nome = nome
        self._cor = cor

    def get_id(self):
        return self._id

    def set_id(self, valor):
        self._id = valor

    def get_nome(self):
        return self._nome

    def set_nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("O nome da categoria nao pode ser vazio.")
        self._nome = valor

    def get_cor(self):
        return self._cor

    def set_cor(self, valor):
        self._cor = valor

    def to_json(self):
        return {"id": self._id, "nome": self._nome, "cor": self._cor}

    @staticmethod
    def from_json(dic):
        return Categoria(dic["id"], dic["nome"], dic["cor"])

    def __str__(self):
        return f"Categoria(id={self._id}, nome='{self._nome}')"


# ======================================================================
# PERSISTENCIA (DAO)
# ======================================================================
class CategoriaDAO:
    ARQUIVO = "data/categorias.json"
    objetos = []

    @staticmethod
    def Abrir():
        if not os.path.exists(CategoriaDAO.ARQUIVO):
            CategoriaDAO.objetos = []
            return
        with open(CategoriaDAO.ARQUIVO, "r", encoding="utf-8") as arquivo:
            CategoriaDAO.objetos = [Categoria.from_json(d) for d in json.load(arquivo)]

    @staticmethod
    def Salvar():
        pasta = os.path.dirname(CategoriaDAO.ARQUIVO)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)
        with open(CategoriaDAO.ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump([o.to_json() for o in CategoriaDAO.objetos], arquivo,
                      ensure_ascii=False, indent=4)

    @staticmethod
    def Inserir(obj):
        CategoriaDAO.Abrir()
        novo_id = 1 if not CategoriaDAO.objetos else max(o.get_id() for o in CategoriaDAO.objetos) + 1
        obj.set_id(novo_id)
        CategoriaDAO.objetos.append(obj)
        CategoriaDAO.Salvar()
        return obj

    @staticmethod
    def Listar():
        CategoriaDAO.Abrir()
        return CategoriaDAO.objetos

    @staticmethod
    def Listar_Id(id):
        CategoriaDAO.Abrir()
        for o in CategoriaDAO.objetos:
            if o.get_id() == id:
                return o
        return None

    @staticmethod
    def Atualizar(obj):
        CategoriaDAO.Abrir()
        for i, o in enumerate(CategoriaDAO.objetos):
            if o.get_id() == obj.get_id():
                CategoriaDAO.objetos[i] = obj
                CategoriaDAO.Salvar()
                return True
        return False

    @staticmethod
    def Excluir(id):
        CategoriaDAO.Abrir()
        antes = len(CategoriaDAO.objetos)
        CategoriaDAO.objetos = [o for o in CategoriaDAO.objetos if o.get_id() != id]
        if len(CategoriaDAO.objetos) < antes:
            CategoriaDAO.Salvar()
            return True
        return False

    # ---- Pesquisa ----
    @staticmethod
    def Pesquisar_Por_Nome(termo):
        termo = termo.lower()
        return [o for o in CategoriaDAO.Listar() if termo in o.get_nome().lower()]
