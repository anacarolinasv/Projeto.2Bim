import json
import os

class Comentario:
    def __init__(self, id=0, texto="", data_criacao="", tarefa_id=0, autor_id=0):
        self._id = id
        self._texto = texto
        self._data_criacao = data_criacao
        self._tarefa_id = tarefa_id
        self._autor_id = autor_id

    def get_id(self):
        return self._id

    def set_id(self, valor):
        self._id = valor

    def get_texto(self):
        return self._texto

    def set_texto(self, valor):
        if not valor or not valor.strip():
            raise ValueError("O texto do comentario nao pode ser vazio.")
        self._texto = valor

    def get_data_criacao(self):
        return self._data_criacao

    def set_data_criacao(self, valor):
        self._data_criacao = valor

    def get_tarefa_id(self):
        return self._tarefa_id

    def set_tarefa_id(self, valor):
        self._tarefa_id = valor

    def get_autor_id(self):
        return self._autor_id

    def set_autor_id(self, valor):
        self._autor_id = valor

    def to_json(self):
        return {
            "id": self._id,
            "texto": self._texto,
            "data_criacao": self._data_criacao,
            "tarefa_id": self._tarefa_id,
            "autor_id": self._autor_id,
        }

    @staticmethod
    def from_json(dic):
        return Comentario(
            dic["id"], dic["texto"], dic["data_criacao"],
            dic["tarefa_id"], dic["autor_id"],
        )

    def __str__(self):
        return f"Comentario(id={self._id}, tarefa_id={self._tarefa_id})"


# ======================================================================
# PERSISTENCIA (DAO)
# ======================================================================
class ComentarioDAO:
    ARQUIVO = "data/comentarios.json"
    objetos = []

    @staticmethod
    def Abrir():
        if not os.path.exists(ComentarioDAO.ARQUIVO):
            ComentarioDAO.objetos = []
            return
        with open(ComentarioDAO.ARQUIVO, "r", encoding="utf-8") as arquivo:
            ComentarioDAO.objetos = [Comentario.from_json(d) for d in json.load(arquivo)]

    @staticmethod
    def Salvar():
        pasta = os.path.dirname(ComentarioDAO.ARQUIVO)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)
        with open(ComentarioDAO.ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump([o.to_json() for o in ComentarioDAO.objetos], arquivo,
                      ensure_ascii=False, indent=4)

    @staticmethod
    def Inserir(obj):
        ComentarioDAO.Abrir()
        novo_id = 1 if not ComentarioDAO.objetos else max(o.get_id() for o in ComentarioDAO.objetos) + 1
        obj.set_id(novo_id)
        ComentarioDAO.objetos.append(obj)
        ComentarioDAO.Salvar()
        return obj

    @staticmethod
    def Listar():
        ComentarioDAO.Abrir()
        return ComentarioDAO.objetos

    @staticmethod
    def Listar_Id(id):
        ComentarioDAO.Abrir()
        for o in ComentarioDAO.objetos:
            if o.get_id() == id:
                return o
        return None

    @staticmethod
    def Atualizar(obj):
        ComentarioDAO.Abrir()
        for i, o in enumerate(ComentarioDAO.objetos):
            if o.get_id() == obj.get_id():
                ComentarioDAO.objetos[i] = obj
                ComentarioDAO.Salvar()
                return True
        return False

    @staticmethod
    def Excluir(id):
        ComentarioDAO.Abrir()
        antes = len(ComentarioDAO.objetos)
        ComentarioDAO.objetos = [o for o in ComentarioDAO.objetos if o.get_id() != id]
        if len(ComentarioDAO.objetos) < antes:
            ComentarioDAO.Salvar()
            return True
        return False

    # ---- Associacao ----
    @staticmethod
    def Listar_Por_Tarefa(tarefa_id):
        return [o for o in ComentarioDAO.Listar() if o.get_tarefa_id() == tarefa_id]

    @staticmethod
    def Listar_Por_Autor(autor_id):
        return [o for o in ComentarioDAO.Listar() if o.get_autor_id() == autor_id]
