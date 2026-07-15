"""Interface com o usuario (camada template) do TaskFlow — console.

A UI so conversa com a camada de operacoes (View); nao acessa DAO nem
modelo diretamente. Os enums sao importados apenas para montar os menus.

Executar a partir da raiz do projeto:
    python3 ui.py

Login inicial (criado automaticamente se nao houver usuarios):
    e-mail: admin@taskflow.com
    senha:  admin
"""

from view.view import View
from usuarios.usuario import Perfil
from projetos.projeto import StatusProjeto
from tarefas.tarefa import StatusTarefa, Prioridade


class UI:
    # Usuario autenticado na sessao atual
    usuario_logado = None

    # ------------------------------------------------------------------
    # Ponto de entrada
    # ------------------------------------------------------------------
    @staticmethod
    def Main():
        if View.Garantir_Admin_Inicial():
            print(">> Usuario admin inicial criado (admin@taskflow.com / admin)")
        while True:
            if not UI.Tela_Acesso():
                print("Aplicacao finalizada.")
                break
            UI.Sessao()

    @staticmethod
    def Sessao():
        """Laco principal enquanto ha um usuario logado (ate o logout)."""
        while True:
            op = UI.Menu_Principal()
            if op == 0:
                print(f"Logout de {UI.usuario_logado.get_nome()}. Ate logo!")
                UI.usuario_logado = None
                break
            perfil = UI.usuario_logado.get_perfil()
            if perfil == Perfil.ADMIN and op == 1:
                UI.Menu_Usuario()
            elif perfil == Perfil.ADMIN and op == 2:
                UI.Menu_Equipe()
            elif perfil == Perfil.ADMIN and op == 3:
                UI.Menu_Projeto()
            elif perfil == Perfil.ADMIN and op == 4:
                UI.Menu_Categoria()
            elif perfil == Perfil.ADMIN and op == 8:
                UI.Menu_Sprint()
            elif op == 5:
                UI.Menu_Tarefa()
            elif op == 6:
                UI.Menu_Comentario()
            elif op == 7:
                UI.Menu_Evento()
            else:
                print("Opcao invalida.")

    # ------------------------------------------------------------------
    # Autenticacao
    # ------------------------------------------------------------------
    @staticmethod
    def Tela_Acesso():
        """Menu inicial: entrar ou criar uma nova conta."""
        while True:
            print("\n====== TaskFlow ======")
            print("1 - Entrar")
            print("2 - Criar conta")
            print("0 - Sair")
            op = UI.Ler_Opcao()
            if op == 0:
                return False
            elif op == 1:
                if UI.Login():
                    return True
            elif op == 2:
                UI.Criar_Conta()
            else:
                print("Opcao invalida.")

    @staticmethod
    def Login():
        print("\n=== LOGIN ===")
        email = input("E-mail: ").strip()
        senha = input("Senha: ").strip()
        usuario = View.Usuario_Login(email, senha)
        if usuario:
            UI.usuario_logado = usuario
            print(f"\nBem-vindo(a), {usuario.get_nome()}! Perfil: {usuario.get_perfil().value}")
            return True
        print("E-mail ou senha invalidos.")
        return False

    @staticmethod
    def Criar_Conta():
        try:
            print("\n=== CRIAR CONTA ===")
            nome = input("Nome: ")
            email = input("E-mail: ").strip()
            senha = input("Senha (min. 4 caracteres): ")
            perfil = UI.Ler_Enum("Perfil", Perfil, Perfil.MEMBRO)
            novo = View.Usuario_Inserir(nome, email, senha, perfil)
            print(f"Conta criada com sucesso (id={novo.get_id()})! Agora e so entrar.")
        except Exception as e:
            print(f"Nao foi possivel criar a conta: {e}")

    # ------------------------------------------------------------------
    # Utilitarios de leitura
    # ------------------------------------------------------------------
    @staticmethod
    def Ler_Opcao():
        try:
            return int(input("Escolha: "))
        except ValueError:
            return -1

    @staticmethod
    def Ler_Int(rotulo, padrao=None):
        texto = input(rotulo).strip()
        if not texto and padrao is not None:
            return padrao
        try:
            return int(texto)
        except ValueError:
            return padrao if padrao is not None else 0

    @staticmethod
    def Ler_Enum(rotulo, classe_enum, padrao=None):
        opcoes = list(classe_enum)
        print(f"{rotulo}:")
        for i, e in enumerate(opcoes, 1):
            print(f"  {i} - {e.value}")
        sufixo = f" [{padrao.value}]" if padrao else ""
        escolha = input(f"Numero{sufixo}: ").strip()
        if not escolha and padrao:
            return padrao
        try:
            return opcoes[int(escolha) - 1]
        except (ValueError, IndexError):
            print("Opcao invalida, usando padrao.")
            return padrao or opcoes[0]

    # ------------------------------------------------------------------
    # Menu principal (varia conforme o perfil)
    # ------------------------------------------------------------------
    @staticmethod
    def Menu_Principal():
        print(f"\n=== MENU PRINCIPAL ({UI.usuario_logado.get_perfil().value}) ===")
        if UI.usuario_logado.get_perfil() == Perfil.ADMIN:
            print("1 - Menu Usuario")
            print("2 - Menu Equipe")
            print("3 - Menu Projeto")
            print("4 - Menu Categoria")
            print("8 - Menu Sprint")
        print("5 - Menu Tarefa")
        print("6 - Menu Comentario")
        print("7 - Menu Evento")
        print("0 - Sair (logout)")
        return UI.Ler_Opcao()

    # ==================================================================
    # USUARIO  (somente ADMIN)
    # ==================================================================
    @staticmethod
    def Menu_Usuario():
        while True:
            print("\n=== MENU USUARIO ===")
            print("1 - Listar   2 - Inserir   3 - Atualizar")
            print("4 - Excluir  5 - Pesquisar por nome   0 - Voltar")
            op = UI.Ler_Opcao()
            if op == 0:
                break
            elif op == 1:
                UI.Usuario_Listar()
            elif op == 2:
                UI.Usuario_Inserir()
            elif op == 3:
                UI.Usuario_Atualizar()
            elif op == 4:
                UI.Usuario_Excluir()
            elif op == 5:
                UI.Usuario_Pesquisar()
            else:
                print("Opcao invalida.")

    @staticmethod
    def Usuario_Listar():
        lista = View.Usuario_Listar()
        if not lista:
            print("Nenhum usuario cadastrado.")
            return
        for u in lista:
            print(u)

    @staticmethod
    def Usuario_Inserir():
        try:
            nome = input("Nome: ")
            email = input("Email: ")
            senha = input("Senha: ")
            perfil = UI.Ler_Enum("Perfil", Perfil, Perfil.MEMBRO)
            u = View.Usuario_Inserir(nome, email, senha, perfil)
            print(f"Usuario inserido (id={u.get_id()}).")
        except Exception as e:
            print(f"Erro ao inserir usuario: {e}")

    @staticmethod
    def Usuario_Atualizar():
        try:
            id_ = UI.Ler_Int("Id do usuario para atualizar: ")
            atual = View.Usuario_Listar_Id(id_)
            if atual is None:
                print("Usuario nao encontrado.")
                return
            nome = input(f"Nome [{atual.get_nome()}]: ").strip() or atual.get_nome()
            email = input(f"Email [{atual.get_email()}]: ").strip() or atual.get_email()
            perfil = UI.Ler_Enum("Perfil", Perfil, atual.get_perfil())
            print("Usuario atualizado." if View.Usuario_Atualizar(id_, nome, email, perfil) else "Falhou.")
        except Exception as e:
            print(f"Erro ao atualizar usuario: {e}")

    @staticmethod
    def Usuario_Excluir():
        try:
            id_ = UI.Ler_Int("Id do usuario para excluir: ")
            print("Usuario excluido." if View.Usuario_Excluir(id_) else "Usuario nao encontrado.")
        except Exception as e:
            print(f"Erro ao excluir usuario: {e}")

    @staticmethod
    def Usuario_Pesquisar():
        resultado = View.Usuario_Pesquisar_Nome(input("Parte do nome: "))
        if not resultado:
            print("Nada encontrado.")
            return
        for u in resultado:
            print(u)

    # ==================================================================
    # EQUIPE  (somente ADMIN)
    # ==================================================================
    @staticmethod
    def Menu_Equipe():
        while True:
            print("\n=== MENU EQUIPE ===")
            print("1 - Listar   2 - Inserir   3 - Atualizar   4 - Excluir")
            print("5 - Pesquisar por nome   6 - Gerenciar membros   0 - Voltar")
            op = UI.Ler_Opcao()
            if op == 0:
                break
            elif op == 1:
                UI.Equipe_Listar()
            elif op == 2:
                UI.Equipe_Inserir()
            elif op == 3:
                UI.Equipe_Atualizar()
            elif op == 4:
                UI.Equipe_Excluir()
            elif op == 5:
                UI.Equipe_Pesquisar()
            elif op == 6:
                UI.Equipe_Membros()
            else:
                print("Opcao invalida.")

    @staticmethod
    def Equipe_Membros():
        eq_id = UI.Ler_Int("Id da equipe: ")
        equipe = View.Equipe_Listar_Id(eq_id)
        if equipe is None:
            print("Equipe nao encontrada.")
            return
        print(f"-- Membros de '{equipe.get_nome()}' --")
        for m in View.Equipe_Membros(eq_id):
            print(f"   {m}")
        print("1 - Adicionar membro   2 - Remover membro   0 - Voltar")
        op = UI.Ler_Opcao()
        if op == 1:
            print("-- Usuarios --")
            UI.Usuario_Listar()
            uid = UI.Ler_Int("Id do usuario para adicionar: ")
            print("Membro adicionado." if View.Equipe_Adicionar_Membro(eq_id, uid) else "Falhou.")
        elif op == 2:
            uid = UI.Ler_Int("Id do usuario para remover: ")
            print("Membro removido." if View.Equipe_Remover_Membro(uid) else "Falhou.")

    @staticmethod
    def Equipe_Listar():
        lista = View.Equipe_Listar()
        if not lista:
            print("Nenhuma equipe cadastrada.")
            return
        for e in lista:
            print(e)

    @staticmethod
    def Equipe_Inserir():
        try:
            nome = input("Nome: ")
            descricao = input("Descricao: ")
            print("-- Usuarios disponiveis para liderar --")
            UI.Usuario_Listar()
            lider_id = UI.Ler_Int("Id do lider (0 = nenhum): ", 0)
            e = View.Equipe_Inserir(nome, descricao, lider_id)
            print(f"Equipe inserida (id={e.get_id()}).")
        except Exception as ex:
            print(f"Erro ao inserir equipe: {ex}")

    @staticmethod
    def Equipe_Atualizar():
        try:
            id_ = UI.Ler_Int("Id da equipe para atualizar: ")
            atual = View.Equipe_Listar_Id(id_)
            if atual is None:
                print("Equipe nao encontrada.")
                return
            nome = input(f"Nome [{atual.get_nome()}]: ").strip() or atual.get_nome()
            descricao = input(f"Descricao [{atual.get_descricao()}]: ").strip() or atual.get_descricao()
            lider_id = UI.Ler_Int(f"Id do lider [{atual.get_lider_id()}]: ", atual.get_lider_id())
            print("Equipe atualizada." if View.Equipe_Atualizar(id_, nome, descricao, lider_id) else "Falhou.")
        except Exception as ex:
            print(f"Erro ao atualizar equipe: {ex}")

    @staticmethod
    def Equipe_Excluir():
        try:
            id_ = UI.Ler_Int("Id da equipe para excluir: ")
            print("Equipe excluida." if View.Equipe_Excluir(id_) else "Equipe nao encontrada.")
        except Exception as ex:
            print(f"Erro ao excluir equipe: {ex}")

    @staticmethod
    def Equipe_Pesquisar():
        resultado = View.Equipe_Pesquisar_Nome(input("Parte do nome: "))
        if not resultado:
            print("Nada encontrado.")
            return
        for e in resultado:
            print(e)

    # ==================================================================
    # PROJETO  (somente ADMIN)
    # ==================================================================
    @staticmethod
    def Menu_Projeto():
        while True:
            print("\n=== MENU PROJETO ===")
            print("1 - Listar   2 - Inserir   3 - Atualizar   4 - Excluir")
            print("5 - Pesquisar por nome   6 - Listar por equipe   0 - Voltar")
            op = UI.Ler_Opcao()
            if op == 0:
                break
            elif op == 1:
                UI.Projeto_Listar()
            elif op == 2:
                UI.Projeto_Inserir()
            elif op == 3:
                UI.Projeto_Atualizar()
            elif op == 4:
                UI.Projeto_Excluir()
            elif op == 5:
                UI.Projeto_Pesquisar()
            elif op == 6:
                UI.Projeto_Por_Equipe()
            else:
                print("Opcao invalida.")

    @staticmethod
    def Projeto_Listar():
        lista = View.Projeto_Listar()
        if not lista:
            print("Nenhum projeto cadastrado.")
            return
        for p in lista:
            print(p)

    @staticmethod
    def Projeto_Inserir():
        try:
            nome = input("Nome: ")
            descricao = input("Descricao: ")
            data_inicio = input("Data inicio (AAAA-MM-DD): ")
            data_fim = input("Data fim (AAAA-MM-DD): ")
            status = UI.Ler_Enum("Status", StatusProjeto, StatusProjeto.ATIVO)
            print("-- Equipes disponiveis --")
            UI.Equipe_Listar()
            equipe_id = UI.Ler_Int("Id da equipe: ", 0)
            p = View.Projeto_Inserir(nome, descricao, data_inicio, data_fim, status, equipe_id)
            print(f"Projeto inserido (id={p.get_id()}).")
        except Exception as e:
            print(f"Erro ao inserir projeto: {e}")

    @staticmethod
    def Projeto_Atualizar():
        try:
            id_ = UI.Ler_Int("Id do projeto para atualizar: ")
            atual = View.Projeto_Listar_Id(id_)
            if atual is None:
                print("Projeto nao encontrado.")
                return
            nome = input(f"Nome [{atual.get_nome()}]: ").strip() or atual.get_nome()
            descricao = input(f"Descricao [{atual.get_descricao()}]: ").strip() or atual.get_descricao()
            status = UI.Ler_Enum("Status", StatusProjeto, atual.get_status())
            equipe_id = UI.Ler_Int(f"Id equipe [{atual.get_equipe_id()}]: ", atual.get_equipe_id())
            print("Projeto atualizado." if View.Projeto_Atualizar(id_, nome, descricao, status, equipe_id) else "Falhou.")
        except Exception as e:
            print(f"Erro ao atualizar projeto: {e}")

    @staticmethod
    def Projeto_Excluir():
        try:
            id_ = UI.Ler_Int("Id do projeto para excluir: ")
            print("Projeto excluido." if View.Projeto_Excluir(id_) else "Projeto nao encontrado.")
        except Exception as e:
            print(f"Erro ao excluir projeto: {e}")

    @staticmethod
    def Projeto_Pesquisar():
        resultado = View.Projeto_Pesquisar_Nome(input("Parte do nome: "))
        if not resultado:
            print("Nada encontrado.")
            return
        for p in resultado:
            print(p)

    @staticmethod
    def Projeto_Por_Equipe():
        equipe_id = UI.Ler_Int("Id da equipe: ")
        resultado = View.Projeto_Listar_Por_Equipe(equipe_id)
        if not resultado:
            print("Nenhum projeto para essa equipe.")
            return
        for p in resultado:
            print(p)

    # ==================================================================
    # CATEGORIA  (somente ADMIN)
    # ==================================================================
    @staticmethod
    def Menu_Categoria():
        while True:
            print("\n=== MENU CATEGORIA ===")
            print("1 - Listar   2 - Inserir   3 - Atualizar")
            print("4 - Excluir  5 - Pesquisar por nome   0 - Voltar")
            op = UI.Ler_Opcao()
            if op == 0:
                break
            elif op == 1:
                UI.Categoria_Listar()
            elif op == 2:
                UI.Categoria_Inserir()
            elif op == 3:
                UI.Categoria_Atualizar()
            elif op == 4:
                UI.Categoria_Excluir()
            elif op == 5:
                UI.Categoria_Pesquisar()
            else:
                print("Opcao invalida.")

    @staticmethod
    def Categoria_Listar():
        lista = View.Categoria_Listar()
        if not lista:
            print("Nenhuma categoria cadastrada.")
            return
        for c in lista:
            print(c)

    @staticmethod
    def Categoria_Inserir():
        try:
            nome = input("Nome: ")
            cor = input("Cor (ex: #E53935): ") or "#CCCCCC"
            c = View.Categoria_Inserir(nome, cor)
            print(f"Categoria inserida (id={c.get_id()}).")
        except Exception as e:
            print(f"Erro ao inserir categoria: {e}")

    @staticmethod
    def Categoria_Atualizar():
        try:
            id_ = UI.Ler_Int("Id da categoria para atualizar: ")
            atual = View.Categoria_Listar_Id(id_)
            if atual is None:
                print("Categoria nao encontrada.")
                return
            nome = input(f"Nome [{atual.get_nome()}]: ").strip() or atual.get_nome()
            cor = input(f"Cor [{atual.get_cor()}]: ").strip() or atual.get_cor()
            print("Categoria atualizada." if View.Categoria_Atualizar(id_, nome, cor) else "Falhou.")
        except Exception as e:
            print(f"Erro ao atualizar categoria: {e}")

    @staticmethod
    def Categoria_Excluir():
        try:
            id_ = UI.Ler_Int("Id da categoria para excluir: ")
            print("Categoria excluida." if View.Categoria_Excluir(id_) else "Categoria nao encontrada.")
        except Exception as e:
            print(f"Erro ao excluir categoria: {e}")

    @staticmethod
    def Categoria_Pesquisar():
        resultado = View.Categoria_Pesquisar_Nome(input("Parte do nome: "))
        if not resultado:
            print("Nada encontrado.")
            return
        for c in resultado:
            print(c)

    # ==================================================================
    # SPRINT  (somente ADMIN)
    # ==================================================================
    @staticmethod
    def Menu_Sprint():
        while True:
            print("\n=== MENU SPRINT ===")
            print("1 - Listar   2 - Inserir   3 - Atualizar   4 - Excluir")
            print("5 - Listar por projeto   0 - Voltar")
            op = UI.Ler_Opcao()
            if op == 0:
                break
            elif op == 1:
                UI.Sprint_Listar()
            elif op == 2:
                UI.Sprint_Inserir()
            elif op == 3:
                UI.Sprint_Atualizar()
            elif op == 4:
                UI.Sprint_Excluir()
            elif op == 5:
                UI.Sprint_Por_Projeto()
            else:
                print("Opcao invalida.")

    @staticmethod
    def Sprint_Listar():
        lista = View.Sprint_Listar()
        if not lista:
            print("Nenhuma sprint cadastrada.")
            return
        for s in lista:
            print(s)

    @staticmethod
    def Sprint_Inserir():
        try:
            nome = input("Nome: ")
            objetivo = input("Objetivo: ")
            data_inicio = input("Inicio (AAAA-MM-DD): ")
            data_fim = input("Fim (AAAA-MM-DD): ")
            print("-- Projetos disponiveis --")
            UI.Projeto_Listar()
            projeto_id = UI.Ler_Int("Id do projeto: ", 0)
            s = View.Sprint_Inserir(nome, objetivo, data_inicio, data_fim, projeto_id)
            print(f"Sprint inserida (id={s.get_id()}).")
        except Exception as e:
            print(f"Erro ao inserir sprint: {e}")

    @staticmethod
    def Sprint_Atualizar():
        try:
            id_ = UI.Ler_Int("Id da sprint para atualizar: ")
            atual = View.Sprint_Listar_Id(id_)
            if atual is None:
                print("Sprint nao encontrada.")
                return
            nome = input(f"Nome [{atual.get_nome()}]: ").strip() or atual.get_nome()
            objetivo = input(f"Objetivo [{atual.get_objetivo()}]: ").strip() or atual.get_objetivo()
            inicio = input(f"Inicio [{atual.get_data_inicio()}]: ").strip() or atual.get_data_inicio()
            fim = input(f"Fim [{atual.get_data_fim()}]: ").strip() or atual.get_data_fim()
            print("Sprint atualizada." if View.Sprint_Atualizar(id_, nome, objetivo, inicio, fim) else "Falhou.")
        except Exception as e:
            print(f"Erro ao atualizar sprint: {e}")

    @staticmethod
    def Sprint_Excluir():
        try:
            id_ = UI.Ler_Int("Id da sprint para excluir: ")
            print("Sprint excluida." if View.Sprint_Excluir(id_) else "Sprint nao encontrada.")
        except Exception as e:
            print(f"Erro ao excluir sprint: {e}")

    @staticmethod
    def Sprint_Por_Projeto():
        projeto_id = UI.Ler_Int("Id do projeto: ")
        resultado = View.Sprint_Listar_Por_Projeto(projeto_id)
        if not resultado:
            print("Nenhuma sprint para esse projeto.")
            return
        for s in resultado:
            print(s)

    # ==================================================================
    # TAREFA  (ADMIN e MEMBRO)
    # ==================================================================
    @staticmethod
    def Menu_Tarefa():
        while True:
            print("\n=== MENU TAREFA ===")
            print("1 - Listar   2 - Inserir   3 - Atualizar   4 - Excluir")
            print("5 - Pesquisar por titulo   6 - Listar por projeto")
            print("7 - Concluir tarefa (regra de negocio)   0 - Voltar")
            op = UI.Ler_Opcao()
            if op == 0:
                break
            elif op == 1:
                UI.Tarefa_Listar()
            elif op == 2:
                UI.Tarefa_Inserir()
            elif op == 3:
                UI.Tarefa_Atualizar()
            elif op == 4:
                UI.Tarefa_Excluir()
            elif op == 5:
                UI.Tarefa_Pesquisar()
            elif op == 6:
                UI.Tarefa_Por_Projeto()
            elif op == 7:
                UI.Tarefa_Concluir()
            else:
                print("Opcao invalida.")

    @staticmethod
    def Tarefa_Listar():
        lista = View.Tarefa_Listar()
        if not lista:
            print("Nenhuma tarefa cadastrada.")
            return
        for t in lista:
            print(t)

    @staticmethod
    def Tarefa_Inserir():
        try:
            titulo = input("Titulo: ")
            descricao = input("Descricao: ")
            status = UI.Ler_Enum("Status", StatusTarefa, StatusTarefa.A_FAZER)
            prioridade = UI.Ler_Enum("Prioridade", Prioridade, Prioridade.MEDIA)
            prazo = input("Prazo (AAAA-MM-DD): ")
            print("-- Sprints disponiveis --")
            for s in View.Sprint_Listar():
                print(f"   {s}")
            sprint_id = UI.Ler_Int("Id da sprint: ", 0)
            print("-- Usuarios disponiveis --")
            UI.Usuario_Listar()
            responsavel_id = UI.Ler_Int("Id do responsavel: ", 0)
            print("-- Categorias disponiveis --")
            UI.Categoria_Listar()
            categoria_id = UI.Ler_Int("Id da categoria: ", 0)
            t = View.Tarefa_Inserir(titulo, descricao, status, prioridade, prazo,
                                    sprint_id, responsavel_id, categoria_id)
            print(f"Tarefa inserida (id={t.get_id()}).")
        except Exception as e:
            print(f"Erro ao inserir tarefa: {e}")

    @staticmethod
    def Tarefa_Atualizar():
        try:
            id_ = UI.Ler_Int("Id da tarefa para atualizar: ")
            atual = View.Tarefa_Listar_Id(id_)
            if atual is None:
                print("Tarefa nao encontrada.")
                return
            titulo = input(f"Titulo [{atual.get_titulo()}]: ").strip() or atual.get_titulo()
            descricao = input(f"Descricao [{atual.get_descricao()}]: ").strip() or atual.get_descricao()
            status = UI.Ler_Enum("Status", StatusTarefa, atual.get_status())
            prioridade = UI.Ler_Enum("Prioridade", Prioridade, atual.get_prioridade())
            categoria_id = UI.Ler_Int(f"Id categoria [{atual.get_categoria_id()}]: ", atual.get_categoria_id())
            ok = View.Tarefa_Atualizar(id_, titulo, descricao, status, prioridade, categoria_id)
            print("Tarefa atualizada." if ok else "Falhou.")
        except Exception as e:
            print(f"Erro ao atualizar tarefa: {e}")

    @staticmethod
    def Tarefa_Excluir():
        try:
            id_ = UI.Ler_Int("Id da tarefa para excluir: ")
            print("Tarefa excluida." if View.Tarefa_Excluir(id_) else "Tarefa nao encontrada.")
        except Exception as e:
            print(f"Erro ao excluir tarefa: {e}")

    @staticmethod
    def Tarefa_Pesquisar():
        resultado = View.Tarefa_Pesquisar_Titulo(input("Parte do titulo: "))
        if not resultado:
            print("Nada encontrado.")
            return
        for t in resultado:
            print(t)

    @staticmethod
    def Tarefa_Por_Projeto():
        projeto_id = UI.Ler_Int("Id do projeto: ")
        resultado = View.Tarefa_Listar_Por_Projeto(projeto_id)
        if not resultado:
            print("Nenhuma tarefa para esse projeto.")
            return
        for t in resultado:
            print(t)

    @staticmethod
    def Tarefa_Concluir():
        try:
            id_ = UI.Ler_Int("Id da tarefa a concluir: ")
            resultado = View.Tarefa_Concluir(id_)
            if resultado is None:
                print("Tarefa nao encontrada.")
                return
            tarefa, projeto = resultado
            print(f"Tarefa {tarefa.get_id()} concluida.")
            if projeto:
                print(f">> Todas as tarefas concluidas! Projeto '{projeto.get_nome()}' marcado como CONCLUIDO.")
        except Exception as e:
            print(f"Erro ao concluir tarefa: {e}")

    # ==================================================================
    # COMENTARIO  (ADMIN e MEMBRO)
    # ==================================================================
    @staticmethod
    def Menu_Comentario():
        while True:
            print("\n=== MENU COMENTARIO ===")
            print("1 - Listar por tarefa   2 - Inserir   3 - Atualizar")
            print("4 - Excluir   0 - Voltar")
            op = UI.Ler_Opcao()
            if op == 0:
                break
            elif op == 1:
                UI.Comentario_Por_Tarefa()
            elif op == 2:
                UI.Comentario_Inserir()
            elif op == 3:
                UI.Comentario_Atualizar()
            elif op == 4:
                UI.Comentario_Excluir()
            else:
                print("Opcao invalida.")

    @staticmethod
    def Comentario_Por_Tarefa():
        tarefa_id = UI.Ler_Int("Id da tarefa: ")
        resultado = View.Comentario_Listar_Por_Tarefa(tarefa_id)
        if not resultado:
            print("Nenhum comentario para essa tarefa.")
            return
        for c in resultado:
            print(f"[{c.get_id()}] {c.get_texto()}  (autor_id={c.get_autor_id()})")

    @staticmethod
    def Comentario_Inserir():
        try:
            print("-- Tarefas disponiveis --")
            UI.Tarefa_Listar()
            tarefa_id = UI.Ler_Int("Id da tarefa: ", 0)
            texto = input("Comentario: ")
            # Associacao: o autor e o usuario logado
            c = View.Comentario_Inserir(texto, tarefa_id, UI.usuario_logado.get_id())
            print(f"Comentario inserido (id={c.get_id()}).")
        except Exception as e:
            print(f"Erro ao inserir comentario: {e}")

    @staticmethod
    def Comentario_Atualizar():
        try:
            id_ = UI.Ler_Int("Id do comentario para atualizar: ")
            atual = View.Comentario_Listar_Id(id_)
            if atual is None:
                print("Comentario nao encontrado.")
                return
            texto = input(f"Texto [{atual.get_texto()}]: ").strip() or atual.get_texto()
            print("Comentario atualizado." if View.Comentario_Atualizar(id_, texto) else "Falhou.")
        except Exception as e:
            print(f"Erro ao atualizar comentario: {e}")

    @staticmethod
    def Comentario_Excluir():
        try:
            id_ = UI.Ler_Int("Id do comentario para excluir: ")
            print("Comentario excluido." if View.Comentario_Excluir(id_) else "Comentario nao encontrado.")
        except Exception as e:
            print(f"Erro ao excluir comentario: {e}")

    # ==================================================================
    # EVENTO  (ADMIN e MEMBRO)
    # ==================================================================
    @staticmethod
    def Menu_Evento():
        while True:
            print("\n=== MENU EVENTO (CALENDARIO) ===")
            print("1 - Listar meus eventos   2 - Inserir   3 - Atualizar")
            print("4 - Excluir   5 - Pesquisar por titulo   0 - Voltar")
            op = UI.Ler_Opcao()
            if op == 0:
                break
            elif op == 1:
                UI.Evento_Meus()
            elif op == 2:
                UI.Evento_Inserir()
            elif op == 3:
                UI.Evento_Atualizar()
            elif op == 4:
                UI.Evento_Excluir()
            elif op == 5:
                UI.Evento_Pesquisar()
            else:
                print("Opcao invalida.")

    @staticmethod
    def Evento_Meus():
        resultado = View.Evento_Listar_Por_Usuario(UI.usuario_logado.get_id())
        if not resultado:
            print("Voce nao tem eventos.")
            return
        for e in resultado:
            print(f"{e}  {e.get_data_inicio()} -> {e.get_data_fim()}")

    @staticmethod
    def Evento_Inserir():
        try:
            titulo = input("Titulo: ")
            descricao = input("Descricao: ")
            data_inicio = input("Inicio (AAAA-MM-DDTHH:MM): ")
            data_fim = input("Fim (AAAA-MM-DDTHH:MM): ")
            tarefa_id = UI.Ler_Int("Id da tarefa vinculada (0 = nenhuma): ", 0)
            e = View.Evento_Inserir(titulo, descricao, data_inicio, data_fim,
                                    UI.usuario_logado.get_id(), tarefa_id)
            print(f"Evento inserido (id={e.get_id()}).")
        except Exception as ex:
            print(f"Erro ao inserir evento: {ex}")

    @staticmethod
    def Evento_Atualizar():
        try:
            id_ = UI.Ler_Int("Id do evento para atualizar: ")
            ev = View.Evento_Listar_Id(id_)
            if ev is None:
                print("Evento nao encontrado.")
                return
            titulo = input(f"Titulo [{ev.get_titulo()}]: ").strip() or ev.get_titulo()
            inicio = input(f"Inicio [{ev.get_data_inicio()}]: ").strip() or ev.get_data_inicio()
            fim = input(f"Fim [{ev.get_data_fim()}]: ").strip() or ev.get_data_fim()
            print("Evento atualizado." if View.Evento_Atualizar(id_, titulo, inicio, fim) else "Falhou.")
        except Exception as ex:
            print(f"Erro ao atualizar evento: {ex}")

    @staticmethod
    def Evento_Excluir():
        try:
            id_ = UI.Ler_Int("Id do evento para excluir: ")
            print("Evento excluido." if View.Evento_Excluir(id_) else "Evento nao encontrado.")
        except Exception as ex:
            print(f"Erro ao excluir evento: {ex}")

    @staticmethod
    def Evento_Pesquisar():
        resultado = View.Evento_Pesquisar_Titulo(input("Parte do titulo: "))
        if not resultado:
            print("Nada encontrado.")
            return
        for e in resultado:
            print(e)


if __name__ == "__main__":
    UI.Main()
