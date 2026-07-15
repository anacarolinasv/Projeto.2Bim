"""
Como executar (a partir da raiz do projeto):
    python3 -m streamlit run streamlit_app.py

Login inicial (criado automaticamente): admin@taskflow.com / admin
"""

from datetime import date

import streamlit as st

from view.view import View
from usuarios.usuario import Perfil
from projetos.projeto import StatusProjeto
from tarefas.tarefa import StatusTarefa, Prioridade

st.set_page_config(page_title="TaskFlow", page_icon="🟣", layout="wide")

# ----------------------------------------------------------------------
# Paleta / cores
# ----------------------------------------------------------------------
ROXO = "#7C3AED"
ROXO_ESCURO = "#5B21B6"
STATUS_COR = {"A_FAZER": "#94A3B8", "EM_ANDAMENTO": "#F59E0B", "CONCLUIDA": "#22C55E"}
STATUS_ROTULO = {"A_FAZER": "A fazer", "EM_ANDAMENTO": "Em andamento", "CONCLUIDA": "Concluída"}
PRIOR_COR = {"BAIXA": "#64748B", "MEDIA": "#6366F1", "ALTA": "#EF4444"}
PROJ_COR = {"ATIVO": "#7C3AED", "CONCLUIDO": "#22C55E", "ARQUIVADO": "#94A3B8"}


def logo_icon(size=40, claro=False):
    """Ícone da marca (SVG inline). claro=True usa borda/glow para fundo escuro."""
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex:0 0 auto">
      <defs><linearGradient id="tf{size}{int(claro)}" x1="8" y1="8" x2="52" y2="52" gradientUnits="userSpaceOnUse">
        <stop stop-color="#A78BFA"/><stop offset="1" stop-color="#6D28D9"/></linearGradient></defs>
      <rect x="8" y="8" width="44" height="44" rx="13" fill="{'#fff' if claro else 'url(#tf' + str(size) + str(int(claro)) + ')'}"/>
      <path d="M32 20 h9 M26 30 h15 M20 40 h21" stroke="{'#7C3AED' if claro else '#fff'}" stroke-opacity="0.35" stroke-width="3" stroke-linecap="round"/>
      <path d="M19 31 l6.5 6.5 L39 22" stroke="{'#7C3AED' if claro else '#fff'}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    </svg>'''


def css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    .stApp {{ background: #FAFAFC; }}
    header[data-testid="stHeader"] {{ background: transparent; }}

    /* Sidebar roxo com gradiente */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {ROXO} 0%, {ROXO_ESCURO} 100%);
    }}
    section[data-testid="stSidebar"] * {{ color: #F5F3FF !important; }}
    section[data-testid="stSidebar"] .stRadio label {{
        padding: 8px 12px; border-radius: 10px; font-weight: 600; font-size: 0.95rem;
    }}
    section[data-testid="stSidebar"] .stRadio label:hover {{ background: rgba(255,255,255,0.12); }}

    /* Botoes: primario roxo, secundario branco (estilo Asana) */
    .stButton>button[kind="primary"], .stFormSubmitButton>button {{
        background: {ROXO}; color: #fff; border: none; border-radius: 10px;
        font-weight: 600; padding: 0.45rem 1rem; transition: all .15s;
    }}
    .stButton>button[kind="primary"]:hover, .stFormSubmitButton>button:hover {{
        background: {ROXO_ESCURO}; color: #fff;
    }}
    .stButton>button[kind="secondary"] {{
        background: #fff; color: #374151; border: 1px solid #E5E7EB; border-radius: 10px;
        font-weight: 600; padding: 0.35rem 0.7rem; transition: all .15s;
    }}
    .stButton>button[kind="secondary"]:hover {{ border-color: {ROXO}; color: {ROXO}; }}
    /* projeto/sprint (secundario) = link alinhado a esquerda */
    section[data-testid="stSidebar"] .stButton>button[kind="secondary"] {{
        background: transparent !important; color: #F5F3FF !important; border: none !important;
        justify-content: flex-start !important; text-align: left !important;
        padding: .28rem .5rem !important; font-weight: 600 !important;
    }}
    section[data-testid="stSidebar"] .stButton>button[kind="secondary"]:hover {{
        background: rgba(255,255,255,0.16) !important; }}
    section[data-testid="stSidebar"] .stButton>button[kind="secondary"] p {{ text-align: left !important; width: 100%; }}
    /* logout (primario) = botao translucido centralizado */
    section[data-testid="stSidebar"] .stButton>button[kind="primary"] {{
        background: rgba(255,255,255,0.15) !important; color: #fff !important;
        border: 1px solid rgba(255,255,255,0.3) !important; justify-content: center !important;
    }}
    section[data-testid="stSidebar"] .stButton>button[kind="primary"]:hover {{
        background: rgba(255,255,255,0.28) !important; }}

    /* Cabecalho de pagina */
    .page-title {{ font-size: 1.9rem; font-weight: 800; color: #1E1B2E; margin: 0; }}
    .page-sub {{ color: #6B7280; font-size: 0.95rem; margin-top: -2px; margin-bottom: 1rem; }}

    /* KPI cards */
    .kpi {{ background: #fff; border-radius: 16px; padding: 18px 20px;
            box-shadow: 0 1px 3px rgba(16,24,40,.08); border: 1px solid #EEE9FB; }}
    .kpi .v {{ font-size: 1.9rem; font-weight: 800; line-height: 1; }}
    .kpi .l {{ color: #6B7280; font-size: .82rem; font-weight: 600; margin-top: 6px;
               text-transform: uppercase; letter-spacing: .3px; }}

    /* Badges */
    .badge {{ display:inline-block; padding: 2px 10px; border-radius: 999px;
              font-size: .72rem; font-weight: 700; color:#fff; }}

    /* Kanban */
    .kanban-col-head {{ font-weight: 700; font-size: .95rem; padding: 6px 4px 10px;
                        border-bottom: 3px solid; margin-bottom: 8px; }}
    .task-title {{ font-weight: 700; color:#1E1B2E; font-size: .95rem; margin-bottom: 6px; }}
    .task-meta {{ color:#6B7280; font-size: .78rem; margin-top: 6px; }}

    /* Cartao de projeto */
    .proj-card {{ background:#fff; border-radius:14px; padding:16px 18px; border:1px solid #EEE9FB;
                  box-shadow: 0 1px 3px rgba(16,24,40,.06); margin-bottom: 12px; }}
    .proj-name {{ font-weight:700; color:#1E1B2E; font-size:1.05rem; }}

    /* Menos espaco no topo do conteudo */
    .block-container {{ padding-top: 2.2rem; }}

    /* Marca e card de usuario na sidebar */
    .brand {{ display:flex; align-items:center; gap:10px; font-size:1.35rem; font-weight:800;
              color:#fff; margin-bottom:14px; }}
    .user-card {{ display:flex; align-items:center; gap:10px; background:rgba(255,255,255,0.12);
                  border:1px solid rgba(255,255,255,0.18); border-radius:12px; padding:10px 12px;
                  margin-bottom:14px; }}
    .user-card .av {{ width:34px;height:34px;border-radius:50%;background:#fff;color:{ROXO_ESCURO};
                      display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.8rem; }}
    .side-label {{ opacity:.65; font-size:.7rem; font-weight:800; letter-spacing:.6px;
                   margin:16px 0 4px; }}

    /* Navegacao: item ativo destacado */
    section[data-testid="stSidebar"] .stRadio label:has(input:checked) {{
        background: rgba(255,255,255,0.22); }}

    /* Cabecalho de pagina com barra inferior sutil */
    .page-title {{ letter-spacing:-.3px; }}
    </style>
    """, unsafe_allow_html=True)


def badge(texto, cor):
    return f'<span class="badge" style="background:{cor}">{texto}</span>'


# --- helpers visuais estilo ClickUp ---
_AVATAR_CORES = ["#7C3AED", "#EC4899", "#0EA5E9", "#F59E0B", "#10B981", "#EF4444", "#6366F1"]


def avatar(nome):
    if not nome or nome == "—":
        return '<span style="color:#CBD5E1;font-size:1.1rem">◌</span>'
    partes = nome.split()
    ini = (partes[0][0] + (partes[1][0] if len(partes) > 1 else "")).upper()
    cor = _AVATAR_CORES[sum(map(ord, nome)) % len(_AVATAR_CORES)]
    return (f'<span style="display:inline-flex;align-items:center;justify-content:center;'
            f'width:26px;height:26px;border-radius:50%;background:{cor};color:#fff;'
            f'font-size:.7rem;font-weight:700">{ini}</span>')


def prazo_html(prazo):
    if not prazo:
        return '<span style="color:#CBD5E1">—</span>'
    cor = "#374151"
    try:
        if date.fromisoformat(prazo[:10]) < date.today():
            cor = "#EF4444"
    except ValueError:
        pass
    return f'<span style="color:{cor};font-size:.85rem">{prazo}</span>'


_FLAG = {"ALTA": ("#EF4444", "High"), "MEDIA": ("#3B82F6", "Normal"), "BAIXA": ("#94A3B8", "Low")}


def flag_html(prioridade):
    cor, rotulo = _FLAG[prioridade]
    return f'<span style="color:{cor};font-size:.85rem">⚑ {rotulo}</span>'


_STATUS_ICONE = {"A_FAZER": "○", "EM_ANDAMENTO": "◑", "CONCLUIDA": "✓"}


def status_pill(status_valor, quantidade):
    cor = STATUS_COR[status_valor]
    rotulo = STATUS_ROTULO[status_valor].upper()
    return (f'<span style="display:inline-block;background:{cor};color:#fff;padding:3px 12px;'
            f'border-radius:6px;font-size:.72rem;font-weight:800;letter-spacing:.4px">'
            f'{_STATUS_ICONE[status_valor]} {rotulo}</span>'
            f'<span style="color:#9CA3AF;font-weight:700;margin-left:8px">{quantidade}</span>')


def cabecalho(titulo, subtitulo=""):
    st.markdown(f'<div class="page-title">{titulo}</div>', unsafe_allow_html=True)
    if subtitulo:
        st.markdown(f'<div class="page-sub">{subtitulo}</div>', unsafe_allow_html=True)


# --- estado inicial ---
if "seeded" not in st.session_state:
    View.Garantir_Admin_Inicial()
    if not View.Categoria_Listar():
        for nome, cor in [("Bug", "#EF4444"), ("Feature", "#7C3AED"),
                          ("Melhoria", "#22C55E"), ("Documentação", "#F59E0B")]:
            View.Categoria_Inserir(nome, cor)
    st.session_state.seeded = True
if "usuario" not in st.session_state:
    st.session_state.usuario = None


# ----------------------------------------------------------------------
# Helpers de selecao/associacao
# ----------------------------------------------------------------------
def rotulo_id(obj, campo="get_nome"):
    return f"{obj.get_id()} - {getattr(obj, campo)()}"


def selecionar(rotulo, objetos, campo="get_nome", key=None):
    if not objetos:
        st.info("Nenhum registro cadastrado ainda.")
        return None
    return st.selectbox(rotulo, objetos, format_func=lambda o: rotulo_id(o, campo), key=key)


def opcao_id(rotulo, objetos, campo="get_nome", key=None, permitir_zero=False):
    opcoes = list(objetos)
    if permitir_zero:
        escolha = st.selectbox(rotulo, [None] + opcoes,
                               format_func=lambda o: "— (nenhum)" if o is None else rotulo_id(o, campo),
                               key=key)
        return 0 if escolha is None else escolha.get_id()
    if not opcoes:
        st.warning(f"Cadastre antes um item para '{rotulo}'.")
        return 0
    escolha = st.selectbox(rotulo, opcoes, format_func=lambda o: rotulo_id(o, campo), key=key)
    return escolha.get_id()


def mapa_nomes(objetos, campo="get_nome"):
    return {o.get_id(): getattr(o, campo)() for o in objetos}


# ----------------------------------------------------------------------
# Login / Criar conta
# ----------------------------------------------------------------------
def tela_acesso():
    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.markdown(
            f'<div style="text-align:center;margin-top:7vh">'
            f'<div style="display:flex;justify-content:center;margin-bottom:10px">{logo_icon(64)}</div>'
            f'<div style="font-size:2.4rem;font-weight:800;color:#1E1B2E">Task<span style="color:{ROXO}">Flow</span></div>'
            f'<div style="color:#6B7280;margin-bottom:1.5rem">Gerenciador de Tarefas e Calendário</div>'
            f'</div>', unsafe_allow_html=True)
        aba_entrar, aba_conta = st.tabs(["  Entrar  ", "  Criar conta  "])
        with aba_entrar:
            with st.form("form_login"):
                email = st.text_input("E-mail", value="admin@taskflow.com")
                senha = st.text_input("Senha", type="password")
                if st.form_submit_button("Entrar", type="primary", use_container_width=True):
                    usuario = View.Usuario_Login(email, senha)
                    if usuario:
                        st.session_state.usuario = usuario
                        st.rerun()
                    else:
                        st.error("E-mail ou senha invalidos.")
        with aba_conta:
            with st.form("form_conta"):
                nome = st.text_input("Nome")
                email = st.text_input("E-mail")
                senha = st.text_input("Senha (min. 4 caracteres)", type="password")
                perfil = st.selectbox("Perfil", list(Perfil), format_func=lambda p: p.value)
                if st.form_submit_button("Criar conta", use_container_width=True):
                    try:
                        novo = View.Usuario_Inserir(nome, email, senha, perfil)
                        st.success(f"Conta criada (id={novo.get_id()})! Agora e so entrar.")
                    except Exception as e:
                        st.error(str(e))


# ----------------------------------------------------------------------
# Dashboard
# ----------------------------------------------------------------------
def pagina_dashboard():
    u = st.session_state.usuario
    cabecalho(f"Olá, {u.get_nome().split()[0]} 👋", "Visão geral do seu trabalho")

    tarefas = View.Tarefa_Listar()
    projetos = View.Projeto_Listar()
    n_af = sum(1 for t in tarefas if t.get_status() == StatusTarefa.A_FAZER)
    n_em = sum(1 for t in tarefas if t.get_status() == StatusTarefa.EM_ANDAMENTO)
    n_ok = sum(1 for t in tarefas if t.get_status() == StatusTarefa.CONCLUIDA)

    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        (c1, "Projetos", len(projetos), ROXO),
        (c2, "A fazer", n_af, STATUS_COR["A_FAZER"]),
        (c3, "Em andamento", n_em, STATUS_COR["EM_ANDAMENTO"]),
        (c4, "Concluídas", n_ok, STATUS_COR["CONCLUIDA"]),
    ]
    for col, label, valor, cor in kpis:
        col.markdown(f'<div class="kpi"><div class="v" style="color:{cor}">{valor}</div>'
                     f'<div class="l">{label}</div></div>', unsafe_allow_html=True)

    st.write("")
    esq, dir = st.columns([1.4, 1])
    with esq:
        st.markdown("##### 📋 Minhas tarefas")
        minhas = [t for t in tarefas if t.get_responsavel_id() == u.get_id()]
        if not minhas:
            st.caption("Você não tem tarefas atribuídas.")
        for t in minhas[:8]:
            s = t.get_status().value
            st.markdown(
                f'<div class="proj-card" style="padding:12px 16px;margin-bottom:8px">'
                f'<span class="task-title">{t.get_titulo()}</span> '
                f'{badge(STATUS_ROTULO[s], STATUS_COR[s])} '
                f'{badge(t.get_prioridade().value, PRIOR_COR[t.get_prioridade().value])}'
                f'</div>', unsafe_allow_html=True)
    with dir:
        st.markdown("##### 🎯 Andamento dos projetos")
        if not projetos:
            st.caption("Nenhum projeto cadastrado.")
        for p in projetos[:6]:
            tks = View.Tarefa_Listar_Por_Projeto(p.get_id())
            total = len(tks)
            feitas = sum(1 for t in tks if t.get_status() == StatusTarefa.CONCLUIDA)
            pct = feitas / total if total else 0
            st.markdown(f"**{p.get_nome()}**  ·  {feitas}/{total}")
            st.progress(pct)


# ----------------------------------------------------------------------
# Tarefas — quadro Kanban
# ----------------------------------------------------------------------
def _form_nova_tarefa():
    """Nova tarefa: escolhe Projeto -> Sprint, responsavel entre os membros."""
    projetos = View.Projeto_Listar()
    with st.expander("➕ Nova tarefa"):
        if not projetos:
            st.info("Crie um projeto e uma sprint na aba **Projetos** primeiro.")
            return
        cp, cs = st.columns(2)
        projeto = cp.selectbox("Projeto", projetos, format_func=lambda p: p.get_nome(), key="nt_proj")
        sprints = View.Sprint_Listar_Por_Projeto(projeto.get_id())
        if not sprints:
            cs.selectbox("Sprint", ["(nenhuma)"], disabled=True, key="nt_sp0")
            st.warning("Este projeto não tem sprint. Crie uma na aba **Projetos**.")
            return
        sprint = cs.selectbox("Sprint", sprints, format_func=lambda s: s.get_nome(), key="nt_sprint")

        titulo = st.text_input("Título", key="nt_titulo")
        descricao = st.text_input("Descrição", key="nt_desc")
        c1, c2, c3 = st.columns(3)
        status = c1.selectbox("Status", list(StatusTarefa), format_func=lambda s: STATUS_ROTULO[s.value], key="nt_status")
        prioridade = c2.selectbox("Prioridade", list(Prioridade), format_func=lambda p: p.value, key="nt_prior")
        prazo = c3.text_input("Prazo (AAAA-MM-DD)", key="nt_prazo")

        cr, cc = st.columns(2)
        membros = View.Projeto_Membros(projeto.get_id())
        if membros:
            resp = cr.selectbox("Responsável", membros, format_func=lambda u: u.get_nome(), key="nt_resp")
        else:
            resp = None
            cr.caption("Sem membros — adicione na aba Projetos.")
        cats = View.Categoria_Listar()
        categoria = cc.selectbox("Categoria", cats, format_func=lambda c: c.get_nome(), key="nt_cat") if cats else None

        if st.button("Criar tarefa", key="nt_btn", type="primary"):
            try:
                View.Tarefa_Inserir(titulo, descricao, status, prioridade, prazo,
                                    sprint.get_id(), resp.get_id() if resp else 0,
                                    categoria.get_id() if categoria else 0)
                st.success("Tarefa criada."); st.rerun()
            except Exception as e:
                st.error(str(e))


def render_lista(tarefas, usuarios, sprint_ctx=None):
    """Visão de lista agrupada por status (estilo Asana): círculo de concluir,
    texto riscado quando concluída e '+ Adicionar tarefa' inline por seção."""
    RATIOS = [0.5, 4.5, 1.1, 1.5, 1.4]
    for status in [StatusTarefa.EM_ANDAMENTO, StatusTarefa.A_FAZER, StatusTarefa.CONCLUIDA]:
        itens = [t for t in tarefas if t.get_status() == status]
        st.markdown(status_pill(status.value, len(itens)), unsafe_allow_html=True)

        h = st.columns(RATIOS)
        for col, nome in zip(h[1:], ["Tarefa", "Resp.", "Prazo", "Prioridade"]):
            col.markdown(f'<span style="color:#9CA3AF;font-size:.72rem;font-weight:700;'
                         f'text-transform:uppercase;letter-spacing:.4px">{nome}</span>',
                         unsafe_allow_html=True)

        done = status == StatusTarefa.CONCLUIDA
        for t in itens:
            r = st.columns(RATIOS)
            # circulo de concluir / reabrir
            if r[0].button("✅" if done else "◯", key=f"chk{t.get_id()}",
                           help="Reabrir" if done else "Concluir"):
                if done:
                    View.Tarefa_Atualizar(t.get_id(), t.get_titulo(), t.get_descricao(),
                                          StatusTarefa.A_FAZER, t.get_prioridade(), t.get_categoria_id())
                else:
                    _, proj = View.Tarefa_Concluir(t.get_id())
                    if proj:
                        st.toast(f"🎉 Projeto '{proj.get_nome()}' concluído!")
                st.rerun()
            nome_estilo = ("text-decoration:line-through;color:#9CA3AF" if done
                           else "color:#1E1B2E")
            r[1].markdown(f'<div style="padding:6px 0"><b style="{nome_estilo}">{t.get_titulo()}</b></div>',
                          unsafe_allow_html=True)
            resp = usuarios.get(t.get_responsavel_id(), "—")
            r[2].markdown(f'<div style="padding:6px 0">{avatar(resp)}</div>', unsafe_allow_html=True)
            r[3].markdown(f'<div style="padding:6px 0">{prazo_html(t.get_prazo())}</div>', unsafe_allow_html=True)
            r[4].markdown(f'<div style="padding:6px 0">{flag_html(t.get_prioridade().value)}</div>',
                          unsafe_allow_html=True)

        # "+ Adicionar tarefa" inline (so quando uma sprint esta selecionada)
        if sprint_ctx:
            with st.form(f"add_{status.value}_{sprint_ctx}", clear_on_submit=True):
                fc = st.columns([5.5, 1])
                novo = fc[0].text_input("nova", key=f"qa{status.value}{sprint_ctx}",
                                        label_visibility="collapsed",
                                        placeholder="+ Adicionar tarefa nesta seção...")
                if fc[1].form_submit_button("Adicionar") and novo.strip():
                    View.Tarefa_Inserir(novo, "", status, Prioridade.MEDIA, "",
                                        sprint_ctx, 0, 0)
                    st.rerun()
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)


def render_quadro(tarefas, usuarios):
    """Visão de quadro Kanban (3 colunas por status)."""
    colunas = st.columns(3)
    ordem = [StatusTarefa.A_FAZER, StatusTarefa.EM_ANDAMENTO, StatusTarefa.CONCLUIDA]
    for col, status in zip(colunas, ordem):
        s = status.value
        lista = [t for t in tarefas if t.get_status() == status]
        with col:
            st.markdown(f'<div class="kanban-col-head" style="border-color:{STATUS_COR[s]};color:{STATUS_COR[s]}">'
                        f'{STATUS_ROTULO[s]} · {len(lista)}</div>', unsafe_allow_html=True)
            for t in lista:
                with st.container(border=True):
                    resp = usuarios.get(t.get_responsavel_id(), "—")
                    st.markdown(
                        f'<div class="task-title">{t.get_titulo()}</div>'
                        f'{badge(t.get_prioridade().value, PRIOR_COR[t.get_prioridade().value])}'
                        f'<div class="task-meta">👤 {resp}'
                        + (f' · 📅 {t.get_prazo()}' if t.get_prazo() else '') + '</div>',
                        unsafe_allow_html=True)
                    b1, b2 = st.columns(2)
                    if status != StatusTarefa.CONCLUIDA:
                        if b1.button("✓ Concluir", key=f"cc{t.get_id()}", use_container_width=True):
                            _, proj = View.Tarefa_Concluir(t.get_id())
                            if proj:
                                st.toast(f"🎉 Projeto '{proj.get_nome()}' concluído!")
                            st.rerun()
                    if b2.button("🗑", key=f"dd{t.get_id()}", use_container_width=True):
                        View.Tarefa_Excluir(t.get_id()); st.rerun()


def pagina_tarefas():
    cabecalho("Tarefas", "Organize por sprint e acompanhe por status")
    usuarios = mapa_nomes(View.Usuario_Listar())
    projetos = View.Projeto_Listar()

    # barra de controle: filtro por sprint + alternador de visao
    proj_nome = {p.get_id(): p.get_nome() for p in projetos}
    sprints = View.Sprint_Listar()
    c1, c2 = st.columns([2, 1.2])
    opcoes = ["📋 Todas as tarefas"] + [
        f"{s.get_id()} · {proj_nome.get(s.get_projeto_id(), '?')} / {s.get_nome()}" for s in sprints]
    sel = c1.selectbox("Sprint", opcoes, label_visibility="collapsed", key="filtro_tarefas")
    modo = c2.radio("Visão", ["≣ Lista", "▦ Quadro"], horizontal=True, label_visibility="collapsed")

    tarefas = View.Tarefa_Listar()
    sprint_ctx = None
    if not sel.startswith("📋"):
        sprint_ctx = int(sel.split(" · ")[0])
        tarefas = [t for t in tarefas if t.get_sprint_id() == sprint_ctx]

    _form_nova_tarefa()

    if modo.startswith("≣"):
        render_lista(tarefas, usuarios, sprint_ctx)
    else:
        render_quadro(tarefas, usuarios)

    with st.expander("🔍 Pesquisar / editar tarefa"):
        termo = st.text_input("Parte do título", key="busca_tar")
        if termo:
            for t in View.Tarefa_Pesquisar_Titulo(termo):
                st.write("•", t.get_titulo(), f"({STATUS_ROTULO[t.get_status().value]})")
        t = selecionar("Editar tarefa", View.Tarefa_Listar(), campo="get_titulo", key="sel_tar")
        if t:
            with st.form("edit_tarefa"):
                titulo = st.text_input("Título", value=t.get_titulo())
                descricao = st.text_input("Descrição", value=t.get_descricao())
                status = st.selectbox("Status", list(StatusTarefa),
                                      index=list(StatusTarefa).index(t.get_status()),
                                      format_func=lambda s: STATUS_ROTULO[s.value])
                prioridade = st.selectbox("Prioridade", list(Prioridade),
                                          index=list(Prioridade).index(t.get_prioridade()),
                                          format_func=lambda p: p.value)
                categoria_id = st.number_input("Categoria id", value=t.get_categoria_id(), step=1)
                if st.form_submit_button("Salvar alterações"):
                    View.Tarefa_Atualizar(t.get_id(), titulo, descricao, status, prioridade, int(categoria_id))
                    st.success("Atualizado."); st.rerun()


# ----------------------------------------------------------------------
# Projetos — cartoes com progresso
# ----------------------------------------------------------------------
def _cartoes_projetos(equipes):
    projetos = View.Projeto_Listar()
    if not projetos:
        st.caption("Nenhum projeto ainda. Crie o primeiro acima.")
        return
    cols = st.columns(3)
    for i, p in enumerate(projetos):
        feitas, total = View.Projeto_Progresso(p.get_id())
        n_sprints = len(View.Sprint_Listar_Por_Projeto(p.get_id()))
        n_membros = len(View.Projeto_Membros(p.get_id()))
        pct = feitas / total if total else 0
        sp = p.get_status().value
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(
                    f'<div class="proj-name">{p.get_nome()}</div>'
                    f'{badge(sp.capitalize(), PROJ_COR[sp])}'
                    f'<div class="task-meta">👥 {equipes.get(p.get_equipe_id(), "—")} · '
                    f'🏃 {n_sprints} sprints · 👤 {n_membros} membros · {feitas}/{total} tarefas</div>',
                    unsafe_allow_html=True)
                st.progress(pct)


def _gerenciar_sprints(projeto):
    st.markdown("##### 🏃 Sprints do projeto")
    for s in View.Sprint_Listar_Por_Projeto(projeto.get_id()):
        feitas = sum(1 for t in View.Tarefa_Listar_Por_Sprint(s.get_id())
                     if t.get_status() == StatusTarefa.CONCLUIDA)
        total = len(View.Tarefa_Listar_Por_Sprint(s.get_id()))
        with st.container(border=True):
            st.markdown(f'<b>{s.get_nome()}</b> <span class="task-meta">{s.get_objetivo()}</span>'
                        f'<div class="task-meta">📅 {s.get_data_inicio()} → {s.get_data_fim()} · '
                        f'{feitas}/{total} tarefas</div>', unsafe_allow_html=True)
            if st.button("Excluir sprint", key=f"dels{s.get_id()}"):
                View.Sprint_Excluir(s.get_id()); st.rerun()
    with st.form(f"nova_sprint_{projeto.get_id()}"):
        st.caption("Nova sprint")
        nome = st.text_input("Nome da sprint")
        objetivo = st.text_input("Objetivo")
        c1, c2 = st.columns(2)
        inicio = c1.text_input("Início (AAAA-MM-DD)")
        fim = c2.text_input("Fim (AAAA-MM-DD)")
        if st.form_submit_button("Criar sprint"):
            try:
                View.Sprint_Inserir(nome, objetivo, inicio, fim, projeto.get_id())
                st.success("Sprint criada."); st.rerun()
            except Exception as e:
                st.error(str(e))


def _gerenciar_membros(projeto):
    st.markdown("##### 👤 Membros do projeto")
    membros = View.Projeto_Membros(projeto.get_id())
    if membros:
        for m in membros:
            c1, c2 = st.columns([4, 1])
            c1.write(f"• {m.get_nome()}  ·  _{m.get_email()}_")
            if c2.button("Remover", key=f"rem{m.get_id()}"):
                View.Equipe_Remover_Membro(m.get_id()); st.rerun()
    else:
        st.caption("Nenhum membro ainda.")
    # candidatos: usuarios que nao estao na equipe do projeto
    ids_membros = {m.get_id() for m in membros}
    candidatos = [u for u in View.Usuario_Listar() if u.get_id() not in ids_membros]
    if candidatos:
        c1, c2 = st.columns([3, 1])
        escolhido = c1.selectbox("Adicionar membro", candidatos,
                                 format_func=lambda u: u.get_nome(), key=f"addm{projeto.get_id()}")
        if c2.button("Adicionar", key=f"btnaddm{projeto.get_id()}"):
            View.Equipe_Adicionar_Membro(projeto.get_equipe_id(), escolhido.get_id()); st.rerun()


def pagina_projetos():
    cabecalho("Projetos", "Crie projetos, sprints e adicione membros")
    equipes = mapa_nomes(View.Equipe_Listar())

    with st.expander("➕ Novo projeto"):
        if not View.Equipe_Listar():
            st.info("Crie uma equipe na aba **Equipes** primeiro (o projeto pertence a uma equipe).")
        with st.form("novo_projeto"):
            nome = st.text_input("Nome")
            descricao = st.text_input("Descrição")
            c1, c2 = st.columns(2)
            data_inicio = c1.text_input("Início (AAAA-MM-DD)")
            data_fim = c2.text_input("Fim (AAAA-MM-DD)")
            c3, c4 = st.columns(2)
            status = c3.selectbox("Status", list(StatusProjeto), format_func=lambda s: s.value)
            with c4:
                equipe_id = opcao_id("Equipe", View.Equipe_Listar(), key="eq_new_proj")
            if st.form_submit_button("Criar projeto"):
                try:
                    View.Projeto_Inserir(nome, descricao, data_inicio, data_fim, status, equipe_id)
                    st.success("Projeto criado."); st.rerun()
                except Exception as e:
                    st.error(str(e))

    _cartoes_projetos(equipes)

    st.divider()
    st.markdown("#### 🛠️ Gerenciar projeto")
    projs_hub = View.Projeto_Listar()
    projeto = None
    if not projs_hub:
        st.caption("Crie um projeto acima para gerenciar.")
    else:
        nomes_hub = {p.get_id(): p.get_nome() for p in projs_hub}
        pid_hub = st.selectbox("Selecione um projeto", [p.get_id() for p in projs_hub],
                               format_func=lambda i: nomes_hub[i], key="hub_proj")
        projeto = View.Projeto_Listar_Id(pid_hub)
    if projeto:
        aba_s, aba_m, aba_cfg = st.tabs(["🏃 Sprints", "👤 Membros", "⚙️ Configurações"])
        with aba_s:
            _gerenciar_sprints(projeto)
        with aba_m:
            _gerenciar_membros(projeto)
        with aba_cfg:
            with st.form("edit_projeto"):
                nome = st.text_input("Nome", value=projeto.get_nome())
                descricao = st.text_input("Descrição", value=projeto.get_descricao())
                status = st.selectbox("Status", list(StatusProjeto),
                                      index=list(StatusProjeto).index(projeto.get_status()),
                                      format_func=lambda s: s.value)
                c1, c2 = st.columns(2)
                if c1.form_submit_button("Salvar"):
                    View.Projeto_Atualizar(projeto.get_id(), nome, descricao, status, projeto.get_equipe_id())
                    st.success("Atualizado."); st.rerun()
                if c2.form_submit_button("Excluir projeto"):
                    View.Projeto_Excluir(projeto.get_id()); st.success("Excluído."); st.rerun()


# ----------------------------------------------------------------------
# Usuarios / Equipes / Categorias (ADMIN)
# ----------------------------------------------------------------------
def pagina_usuarios():
    cabecalho("Usuários", "Gerencie as contas de acesso")
    st.dataframe([{"id": u.get_id(), "nome": u.get_nome(), "email": u.get_email(),
                   "perfil": u.get_perfil().value} for u in View.Usuario_Listar()],
                 use_container_width=True, hide_index=True)

    with st.expander("➕ Novo usuário"):
        with st.form("novo_usuario"):
            nome = st.text_input("Nome"); email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            perfil = st.selectbox("Perfil", list(Perfil), format_func=lambda p: p.value)
            if st.form_submit_button("Inserir"):
                try:
                    View.Usuario_Inserir(nome, email, senha, perfil)
                    st.success("Inserido."); st.rerun()
                except Exception as e:
                    st.error(str(e))

    with st.expander("✏️ Editar / excluir"):
        u = selecionar("Usuário", View.Usuario_Listar(), key="sel_user")
        if u:
            with st.form("edit_usuario"):
                nome = st.text_input("Nome", value=u.get_nome())
                email = st.text_input("E-mail", value=u.get_email())
                perfil = st.selectbox("Perfil", list(Perfil),
                                      index=list(Perfil).index(u.get_perfil()),
                                      format_func=lambda p: p.value)
                c1, c2 = st.columns(2)
                if c1.form_submit_button("Salvar"):
                    View.Usuario_Atualizar(u.get_id(), nome, email, perfil)
                    st.success("Atualizado."); st.rerun()
                if c2.form_submit_button("Excluir"):
                    View.Usuario_Excluir(u.get_id()); st.success("Excluído."); st.rerun()

    with st.expander("🔍 Pesquisar por nome"):
        termo = st.text_input("Parte do nome", key="busca_user")
        if termo:
            for u in View.Usuario_Pesquisar_Nome(termo):
                st.write("•", u.get_nome(), f"({u.get_email()})")


def pagina_equipes():
    cabecalho("Equipes", "Times que executam os projetos")
    st.dataframe([{"id": e.get_id(), "nome": e.get_nome(), "descricao": e.get_descricao(),
                   "lider_id": e.get_lider_id()} for e in View.Equipe_Listar()],
                 use_container_width=True, hide_index=True)

    with st.expander("➕ Nova equipe"):
        with st.form("nova_equipe"):
            nome = st.text_input("Nome"); descricao = st.text_input("Descrição")
            lider_id = opcao_id("Líder", View.Usuario_Listar(), permitir_zero=True, key="lider_new")
            if st.form_submit_button("Inserir"):
                try:
                    View.Equipe_Inserir(nome, descricao, lider_id)
                    st.success("Inserida."); st.rerun()
                except Exception as e:
                    st.error(str(e))

    with st.expander("✏️ Editar / excluir"):
        e = selecionar("Equipe", View.Equipe_Listar(), key="sel_eq")
        if e:
            with st.form("edit_equipe"):
                nome = st.text_input("Nome", value=e.get_nome())
                descricao = st.text_input("Descrição", value=e.get_descricao())
                lider_id = st.number_input("Líder id", value=e.get_lider_id(), step=1)
                c1, c2 = st.columns(2)
                if c1.form_submit_button("Salvar"):
                    View.Equipe_Atualizar(e.get_id(), nome, descricao, int(lider_id))
                    st.success("Atualizado."); st.rerun()
                if c2.form_submit_button("Excluir"):
                    View.Equipe_Excluir(e.get_id()); st.success("Excluído."); st.rerun()

    with st.expander("👤 Membros da equipe"):
        eq = selecionar("Equipe", View.Equipe_Listar(), key="sel_eq_membros")
        if eq:
            membros = View.Equipe_Membros(eq.get_id())
            st.caption(f"{len(membros)} membro(s)")
            for m in membros:
                c1, c2 = st.columns([4, 1])
                c1.write(f"• {m.get_nome()}  ·  _{m.get_email()}_")
                if c2.button("Remover", key=f"remeq{m.get_id()}"):
                    View.Equipe_Remover_Membro(m.get_id()); st.rerun()
            ids = {m.get_id() for m in membros}
            cand = [u for u in View.Usuario_Listar() if u.get_id() not in ids]
            if cand:
                c1, c2 = st.columns([3, 1])
                esc = c1.selectbox("Adicionar usuário", cand,
                                   format_func=lambda u: u.get_nome(), key="addeqm")
                if c2.button("Adicionar", key="btnaddeqm"):
                    View.Equipe_Adicionar_Membro(eq.get_id(), esc.get_id()); st.rerun()
            else:
                st.caption("Todos os usuários já estão em alguma equipe.")


def pagina_categorias():
    cabecalho("Categorias", "Etiquetas para classificar tarefas")
    cats = View.Categoria_Listar()
    linhas = "".join(
        f'<div style="display:flex;align-items:center;gap:8px;margin:4px 0">'
        f'<span style="width:14px;height:14px;border-radius:4px;background:{c.get_cor()};display:inline-block"></span>'
        f'<b>{c.get_nome()}</b> <span style="color:#9CA3AF">#{c.get_id()}</span></div>'
        for c in cats)
    st.markdown(linhas or "_Nenhuma categoria._", unsafe_allow_html=True)

    with st.expander("➕ Nova categoria"):
        with st.form("nova_categoria"):
            nome = st.text_input("Nome")
            cor = st.color_picker("Cor", value="#7C3AED")
            if st.form_submit_button("Inserir"):
                try:
                    View.Categoria_Inserir(nome, cor)
                    st.success("Inserida."); st.rerun()
                except Exception as e:
                    st.error(str(e))

    with st.expander("✏️ Editar / excluir"):
        c = selecionar("Categoria", View.Categoria_Listar(), key="sel_cat")
        if c:
            with st.form("edit_categoria"):
                nome = st.text_input("Nome", value=c.get_nome())
                cor = st.color_picker("Cor", value=c.get_cor())
                col1, col2 = st.columns(2)
                if col1.form_submit_button("Salvar"):
                    View.Categoria_Atualizar(c.get_id(), nome, cor)
                    st.success("Atualizado."); st.rerun()
                if col2.form_submit_button("Excluir"):
                    View.Categoria_Excluir(c.get_id()); st.success("Excluído."); st.rerun()


# ----------------------------------------------------------------------
# Comentarios / Calendario
# ----------------------------------------------------------------------
def pagina_comentarios():
    cabecalho("Comentários", "Discussão dentro de cada tarefa")
    t = selecionar("Escolha a tarefa", View.Tarefa_Listar(), campo="get_titulo", key="com_tarefa")
    if t:
        autores = mapa_nomes(View.Usuario_Listar())
        for c in View.Comentario_Listar_Por_Tarefa(t.get_id()):
            with st.container(border=True):
                st.markdown(f'**{autores.get(c.get_autor_id(), "—")}**  '
                            f'<span style="color:#9CA3AF">#{c.get_id()}</span><br>{c.get_texto()}',
                            unsafe_allow_html=True)
        with st.form("novo_comentario"):
            texto = st.text_area("Novo comentário")
            if st.form_submit_button("Comentar"):
                try:
                    View.Comentario_Inserir(texto, t.get_id(), st.session_state.usuario.get_id())
                    st.success("Comentário adicionado."); st.rerun()
                except Exception as e:
                    st.error(str(e))
        coment = View.Comentario_Listar_Por_Tarefa(t.get_id())
        if coment:
            with st.expander("✏️ Editar / excluir comentário"):
                c = selecionar("Comentário", coment, campo="get_texto", key="sel_com")
                if c:
                    with st.form("edit_com"):
                        texto = st.text_input("Texto", value=c.get_texto())
                        col1, col2 = st.columns(2)
                        if col1.form_submit_button("Salvar"):
                            View.Comentario_Atualizar(c.get_id(), texto); st.success("Ok."); st.rerun()
                        if col2.form_submit_button("Excluir"):
                            View.Comentario_Excluir(c.get_id()); st.success("Ok."); st.rerun()


def pagina_calendario():
    cabecalho("Meu calendário", "Seus compromissos e prazos")
    uid = st.session_state.usuario.get_id()
    eventos = View.Evento_Listar_Por_Usuario(uid)
    for e in eventos:
        with st.container(border=True):
            st.markdown(f'<span class="task-title">📅 {e.get_titulo()}</span>'
                        f'<div class="task-meta">{e.get_data_inicio()} → {e.get_data_fim()}</div>',
                        unsafe_allow_html=True)
    if not eventos:
        st.caption("Você não tem eventos.")

    with st.expander("➕ Novo evento"):
        with st.form("novo_evento"):
            titulo = st.text_input("Título"); descricao = st.text_input("Descrição")
            c1, c2 = st.columns(2)
            inicio = c1.text_input("Início (AAAA-MM-DDTHH:MM)")
            fim = c2.text_input("Fim (AAAA-MM-DDTHH:MM)")
            tarefa_id = opcao_id("Tarefa vinculada", View.Tarefa_Listar(), campo="get_titulo",
                                 permitir_zero=True, key="tar_new_ev")
            if st.form_submit_button("Inserir"):
                try:
                    View.Evento_Inserir(titulo, descricao, inicio, fim, uid, tarefa_id)
                    st.success("Evento inserido."); st.rerun()
                except Exception as e:
                    st.error(str(e))

    with st.expander("✏️ Editar / excluir evento"):
        e = selecionar("Evento", View.Evento_Listar_Por_Usuario(uid), campo="get_titulo", key="sel_ev")
        if e:
            with st.form("edit_evento"):
                titulo = st.text_input("Título", value=e.get_titulo())
                inicio = st.text_input("Início", value=e.get_data_inicio())
                fim = st.text_input("Fim", value=e.get_data_fim())
                c1, c2 = st.columns(2)
                if c1.form_submit_button("Salvar"):
                    View.Evento_Atualizar(e.get_id(), titulo, inicio, fim); st.success("Ok."); st.rerun()
                if c2.form_submit_button("Excluir"):
                    View.Evento_Excluir(e.get_id()); st.success("Ok."); st.rerun()


# ----------------------------------------------------------------------
# App principal
# ----------------------------------------------------------------------
PAGINAS = {
    "🏠 Início": pagina_dashboard,
    "✅ Tarefas": pagina_tarefas,
    "📁 Projetos": pagina_projetos,
    "👥 Equipes": pagina_equipes,
}


def app():
    usuario = st.session_state.usuario
    eh_admin = usuario.get_perfil() == Perfil.ADMIN

    with st.sidebar:
        st.markdown(f'<div class="brand">{logo_icon(34)}<span>TaskFlow</span></div>',
                    unsafe_allow_html=True)
        partes = usuario.get_nome().split()
        ini = (partes[0][0] + (partes[1][0] if len(partes) > 1 else "")).upper()
        st.markdown(f'<div class="user-card"><div class="av">{ini}</div>'
                    f'<div style="line-height:1.15"><b>{usuario.get_nome()}</b><br>'
                    f'<small style="opacity:.75">{usuario.get_perfil().value}</small></div></div>',
                    unsafe_allow_html=True)

        itens = ["🏠 Início", "✅ Tarefas"]
        if eh_admin:
            itens += ["📁 Projetos", "👥 Equipes"]
        escolha = st.radio("Navegação", itens, label_visibility="collapsed", key="nav")

        # callbacks de navegacao a partir da lista de projetos/sprints
        def _ir_projeto(pid):
            st.session_state["nav"] = "📁 Projetos" if eh_admin else "✅ Tarefas"
            if eh_admin:
                st.session_state["hub_proj"] = pid

        def _ir_sprint(label):
            st.session_state["nav"] = "✅ Tarefas"
            st.session_state["filtro_tarefas"] = label

        # Projetos e sprints CLICAVEIS (vao para as informacoes)
        projetos = View.Projeto_Listar()
        proj_nome = {p.get_id(): p.get_nome() for p in projetos}
        emojis = ["🟠", "🟢", "🔵", "🟣", "🟡", "🩵"]
        if projetos:
            st.markdown('<div class="side-label">PROJETOS</div>', unsafe_allow_html=True)
            for p in projetos:
                em = emojis[p.get_id() % len(emojis)]
                n = len(View.Tarefa_Listar_Por_Projeto(p.get_id()))
                st.button(f"{em}  {p.get_nome()}   ·  {n}", key=f"navp{p.get_id()}",
                          use_container_width=True, on_click=_ir_projeto, args=(p.get_id(),))
                for s in View.Sprint_Listar_Por_Projeto(p.get_id()):
                    lbl = f"{s.get_id()} · {proj_nome[p.get_id()]} / {s.get_nome()}"
                    st.button(f"　　▪ {s.get_nome()}", key=f"navs{s.get_id()}",
                              use_container_width=True, on_click=_ir_sprint, args=(lbl,))

        st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)
        if st.button("Sair", use_container_width=True, type="primary"):
            st.session_state.usuario = None
            st.rerun()

    PAGINAS[escolha]()


# --- roteamento ---
css()
if st.session_state.usuario is None:
    tela_acesso()
else:
    app()
