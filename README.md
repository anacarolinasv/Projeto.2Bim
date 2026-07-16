# Documento de Visão do Sistema

**Disciplina:** Programação Orientada a Objetos — 2º Bimestre — 2026.1
**Curso:** Tecnologia em Análise e Desenvolvimento de Sistemas — IFRN/DIATINF

---

## 1. Título do Projeto

**TaskFlow — Gerenciador de Tarefas e Calendário**
(aplicação inspirada no Asana)

## 2. Objetivo do Sistema

Oferecer uma ferramenta para **organização e acompanhamento de trabalho em
equipe**, permitindo que times criem projetos, organizem esses projetos em
**sprints**, distribuam tarefas entre seus membros, classifiquem essas tarefas
por categoria, registrem comentários e acompanhem prazos por meio de um
calendário de eventos. O sistema centraliza, em um só lugar, *o que precisa
ser feito, por quem, em qual sprint e até quando*.

## 3. Descrição do Problema a ser Resolvido

Equipes que gerenciam suas atividades por meio de mensagens avulsas, planilhas
ou anotações soltas enfrentam problemas recorrentes:

- Falta de **visão unificada** das tarefas de um projeto e de seu andamento;
- Dificuldade para saber **quem é responsável** por cada tarefa e qual o seu
  **prazo**;
- Ausência de **histórico** (comentários) sobre o que já foi discutido em cada
  tarefa;
- Nenhum vínculo entre as tarefas e um **calendário** de compromissos.

O TaskFlow resolve esses problemas modelando explicitamente equipes, projetos, sprints,
tarefas, responsáveis, categorias, comentários e eventos, com regras que mantêm
as informações consistentes (por exemplo, concluir todas as tarefas de um
projeto  — em todas as suas sprints —  o marca automaticamente como concluído).

## 4. Perfis de Usuários Envolvidos

O sistema possui **controle de login** com dois perfis de acesso:

| Perfil | Descrição | Responsabilidades |
|--------|-----------|-------------------|
| **ADMIN** (Gestor) | Administrador do sistema/equipe. | Gerencia usuários, equipes, projetos, sprints e categorias; associa projetos a equipes e sprints a projetos; define o líder e os membros de cada equipe; tem acesso a todas as operações de cadastro. |
| **MEMBRO** (Colaborador) | Integrante que executa o trabalho. | Gerencia suas tarefas e comentários, atualiza o status das tarefas sob sua responsabilidade e mantém seus eventos de calendário. |

## 5. Lista de Operações do Aplicativo

### 5.1. Autenticação (ambos os perfis)
- Entrar no sistema (login por e-mail e senha)
- Sair do sistema (logout)

### 5.2. Operações de CRUD por entidade
Para **cada** uma das entidades abaixo o sistema oferece **inserir, listar,
atualizar e excluir**:

- Usuário *(ADMIN)*
- Equipe *(ADMIN)*
- Projeto *(ADMIN)*
- Sprint *(ADMIN)*
- Categoria *(ADMIN)*
- Tarefa *(MEMBRO / ADMIN)*
- Comentário *(MEMBRO / ADMIN)*
- Evento *(MEMBRO / ADMIN)*

### 5.3. Operações de associação entre entidades
- Vincular um **projeto** a uma **equipe**
- Definir o **líder** de uma **equipe**
- Adicionar ou remover um **usuário** como **membro** de uma **equipe**
- Vincular uma **sprint** a um **projeto**
- Atribuir uma **tarefa** a um **responsável** (usuário)
- Classificar uma **tarefa** em uma **categoria**
- Adicionar um **comentário** a uma **tarefa**
- Vincular um **evento** de calendário a uma **tarefa**

### 5.4. Operações de pesquisa (listagem parcial)
- Pesquisar **usuários** por parte do nome
- Pesquisar **equipes / projetos / categorias** por parte do nome
- Pesquisar **tarefas / eventos** por parte do título
- Listar **projetos de uma equipe**, **membros de uma equipe/projeto**,
  **sprints de um projeto**, **tarefas de uma sprint** (ou de um projeto
  inteiro, percorrendo suas sprints), **comentários de uma tarefa** e
  **eventos de um usuário**
- Consultar o **progresso de um projeto** (quantidade de tarefas concluídas
  em relação ao total)

### 5.5. Regras de negócio (manipulam mais de uma entidade)
- **Concluir tarefa:** ao concluir uma tarefa, o sistema atualiza o status da
  `Tarefa` e, a partir da sua `Sprint`, localiza o `Projeto` correspondente;
  se **todas** as tarefas do projeto (somando-se as de todas as suas sprints)
  estiverem concluídas, o **projeto** é automaticamente marcado como
  **CONCLUÍDO** (operação que altera as entidades `Tarefa`, `Sprint` e
  `Projeto` de uma só vez).

## 6. Entidades do Modelo

Total de **7 entidades de negócio** + a entidade de **controle de usuário**:

1. **Usuario** (controle de acesso)
2. **Equipe**
3. **Projeto**
4. **Sprint**
5. **Categoria**
6. **Tarefa**
7. **Comentario**
8. **Evento**

**Relacionamentos de associação um-para-muitos:**
- Equipe `1 → N` Usuario (membros da equipe)
- Equipe `1 → N` Projeto
- Projeto `1 → N` Sprint
- Sprint `1 → N` Tarefa
- Categoria `1 → N` Tarefa
- Tarefa `1 → N` Comentario
- Usuario `1 → N` Tarefa (responsável)
- Usuario `1 → N` Evento
- Usuario `1 → N` Comentario (autor)
- Evento `0..1 → 1` Tarefa (cada evento pode estar vinculado a, no máximo, uma tarefa; o vínculo é opcional)