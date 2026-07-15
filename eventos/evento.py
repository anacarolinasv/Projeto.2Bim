import json
import os

class Evento:
    def __init__(self, id=0, titulo="", descricao="", data_inicio="",
                 data_fim="", usuario_id=0, tarefa_id=0):
        self._id = id
        self._titulo = titulo
        self._descricao = descricao
        self._data_inicio = data_inicio
        self._data_fim = data_fim
        self._usuario_id = usuario_id
        self._tarefa_id = tarefa_id

    def get_id(self):
        return self._id

    def set_id(self, valor):
        self._id = valor

    def get_titulo(self):
        return self._titulo

    def set_titulo(self, valor):
        if not valor or not valor.strip():
            raise ValueError("O titulo do evento nao pode ser vazio.")
        self._titulo = valor

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

    def get_usuario_id(self):
        return self._usuario_id

    def set_usuario_id(self, valor):
        self._usuario_id = valor

    def get_tarefa_id(self):
        return self._tarefa_id

    def set_tarefa_id(self, valor):
        self._tarefa_id = valor

    def to_json(self):
        return {
            "id": self._id,
            "titulo": self._titulo,
            "descricao": self._descricao,
            "data_inicio": self._data_inicio,
            "data_fim": self._data_fim,
            "usuario_id": self._usuario_id,
            "tarefa_id": self._tarefa_id,
        }

    @staticmethod
    def from_json(dic):
        return Evento(
            dic["id"], dic["titulo"], dic["descricao"], dic["data_inicio"],
            dic["data_fim"], dic["usuario_id"], dic["tarefa_id"],
        )

    def __str__(self):
        return f"Evento(id={self._id}, titulo='{self._titulo}')"


# ======================================================================
# PERSISTENCIA (DAO)
# ======================================================================
class EventoDAO:
    ARQUIVO = "data/eventos.json"
    objetos = []

    @staticmethod
    def Abrir():
        if not os.path.exists(EventoDAO.ARQUIVO):
            EventoDAO.objetos = []
            return
        with open(EventoDAO.ARQUIVO, "r", encoding="utf-8") as arquivo:
            EventoDAO.objetos = [Evento.from_json(d) for d in json.load(arquivo)]

    @staticmethod
    def Salvar():
        pasta = os.path.dirname(EventoDAO.ARQUIVO)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)
        with open(EventoDAO.ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump([o.to_json() for o in EventoDAO.objetos], arquivo,
                      ensure_ascii=False, indent=4)

    @staticmethod
    def Inserir(obj):
        EventoDAO.Abrir()
        novo_id = 1 if not EventoDAO.objetos else max(o.get_id() for o in EventoDAO.objetos) + 1
        obj.set_id(novo_id)
        EventoDAO.objetos.append(obj)
        EventoDAO.Salvar()
        return obj

    @staticmethod
    def Listar():
        EventoDAO.Abrir()
        return EventoDAO.objetos

    @staticmethod
    def Listar_Id(id):
        EventoDAO.Abrir()
        for o in EventoDAO.objetos:
            if o.get_id() == id:
                return o
        return None

    @staticmethod
    def Atualizar(obj):
        EventoDAO.Abrir()
        for i, o in enumerate(EventoDAO.objetos):
            if o.get_id() == obj.get_id():
                EventoDAO.objetos[i] = obj
                EventoDAO.Salvar()
                return True
        return False

    @staticmethod
    def Excluir(id):
        EventoDAO.Abrir()
        antes = len(EventoDAO.objetos)
        EventoDAO.objetos = [o for o in EventoDAO.objetos if o.get_id() != id]
        if len(EventoDAO.objetos) < antes:
            EventoDAO.Salvar()
            return True
        return False

    # ---- Pesquisa e associacao ----
    @staticmethod
    def Pesquisar_Por_Titulo(termo):
        termo = termo.lower()
        return [o for o in EventoDAO.Listar() if termo in o.get_titulo().lower()]

    @staticmethod
    def Listar_Por_Usuario(usuario_id):
        return [o for o in EventoDAO.Listar() if o.get_usuario_id() == usuario_id]

    @staticmethod
    def Listar_Por_Tarefa(tarefa_id):
        return [o for o in EventoDAO.Listar() if o.get_tarefa_id() == tarefa_id]
