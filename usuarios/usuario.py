import json
import os
from enum import Enum


class Perfil(Enum):
    """Perfis de acesso do sistema (controle de login)."""

    ADMIN = "ADMIN"
    MEMBRO = "MEMBRO"

class Usuario:
    def __init__(self, id=0, nome="", email="", senha="", perfil=Perfil.MEMBRO,
                 equipe_id=0):
        self._id = id
        self._nome = nome
        self._email = email
        self._senha = senha
        self._perfil = perfil
        self._equipe_id = equipe_id

    def get_id(self):
        return self._id

    def set_id(self, valor):
        self._id = valor

    def get_nome(self):
        return self._nome

    def set_nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("O nome do usuario nao pode ser vazio.")
        self._nome = valor

    def get_email(self):
        return self._email

    def set_email(self, valor):
        if "@" not in valor:
            raise ValueError("E-mail invalido.")
        self._email = valor

    def get_senha(self):
        return self._senha

    def set_senha(self, valor):
        if len(valor) < 4:
            raise ValueError("A senha deve ter no minimo 4 caracteres.")
        self._senha = valor

    def get_perfil(self):
        return self._perfil

    def set_perfil(self, valor):
        self._perfil = valor

    def get_equipe_id(self):
        return self._equipe_id

    def set_equipe_id(self, valor):
        self._equipe_id = valor

    def eh_admin(self):
        return self._perfil == Perfil.ADMIN

    def to_json(self):
        return {
            "id": self._id,
            "nome": self._nome,
            "email": self._email,
            "senha": self._senha,
            "perfil": self._perfil.value,
            "equipe_id": self._equipe_id,
        }

    @staticmethod
    def from_json(dic):
        return Usuario(
            dic["id"], dic["nome"], dic["email"], dic["senha"],
            Perfil(dic["perfil"]), dic.get("equipe_id", 0),
        )

    def __str__(self):
        return f"Usuario(id={self._id}, nome='{self._nome}', perfil={self._perfil.value})"


# ======================================================================
# PERSISTENCIA (DAO)
# ======================================================================
class UsuarioDAO:
    ARQUIVO = "data/usuarios.json"
    objetos = []

    @staticmethod
    def Abrir():
        if not os.path.exists(UsuarioDAO.ARQUIVO):
            UsuarioDAO.objetos = []
            return
        with open(UsuarioDAO.ARQUIVO, "r", encoding="utf-8") as arquivo:
            UsuarioDAO.objetos = [Usuario.from_json(d) for d in json.load(arquivo)]

    @staticmethod
    def Salvar():
        pasta = os.path.dirname(UsuarioDAO.ARQUIVO)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)
        with open(UsuarioDAO.ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump([o.to_json() for o in UsuarioDAO.objetos], arquivo,
                      ensure_ascii=False, indent=4)

    @staticmethod
    def Inserir(obj):
        UsuarioDAO.Abrir()
        novo_id = 1 if not UsuarioDAO.objetos else max(o.get_id() for o in UsuarioDAO.objetos) + 1
        obj.set_id(novo_id)
        UsuarioDAO.objetos.append(obj)
        UsuarioDAO.Salvar()
        return obj

    @staticmethod
    def Listar():
        UsuarioDAO.Abrir()
        return UsuarioDAO.objetos

    @staticmethod
    def Listar_Id(id):
        UsuarioDAO.Abrir()
        for o in UsuarioDAO.objetos:
            if o.get_id() == id:
                return o
        return None

    @staticmethod
    def Atualizar(obj):
        UsuarioDAO.Abrir()
        for i, o in enumerate(UsuarioDAO.objetos):
            if o.get_id() == obj.get_id():
                UsuarioDAO.objetos[i] = obj
                UsuarioDAO.Salvar()
                return True
        return False

    @staticmethod
    def Excluir(id):
        UsuarioDAO.Abrir()
        antes = len(UsuarioDAO.objetos)
        UsuarioDAO.objetos = [o for o in UsuarioDAO.objetos if o.get_id() != id]
        if len(UsuarioDAO.objetos) < antes:
            UsuarioDAO.Salvar()
            return True
        return False

    # ---- Pesquisa e associacao ----
    @staticmethod
    def Buscar_Por_Email(email):
        for o in UsuarioDAO.Listar():
            if o.get_email() == email:
                return o
        return None

    @staticmethod
    def Pesquisar_Por_Nome(termo):
        termo = termo.lower()
        return [o for o in UsuarioDAO.Listar() if termo in o.get_nome().lower()]

    @staticmethod
    def Listar_Por_Equipe(equipe_id):
        """Associacao 1->N: usuarios (membros) de uma equipe."""
        return [o for o in UsuarioDAO.Listar() if o.get_equipe_id() == equipe_id]
