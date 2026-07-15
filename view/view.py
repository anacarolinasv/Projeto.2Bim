"""Camada de Operacoes (View/Service) do TaskFlow.

Fica entre a interface (ui.py) e os DAOs. Recebe dados simples da UI,
monta os objetos do modelo, aplica as regras de negocio e chama os DAOs.
A UI nao acessa DAO nem modelo diretamente — so chama metodos da View.
"""

from usuarios.usuario import Usuario, UsuarioDAO, Perfil
from equipes.equipe import Equipe, EquipeDAO
from projetos.projeto import Projeto, ProjetoDAO, StatusProjeto
from sprints.sprint import Sprint, SprintDAO
from categorias.categoria import Categoria, CategoriaDAO
from tarefas.tarefa import Tarefa, TarefaDAO, StatusTarefa, Prioridade
from comentarios.comentario import Comentario, ComentarioDAO
from eventos.evento import Evento, EventoDAO


class View:
    # ==================================================================
    # AUTENTICACAO
    # ==================================================================
    @staticmethod
    def Garantir_Admin_Inicial():
        """Cria um admin padrao se nao houver usuarios. Retorna True se criou."""
        if not UsuarioDAO.Listar():
            admin = Usuario(nome="Administrador", email="admin@taskflow.com",
                            senha="admin", perfil=Perfil.ADMIN)
            UsuarioDAO.Inserir(admin)
            return True
        return False

    @staticmethod
    def Usuario_Login(email, senha):
        """Retorna o Usuario se e-mail e senha conferirem, senao None."""
        usuario = UsuarioDAO.Buscar_Por_Email(email)
        if usuario and usuario.get_senha() == senha:
            return usuario
        return None

    # ==================================================================
    # USUARIO
    # ==================================================================
    @staticmethod
    def Usuario_Listar():
        return UsuarioDAO.Listar()

    @staticmethod
    def Usuario_Listar_Id(id):
        return UsuarioDAO.Listar_Id(id)

    @staticmethod
    def Usuario_Inserir(nome, email, senha, perfil):
        if UsuarioDAO.Buscar_Por_Email(email):
            raise ValueError("Ja existe uma conta com esse e-mail.")
        u = Usuario(perfil=perfil)
        u.set_nome(nome)
        u.set_email(email)
        u.set_senha(senha)
        return UsuarioDAO.Inserir(u)

    @staticmethod
    def Usuario_Atualizar(id, nome, email, perfil):
        u = UsuarioDAO.Listar_Id(id)
        if u is None:
            return False
        u.set_nome(nome)
        u.set_email(email)
        u.set_perfil(perfil)
        return UsuarioDAO.Atualizar(u)

    @staticmethod
    def Usuario_Excluir(id):
        return UsuarioDAO.Excluir(id)

    @staticmethod
    def Usuario_Pesquisar_Nome(termo):
        return UsuarioDAO.Pesquisar_Por_Nome(termo)

    # ==================================================================
    # EQUIPE
    # ==================================================================
    @staticmethod
    def Equipe_Listar():
        return EquipeDAO.Listar()

    @staticmethod
    def Equipe_Listar_Id(id):
        return EquipeDAO.Listar_Id(id)

    @staticmethod
    def Equipe_Inserir(nome, descricao, lider_id):
        e = Equipe(descricao=descricao, lider_id=lider_id)
        e.set_nome(nome)
        return EquipeDAO.Inserir(e)

    @staticmethod
    def Equipe_Atualizar(id, nome, descricao, lider_id):
        e = EquipeDAO.Listar_Id(id)
        if e is None:
            return False
        e.set_nome(nome)
        e.set_descricao(descricao)
        e.set_lider_id(lider_id)
        return EquipeDAO.Atualizar(e)

    @staticmethod
    def Equipe_Excluir(id):
        return EquipeDAO.Excluir(id)

    @staticmethod
    def Equipe_Pesquisar_Nome(termo):
        return EquipeDAO.Pesquisar_Por_Nome(termo)

    @staticmethod
    def Equipe_Membros(equipe_id):
        """Usuarios que sao membros da equipe."""
        return UsuarioDAO.Listar_Por_Equipe(equipe_id)

    @staticmethod
    def Equipe_Adicionar_Membro(equipe_id, usuario_id):
        """Adiciona um usuario como membro da equipe (define seu equipe_id)."""
        u = UsuarioDAO.Listar_Id(usuario_id)
        if u is None:
            return False
        u.set_equipe_id(equipe_id)
        return UsuarioDAO.Atualizar(u)

    @staticmethod
    def Equipe_Remover_Membro(usuario_id):
        """Remove o usuario da sua equipe atual (equipe_id = 0)."""
        u = UsuarioDAO.Listar_Id(usuario_id)
        if u is None:
            return False
        u.set_equipe_id(0)
        return UsuarioDAO.Atualizar(u)

    # ==================================================================
    # PROJETO
    # ==================================================================
    @staticmethod
    def Projeto_Listar():
        return ProjetoDAO.Listar()

    @staticmethod
    def Projeto_Listar_Id(id):
        return ProjetoDAO.Listar_Id(id)

    @staticmethod
    def Projeto_Inserir(nome, descricao, data_inicio, data_fim, status, equipe_id):
        p = Projeto(descricao=descricao, data_inicio=data_inicio,
                    data_fim=data_fim, status=status, equipe_id=equipe_id)
        p.set_nome(nome)
        return ProjetoDAO.Inserir(p)

    @staticmethod
    def Projeto_Atualizar(id, nome, descricao, status, equipe_id):
        p = ProjetoDAO.Listar_Id(id)
        if p is None:
            return False
        p.set_nome(nome)
        p.set_descricao(descricao)
        p.set_status(status)
        p.set_equipe_id(equipe_id)
        return ProjetoDAO.Atualizar(p)

    @staticmethod
    def Projeto_Excluir(id):
        return ProjetoDAO.Excluir(id)

    @staticmethod
    def Projeto_Pesquisar_Nome(termo):
        return ProjetoDAO.Pesquisar_Por_Nome(termo)

    @staticmethod
    def Projeto_Listar_Por_Equipe(equipe_id):
        return ProjetoDAO.Listar_Por_Equipe(equipe_id)

    @staticmethod
    def Projeto_Membros(projeto_id):
        """Membros do projeto = membros da equipe dona do projeto."""
        p = ProjetoDAO.Listar_Id(projeto_id)
        if p is None:
            return []
        return UsuarioDAO.Listar_Por_Equipe(p.get_equipe_id())

    @staticmethod
    def Projeto_Progresso(projeto_id):
        """Retorna (feitas, total) das tarefas do projeto (via suas sprints)."""
        tarefas = View.Tarefa_Listar_Por_Projeto(projeto_id)
        total = len(tarefas)
        feitas = sum(1 for t in tarefas if t.get_status() == StatusTarefa.CONCLUIDA)
        return feitas, total

    # ==================================================================
    # SPRINT
    # ==================================================================
    @staticmethod
    def Sprint_Listar():
        return SprintDAO.Listar()

    @staticmethod
    def Sprint_Listar_Id(id):
        return SprintDAO.Listar_Id(id)

    @staticmethod
    def Sprint_Listar_Por_Projeto(projeto_id):
        return SprintDAO.Listar_Por_Projeto(projeto_id)

    @staticmethod
    def Sprint_Inserir(nome, objetivo, data_inicio, data_fim, projeto_id):
        s = Sprint(objetivo=objetivo, data_inicio=data_inicio,
                   data_fim=data_fim, projeto_id=projeto_id)
        s.set_nome(nome)
        return SprintDAO.Inserir(s)

    @staticmethod
    def Sprint_Atualizar(id, nome, objetivo, data_inicio, data_fim):
        s = SprintDAO.Listar_Id(id)
        if s is None:
            return False
        s.set_nome(nome)
        s.set_objetivo(objetivo)
        s.set_data_inicio(data_inicio)
        s.set_data_fim(data_fim)
        return SprintDAO.Atualizar(s)

    @staticmethod
    def Sprint_Excluir(id):
        return SprintDAO.Excluir(id)

    # ==================================================================
    # CATEGORIA
    # ==================================================================
    @staticmethod
    def Categoria_Listar():
        return CategoriaDAO.Listar()

    @staticmethod
    def Categoria_Listar_Id(id):
        return CategoriaDAO.Listar_Id(id)

    @staticmethod
    def Categoria_Inserir(nome, cor):
        c = Categoria(cor=cor)
        c.set_nome(nome)
        return CategoriaDAO.Inserir(c)

    @staticmethod
    def Categoria_Atualizar(id, nome, cor):
        c = CategoriaDAO.Listar_Id(id)
        if c is None:
            return False
        c.set_nome(nome)
        c.set_cor(cor)
        return CategoriaDAO.Atualizar(c)

    @staticmethod
    def Categoria_Excluir(id):
        return CategoriaDAO.Excluir(id)

    @staticmethod
    def Categoria_Pesquisar_Nome(termo):
        return CategoriaDAO.Pesquisar_Por_Nome(termo)

    # ==================================================================
    # TAREFA
    # ==================================================================
    @staticmethod
    def Tarefa_Listar():
        return TarefaDAO.Listar()

    @staticmethod
    def Tarefa_Listar_Id(id):
        return TarefaDAO.Listar_Id(id)

    @staticmethod
    def Tarefa_Inserir(titulo, descricao, status, prioridade, prazo,
                       sprint_id, responsavel_id, categoria_id):
        t = Tarefa(descricao=descricao, status=status, prioridade=prioridade,
                   prazo=prazo, sprint_id=sprint_id,
                   responsavel_id=responsavel_id, categoria_id=categoria_id)
        t.set_titulo(titulo)
        return TarefaDAO.Inserir(t)

    @staticmethod
    def Tarefa_Atualizar(id, titulo, descricao, status, prioridade, categoria_id):
        t = TarefaDAO.Listar_Id(id)
        if t is None:
            return False
        t.set_titulo(titulo)
        t.set_descricao(descricao)
        t.set_status(status)
        t.set_prioridade(prioridade)
        t.set_categoria_id(categoria_id)
        return TarefaDAO.Atualizar(t)

    @staticmethod
    def Tarefa_Excluir(id):
        return TarefaDAO.Excluir(id)

    @staticmethod
    def Tarefa_Pesquisar_Titulo(termo):
        return TarefaDAO.Pesquisar_Por_Titulo(termo)

    @staticmethod
    def Tarefa_Listar_Por_Sprint(sprint_id):
        return TarefaDAO.Listar_Por_Sprint(sprint_id)

    @staticmethod
    def Tarefa_Listar_Por_Projeto(projeto_id):
        """Todas as tarefas do projeto, percorrendo as sprints dele."""
        tarefas = []
        for s in SprintDAO.Listar_Por_Projeto(projeto_id):
            tarefas.extend(TarefaDAO.Listar_Por_Sprint(s.get_id()))
        return tarefas

    @staticmethod
    def Tarefa_Concluir(tarefa_id):
        """Regra de negocio (mexe em Tarefa E Projeto): conclui a tarefa e,
        se todas as tarefas do projeto ficarem concluidas, marca o projeto
        como CONCLUIDO.

        Retorna (tarefa, projeto_concluido) — projeto_concluido e o Projeto
        se ele acabou de ser concluido, ou None caso contrario.
        Retorna None se a tarefa nao existir.
        """
        tarefa = TarefaDAO.Listar_Id(tarefa_id)
        if tarefa is None:
            return None
        tarefa.concluir()
        TarefaDAO.Atualizar(tarefa)

        # Sprint -> Projeto: se todas as tarefas do projeto (em todas as
        # sprints) estiverem concluidas, o projeto vira CONCLUIDO.
        projeto_concluido = None
        sprint = SprintDAO.Listar_Id(tarefa.get_sprint_id())
        if sprint:
            projeto_id = sprint.get_projeto_id()
            tarefas = View.Tarefa_Listar_Por_Projeto(projeto_id)
            if tarefas and all(t.get_status() == StatusTarefa.CONCLUIDA for t in tarefas):
                projeto = ProjetoDAO.Listar_Id(projeto_id)
                if projeto:
                    projeto.set_status(StatusProjeto.CONCLUIDO)
                    ProjetoDAO.Atualizar(projeto)
                    projeto_concluido = projeto
        return tarefa, projeto_concluido

    # ==================================================================
    # COMENTARIO
    # ==================================================================
    @staticmethod
    def Comentario_Listar_Por_Tarefa(tarefa_id):
        return ComentarioDAO.Listar_Por_Tarefa(tarefa_id)

    @staticmethod
    def Comentario_Listar_Id(id):
        return ComentarioDAO.Listar_Id(id)

    @staticmethod
    def Comentario_Inserir(texto, tarefa_id, autor_id):
        c = Comentario(tarefa_id=tarefa_id, autor_id=autor_id)
        c.set_texto(texto)
        return ComentarioDAO.Inserir(c)

    @staticmethod
    def Comentario_Atualizar(id, texto):
        c = ComentarioDAO.Listar_Id(id)
        if c is None:
            return False
        c.set_texto(texto)
        return ComentarioDAO.Atualizar(c)

    @staticmethod
    def Comentario_Excluir(id):
        return ComentarioDAO.Excluir(id)

    # ==================================================================
    # EVENTO
    # ==================================================================
    @staticmethod
    def Evento_Listar_Id(id):
        return EventoDAO.Listar_Id(id)

    @staticmethod
    def Evento_Listar_Por_Usuario(usuario_id):
        return EventoDAO.Listar_Por_Usuario(usuario_id)

    @staticmethod
    def Evento_Inserir(titulo, descricao, data_inicio, data_fim, usuario_id, tarefa_id):
        e = Evento(descricao=descricao, data_inicio=data_inicio, data_fim=data_fim,
                   usuario_id=usuario_id, tarefa_id=tarefa_id)
        e.set_titulo(titulo)
        return EventoDAO.Inserir(e)

    @staticmethod
    def Evento_Atualizar(id, titulo, data_inicio, data_fim):
        e = EventoDAO.Listar_Id(id)
        if e is None:
            return False
        e.set_titulo(titulo)
        e.set_data_inicio(data_inicio)
        e.set_data_fim(data_fim)
        return EventoDAO.Atualizar(e)

    @staticmethod
    def Evento_Excluir(id):
        return EventoDAO.Excluir(id)

    @staticmethod
    def Evento_Pesquisar_Titulo(termo):
        return EventoDAO.Pesquisar_Por_Titulo(termo)
