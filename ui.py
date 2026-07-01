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
from cores import C


class UI:
    # Usuario autenticado na sessao atual
    usuario_logado = None

    @staticmethod
    def _listar(itens):
        for item in itens:
            print(C.item(item))

    # ------------------------------------------------------------------
    # Ponto de entrada
    # ------------------------------------------------------------------
    @staticmethod
    def Main():
        if View.Garantir_Admin_Inicial():
            print(C.aviso("Usuario admin inicial criado (admin@taskflow.com / admin)"))
        if not UI.Tela_Acesso():
            print(C.info("Encerrando."))
            return
        while True:
            op = UI.Menu_Principal()
            if op == 0:
                print(C.info("Aplicacao finalizada."))
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
            elif op == 5:
                UI.Menu_Tarefa()
            elif op == 6:
                UI.Menu_Comentario()
            elif op == 7:
                UI.Menu_Evento()
            else:
                print(C.erro("Opcao invalida."))

    # ------------------------------------------------------------------
    # Autenticacao
    # ------------------------------------------------------------------
    @staticmethod
    def Tela_Acesso():
        """Menu inicial: entrar ou criar uma nova conta."""
        while True:
            print(C.banner())
            print(C.opcao(1, "Entrar"))
            print(C.opcao(2, "Criar conta"))
            print(C.opcao_sair("Sair"))
            op = UI.Ler_Opcao()
            if op == 0:
                return False
            elif op == 1:
                if UI.Login():
                    return True
            elif op == 2:
                UI.Criar_Conta()
            else:
                print(C.erro("Opcao invalida."))

    @staticmethod
    def Login():
        print(C.menu_titulo("LOGIN"))
        email = input(C.prompt("E-mail: ")).strip()
        senha = input(C.prompt("Senha: ")).strip()
        usuario = View.Usuario_Login(email, senha)
        if usuario:
            UI.usuario_logado = usuario
            print(C.destaque(
                f"\nBem-vindo(a), {usuario.get_nome()}! Perfil: {usuario.get_perfil().value}"
            ))
            return True
        print(C.erro("E-mail ou senha invalidos."))
        return False

    @staticmethod
    def Criar_Conta():
        try:
            print(C.menu_titulo("CRIAR CONTA"))
            nome = input(C.prompt("Nome: "))
            email = input(C.prompt("E-mail: ")).strip()
            senha = input(C.prompt("Senha (min. 4 caracteres): "))
            perfil = UI.Ler_Enum("Perfil", Perfil, Perfil.MEMBRO)
            novo = View.Usuario_Inserir(nome, email, senha, perfil)
            print(C.sucesso(f"Conta criada com sucesso (id={novo.get_id()})! Agora e so entrar."))
        except Exception as e:
            print(C.erro(f"Nao foi possivel criar a conta: {e}"))

    # ------------------------------------------------------------------
    # Utilitarios de leitura
    # ------------------------------------------------------------------
    @staticmethod
    def Ler_Opcao():
        try:
            return int(input(C.prompt("Escolha: ")))
        except ValueError:
            return -1

    @staticmethod
    def Ler_Int(rotulo, padrao=None):
        texto = input(C.prompt(rotulo)).strip()
        if not texto and padrao is not None:
            return padrao
        try:
            return int(texto)
        except ValueError:
            return padrao if padrao is not None else 0

    @staticmethod
    def Ler_Enum(rotulo, classe_enum, padrao=None):
        opcoes = list(classe_enum)
        print(C.wrap(f"{rotulo}:", C.YELLOW, C.BOLD))
        for i, e in enumerate(opcoes, 1):
            print(f"  {C.opcao(i, e.value)}")
        sufixo = f" [{padrao.value}]" if padrao else ""
        escolha = input(C.prompt(f"Numero{sufixo}: ")).strip()
        if not escolha and padrao:
            return padrao
        try:
            return opcoes[int(escolha) - 1]
        except (ValueError, IndexError):
            print(C.aviso("Opcao invalida, usando padrao."))
            return padrao or opcoes[0]

    # ------------------------------------------------------------------
    # Menu principal (varia conforme o perfil)
    # ------------------------------------------------------------------
    @staticmethod
    def Menu_Principal():
        perfil = UI.usuario_logado.get_perfil().value
        print(C.menu_titulo(f"MENU PRINCIPAL ({perfil})"))
        if UI.usuario_logado.get_perfil() == Perfil.ADMIN:
            print(C.opcao(1, "Menu Usuario"))
            print(C.opcao(2, "Menu Equipe"))
            print(C.opcao(3, "Menu Projeto"))
            print(C.opcao(4, "Menu Categoria"))
        print(C.opcao(5, "Menu Tarefa"))
        print(C.opcao(6, "Menu Comentario"))
        print(C.opcao(7, "Menu Evento"))
        print(C.opcao_sair("Sair"))
        return UI.Ler_Opcao()

    # ==================================================================
    # USUARIO  (somente ADMIN)
    # ==================================================================
    @staticmethod
    def Menu_Usuario():
        while True:
            print(C.menu_titulo("MENU USUARIO"))
            print(C.opcoes((1, "Listar"), (2, "Inserir"), (3, "Atualizar")))
            print(C.opcoes((4, "Excluir"), (5, "Pesquisar por nome")))
            print(C.opcao_sair("Voltar"))
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
                print(C.erro("Opcao invalida."))

    @staticmethod
    def Usuario_Listar():
        lista = View.Usuario_Listar()
        if not lista:
            print(C.info("Nenhum usuario cadastrado."))
            return
        UI._listar(lista)

    @staticmethod
    def Usuario_Inserir():
        try:
            nome = input(C.prompt("Nome: "))
            email = input(C.prompt("Email: "))
            senha = input(C.prompt("Senha: "))
            perfil = UI.Ler_Enum("Perfil", Perfil, Perfil.MEMBRO)
            u = View.Usuario_Inserir(nome, email, senha, perfil)
            print(C.sucesso(f"Usuario inserido (id={u.get_id()})."))
        except Exception as e:
            print(C.erro(f"Erro ao inserir usuario: {e}"))

    @staticmethod
    def Usuario_Atualizar():
        try:
            id_ = UI.Ler_Int("Id do usuario para atualizar: ")
            atual = View.Usuario_Listar_Id(id_)
            if atual is None:
                print(C.erro("Usuario nao encontrado."))
                return
            nome = input(C.prompt(f"Nome [{atual.get_nome()}]: ")).strip() or atual.get_nome()
            email = input(C.prompt(f"Email [{atual.get_email()}]: ")).strip() or atual.get_email()
            perfil = UI.Ler_Enum("Perfil", Perfil, atual.get_perfil())
            if View.Usuario_Atualizar(id_, nome, email, perfil):
                print(C.sucesso("Usuario atualizado."))
            else:
                print(C.erro("Falhou."))
        except Exception as e:
            print(C.erro(f"Erro ao atualizar usuario: {e}"))

    @staticmethod
    def Usuario_Excluir():
        try:
            id_ = UI.Ler_Int("Id do usuario para excluir: ")
            if View.Usuario_Excluir(id_):
                print(C.sucesso("Usuario excluido."))
            else:
                print(C.erro("Usuario nao encontrado."))
        except Exception as e:
            print(C.erro(f"Erro ao excluir usuario: {e}"))

    @staticmethod
    def Usuario_Pesquisar():
        resultado = View.Usuario_Pesquisar_Nome(input(C.prompt("Parte do nome: ")))
        if not resultado:
            print(C.info("Nada encontrado."))
            return
        UI._listar(resultado)

    # ==================================================================
    # EQUIPE  (somente ADMIN)
    # ==================================================================
    @staticmethod
    def Menu_Equipe():
        while True:
            print(C.menu_titulo("MENU EQUIPE"))
            print(C.opcoes((1, "Listar"), (2, "Inserir"), (3, "Atualizar")))
            print(C.opcoes((4, "Excluir"), (5, "Pesquisar por nome")))
            print(C.opcao_sair("Voltar"))
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
            else:
                print(C.erro("Opcao invalida."))

    @staticmethod
    def Equipe_Listar():
        lista = View.Equipe_Listar()
        if not lista:
            print(C.info("Nenhuma equipe cadastrada."))
            return
        UI._listar(lista)

    @staticmethod
    def Equipe_Inserir():
        try:
            nome = input(C.prompt("Nome: "))
            descricao = input(C.prompt("Descricao: "))
            print(C.secao("Usuarios disponiveis para liderar"))
            UI.Usuario_Listar()
            lider_id = UI.Ler_Int("Id do lider (0 = nenhum): ", 0)
            e = View.Equipe_Inserir(nome, descricao, lider_id)
            print(C.sucesso(f"Equipe inserida (id={e.get_id()})."))
        except Exception as ex:
            print(C.erro(f"Erro ao inserir equipe: {ex}"))

    @staticmethod
    def Equipe_Atualizar():
        try:
            id_ = UI.Ler_Int("Id da equipe para atualizar: ")
            atual = View.Equipe_Listar_Id(id_)
            if atual is None:
                print(C.erro("Equipe nao encontrada."))
                return
            nome = input(C.prompt(f"Nome [{atual.get_nome()}]: ")).strip() or atual.get_nome()
            descricao = input(C.prompt(f"Descricao [{atual.get_descricao()}]: ")).strip() or atual.get_descricao()
            lider_id = UI.Ler_Int(f"Id do lider [{atual.get_lider_id()}]: ", atual.get_lider_id())
            if View.Equipe_Atualizar(id_, nome, descricao, lider_id):
                print(C.sucesso("Equipe atualizada."))
            else:
                print(C.erro("Falhou."))
        except Exception as ex:
            print(C.erro(f"Erro ao atualizar equipe: {ex}"))

    @staticmethod
    def Equipe_Excluir():
        try:
            id_ = UI.Ler_Int("Id da equipe para excluir: ")
            if View.Equipe_Excluir(id_):
                print(C.sucesso("Equipe excluida."))
            else:
                print(C.erro("Equipe nao encontrada."))
        except Exception as ex:
            print(C.erro(f"Erro ao excluir equipe: {ex}"))

    @staticmethod
    def Equipe_Pesquisar():
        resultado = View.Equipe_Pesquisar_Nome(input(C.prompt("Parte do nome: ")))
        if not resultado:
            print(C.info("Nada encontrado."))
            return
        UI._listar(resultado)

    # ==================================================================
    # PROJETO  (somente ADMIN)
    # ==================================================================
    @staticmethod
    def Menu_Projeto():
        while True:
            print(C.menu_titulo("MENU PROJETO"))
            print(C.opcoes((1, "Listar"), (2, "Inserir"), (3, "Atualizar"), (4, "Excluir")))
            print(C.opcoes((5, "Pesquisar por nome"), (6, "Listar por equipe")))
            print(C.opcao_sair("Voltar"))
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
                print(C.erro("Opcao invalida."))

    @staticmethod
    def Projeto_Listar():
        lista = View.Projeto_Listar()
        if not lista:
            print(C.info("Nenhum projeto cadastrado."))
            return
        UI._listar(lista)

    @staticmethod
    def Projeto_Inserir():
        try:
            nome = input(C.prompt("Nome: "))
            descricao = input(C.prompt("Descricao: "))
            data_inicio = input(C.prompt("Data inicio (AAAA-MM-DD): "))
            data_fim = input(C.prompt("Data fim (AAAA-MM-DD): "))
            status = UI.Ler_Enum("Status", StatusProjeto, StatusProjeto.ATIVO)
            print(C.secao("Equipes disponiveis"))
            UI.Equipe_Listar()
            equipe_id = UI.Ler_Int("Id da equipe: ", 0)
            p = View.Projeto_Inserir(nome, descricao, data_inicio, data_fim, status, equipe_id)
            print(C.sucesso(f"Projeto inserido (id={p.get_id()})."))
        except Exception as e:
            print(C.erro(f"Erro ao inserir projeto: {e}"))

    @staticmethod
    def Projeto_Atualizar():
        try:
            id_ = UI.Ler_Int("Id do projeto para atualizar: ")
            atual = View.Projeto_Listar_Id(id_)
            if atual is None:
                print(C.erro("Projeto nao encontrado."))
                return
            nome = input(C.prompt(f"Nome [{atual.get_nome()}]: ")).strip() or atual.get_nome()
            descricao = input(C.prompt(f"Descricao [{atual.get_descricao()}]: ")).strip() or atual.get_descricao()
            status = UI.Ler_Enum("Status", StatusProjeto, atual.get_status())
            equipe_id = UI.Ler_Int(f"Id equipe [{atual.get_equipe_id()}]: ", atual.get_equipe_id())
            if View.Projeto_Atualizar(id_, nome, descricao, status, equipe_id):
                print(C.sucesso("Projeto atualizado."))
            else:
                print(C.erro("Falhou."))
        except Exception as e:
            print(C.erro(f"Erro ao atualizar projeto: {e}"))

    @staticmethod
    def Projeto_Excluir():
        try:
            id_ = UI.Ler_Int("Id do projeto para excluir: ")
            if View.Projeto_Excluir(id_):
                print(C.sucesso("Projeto excluido."))
            else:
                print(C.erro("Projeto nao encontrado."))
        except Exception as e:
            print(C.erro(f"Erro ao excluir projeto: {e}"))

    @staticmethod
    def Projeto_Pesquisar():
        resultado = View.Projeto_Pesquisar_Nome(input(C.prompt("Parte do nome: ")))
        if not resultado:
            print(C.info("Nada encontrado."))
            return
        UI._listar(resultado)

    @staticmethod
    def Projeto_Por_Equipe():
        equipe_id = UI.Ler_Int("Id da equipe: ")
        resultado = View.Projeto_Listar_Por_Equipe(equipe_id)
        if not resultado:
            print(C.info("Nenhum projeto para essa equipe."))
            return
        UI._listar(resultado)

    # ==================================================================
    # CATEGORIA  (somente ADMIN)
    # ==================================================================
    @staticmethod
    def Menu_Categoria():
        while True:
            print(C.menu_titulo("MENU CATEGORIA"))
            print(C.opcoes((1, "Listar"), (2, "Inserir"), (3, "Atualizar")))
            print(C.opcoes((4, "Excluir"), (5, "Pesquisar por nome")))
            print(C.opcao_sair("Voltar"))
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
                print(C.erro("Opcao invalida."))

    @staticmethod
    def Categoria_Listar():
        lista = View.Categoria_Listar()
        if not lista:
            print(C.info("Nenhuma categoria cadastrada."))
            return
        UI._listar(lista)

    @staticmethod
    def Categoria_Inserir():
        try:
            nome = input(C.prompt("Nome: "))
            cor = input(C.prompt("Cor (ex: #E53935): ")) or "#CCCCCC"
            c = View.Categoria_Inserir(nome, cor)
            print(C.sucesso(f"Categoria inserida (id={c.get_id()})."))
        except Exception as e:
            print(C.erro(f"Erro ao inserir categoria: {e}"))

    @staticmethod
    def Categoria_Atualizar():
        try:
            id_ = UI.Ler_Int("Id da categoria para atualizar: ")
            atual = View.Categoria_Listar_Id(id_)
            if atual is None:
                print(C.erro("Categoria nao encontrada."))
                return
            nome = input(C.prompt(f"Nome [{atual.get_nome()}]: ")).strip() or atual.get_nome()
            cor = input(C.prompt(f"Cor [{atual.get_cor()}]: ")).strip() or atual.get_cor()
            if View.Categoria_Atualizar(id_, nome, cor):
                print(C.sucesso("Categoria atualizada."))
            else:
                print(C.erro("Falhou."))
        except Exception as e:
            print(C.erro(f"Erro ao atualizar categoria: {e}"))

    @staticmethod
    def Categoria_Excluir():
        try:
            id_ = UI.Ler_Int("Id da categoria para excluir: ")
            if View.Categoria_Excluir(id_):
                print(C.sucesso("Categoria excluida."))
            else:
                print(C.erro("Categoria nao encontrada."))
        except Exception as e:
            print(C.erro(f"Erro ao excluir categoria: {e}"))

    @staticmethod
    def Categoria_Pesquisar():
        resultado = View.Categoria_Pesquisar_Nome(input(C.prompt("Parte do nome: ")))
        if not resultado:
            print(C.info("Nada encontrado."))
            return
        UI._listar(resultado)

    # ==================================================================
    # TAREFA  (ADMIN e MEMBRO)
    # ==================================================================
    @staticmethod
    def Menu_Tarefa():
        while True:
            print(C.menu_titulo("MENU TAREFA"))
            print(C.opcoes((1, "Listar"), (2, "Inserir"), (3, "Atualizar"), (4, "Excluir")))
            print(C.opcoes((5, "Pesquisar por titulo"), (6, "Listar por projeto")))
            print(C.opcao(7, "Concluir tarefa (regra de negocio)"))
            print(C.opcao_sair("Voltar"))
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
                print(C.erro("Opcao invalida."))

    @staticmethod
    def Tarefa_Listar():
        lista = View.Tarefa_Listar()
        if not lista:
            print(C.info("Nenhuma tarefa cadastrada."))
            return
        UI._listar(lista)

    @staticmethod
    def Tarefa_Inserir():
        try:
            titulo = input(C.prompt("Titulo: "))
            descricao = input(C.prompt("Descricao: "))
            status = UI.Ler_Enum("Status", StatusTarefa, StatusTarefa.A_FAZER)
            prioridade = UI.Ler_Enum("Prioridade", Prioridade, Prioridade.MEDIA)
            prazo = input(C.prompt("Prazo (AAAA-MM-DD): "))
            print(C.secao("Projetos disponiveis"))
            UI.Projeto_Listar()
            projeto_id = UI.Ler_Int("Id do projeto: ", 0)
            print(C.secao("Usuarios disponiveis"))
            UI.Usuario_Listar()
            responsavel_id = UI.Ler_Int("Id do responsavel: ", 0)
            print(C.secao("Categorias disponiveis"))
            UI.Categoria_Listar()
            categoria_id = UI.Ler_Int("Id da categoria: ", 0)
            t = View.Tarefa_Inserir(titulo, descricao, status, prioridade, prazo,
                                    projeto_id, responsavel_id, categoria_id)
            print(C.sucesso(f"Tarefa inserida (id={t.get_id()})."))
        except Exception as e:
            print(C.erro(f"Erro ao inserir tarefa: {e}"))

    @staticmethod
    def Tarefa_Atualizar():
        try:
            id_ = UI.Ler_Int("Id da tarefa para atualizar: ")
            atual = View.Tarefa_Listar_Id(id_)
            if atual is None:
                print(C.erro("Tarefa nao encontrada."))
                return
            titulo = input(C.prompt(f"Titulo [{atual.get_titulo()}]: ")).strip() or atual.get_titulo()
            descricao = input(C.prompt(f"Descricao [{atual.get_descricao()}]: ")).strip() or atual.get_descricao()
            status = UI.Ler_Enum("Status", StatusTarefa, atual.get_status())
            prioridade = UI.Ler_Enum("Prioridade", Prioridade, atual.get_prioridade())
            categoria_id = UI.Ler_Int(f"Id categoria [{atual.get_categoria_id()}]: ", atual.get_categoria_id())
            ok = View.Tarefa_Atualizar(id_, titulo, descricao, status, prioridade, categoria_id)
            print(C.sucesso("Tarefa atualizada.") if ok else C.erro("Falhou."))
        except Exception as e:
            print(C.erro(f"Erro ao atualizar tarefa: {e}"))

    @staticmethod
    def Tarefa_Excluir():
        try:
            id_ = UI.Ler_Int("Id da tarefa para excluir: ")
            if View.Tarefa_Excluir(id_):
                print(C.sucesso("Tarefa excluida."))
            else:
                print(C.erro("Tarefa nao encontrada."))
        except Exception as e:
            print(C.erro(f"Erro ao excluir tarefa: {e}"))

    @staticmethod
    def Tarefa_Pesquisar():
        resultado = View.Tarefa_Pesquisar_Titulo(input(C.prompt("Parte do titulo: ")))
        if not resultado:
            print(C.info("Nada encontrado."))
            return
        UI._listar(resultado)

    @staticmethod
    def Tarefa_Por_Projeto():
        projeto_id = UI.Ler_Int("Id do projeto: ")
        resultado = View.Tarefa_Listar_Por_Projeto(projeto_id)
        if not resultado:
            print(C.info("Nenhuma tarefa para esse projeto."))
            return
        UI._listar(resultado)

    @staticmethod
    def Tarefa_Concluir():
        try:
            id_ = UI.Ler_Int("Id da tarefa a concluir: ")
            resultado = View.Tarefa_Concluir(id_)
            if resultado is None:
                print(C.erro("Tarefa nao encontrada."))
                return
            tarefa, projeto = resultado
            print(C.sucesso(f"Tarefa {tarefa.get_id()} concluida."))
            if projeto:
                print(C.destaque(
                    f"Todas as tarefas concluidas! Projeto '{projeto.get_nome()}' marcado como CONCLUIDO."
                ))
        except Exception as e:
            print(C.erro(f"Erro ao concluir tarefa: {e}"))

    # ==================================================================
    # COMENTARIO  (ADMIN e MEMBRO)
    # ==================================================================
    @staticmethod
    def Menu_Comentario():
        while True:
            print(C.menu_titulo("MENU COMENTARIO"))
            print(C.opcoes((1, "Listar por tarefa"), (2, "Inserir"), (3, "Excluir")))
            print(C.opcao_sair("Voltar"))
            op = UI.Ler_Opcao()
            if op == 0:
                break
            elif op == 1:
                UI.Comentario_Por_Tarefa()
            elif op == 2:
                UI.Comentario_Inserir()
            elif op == 3:
                UI.Comentario_Excluir()
            else:
                print(C.erro("Opcao invalida."))

    @staticmethod
    def Comentario_Por_Tarefa():
        tarefa_id = UI.Ler_Int("Id da tarefa: ")
        resultado = View.Comentario_Listar_Por_Tarefa(tarefa_id)
        if not resultado:
            print(C.info("Nenhum comentario para essa tarefa."))
            return
        for c in resultado:
            print(C.item(
                f"[{c.get_id()}] {c.get_texto()}  (autor_id={c.get_autor_id()})"
            ))

    @staticmethod
    def Comentario_Inserir():
        try:
            print(C.secao("Tarefas disponiveis"))
            UI.Tarefa_Listar()
            tarefa_id = UI.Ler_Int("Id da tarefa: ", 0)
            texto = input(C.prompt("Comentario: "))
            c = View.Comentario_Inserir(texto, tarefa_id, UI.usuario_logado.get_id())
            print(C.sucesso(f"Comentario inserido (id={c.get_id()})."))
        except Exception as e:
            print(C.erro(f"Erro ao inserir comentario: {e}"))

    @staticmethod
    def Comentario_Excluir():
        try:
            id_ = UI.Ler_Int("Id do comentario para excluir: ")
            if View.Comentario_Excluir(id_):
                print(C.sucesso("Comentario excluido."))
            else:
                print(C.erro("Comentario nao encontrado."))
        except Exception as e:
            print(C.erro(f"Erro ao excluir comentario: {e}"))

    # ==================================================================
    # EVENTO  (ADMIN e MEMBRO)
    # ==================================================================
    @staticmethod
    def Menu_Evento():
        while True:
            print(C.menu_titulo("MENU EVENTO (CALENDARIO)"))
            print(C.opcoes((1, "Listar meus eventos"), (2, "Inserir"), (3, "Atualizar")))
            print(C.opcoes((4, "Excluir"), (5, "Pesquisar por titulo")))
            print(C.opcao_sair("Voltar"))
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
                print(C.erro("Opcao invalida."))

    @staticmethod
    def Evento_Meus():
        resultado = View.Evento_Listar_Por_Usuario(UI.usuario_logado.get_id())
        if not resultado:
            print(C.info("Voce nao tem eventos."))
            return
        for e in resultado:
            print(C.item(f"{e}  {e.get_data_inicio()} -> {e.get_data_fim()}"))

    @staticmethod
    def Evento_Inserir():
        try:
            titulo = input(C.prompt("Titulo: "))
            descricao = input(C.prompt("Descricao: "))
            data_inicio = input(C.prompt("Inicio (AAAA-MM-DDTHH:MM): "))
            data_fim = input(C.prompt("Fim (AAAA-MM-DDTHH:MM): "))
            tarefa_id = UI.Ler_Int("Id da tarefa vinculada (0 = nenhuma): ", 0)
            e = View.Evento_Inserir(titulo, descricao, data_inicio, data_fim,
                                    UI.usuario_logado.get_id(), tarefa_id)
            print(C.sucesso(f"Evento inserido (id={e.get_id()})."))
        except Exception as ex:
            print(C.erro(f"Erro ao inserir evento: {ex}"))

    @staticmethod
    def Evento_Atualizar():
        try:
            id_ = UI.Ler_Int("Id do evento para atualizar: ")
            ev = View.Evento_Listar_Id(id_)
            if ev is None:
                print(C.erro("Evento nao encontrado."))
                return
            titulo = input(C.prompt(f"Titulo [{ev.get_titulo()}]: ")).strip() or ev.get_titulo()
            inicio = input(C.prompt(f"Inicio [{ev.get_data_inicio()}]: ")).strip() or ev.get_data_inicio()
            fim = input(C.prompt(f"Fim [{ev.get_data_fim()}]: ")).strip() or ev.get_data_fim()
            if View.Evento_Atualizar(id_, titulo, inicio, fim):
                print(C.sucesso("Evento atualizado."))
            else:
                print(C.erro("Falhou."))
        except Exception as ex:
            print(C.erro(f"Erro ao atualizar evento: {ex}"))

    @staticmethod
    def Evento_Excluir():
        try:
            id_ = UI.Ler_Int("Id do evento para excluir: ")
            if View.Evento_Excluir(id_):
                print(C.sucesso("Evento excluido."))
            else:
                print(C.erro("Evento nao encontrado."))
        except Exception as ex:
            print(C.erro(f"Erro ao excluir evento: {ex}"))

    @staticmethod
    def Evento_Pesquisar():
        resultado = View.Evento_Pesquisar_Titulo(input(C.prompt("Parte do titulo: ")))
        if not resultado:
            print(C.info("Nada encontrado."))
            return
        UI._listar(resultado)


if __name__ == "__main__":
    UI.Main()