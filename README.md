# Financial Assistant Telegram Bot

Bot Telegram em Python com CRUD de tarefas usando **python-telegram-bot**, **LangGraph** para orquestração de estado e **SQLite + SQLAlchemy** para persistência.

## 1. Descrição do projeto

Projeto modular preparado para evolução, com separação entre interface Telegram, fluxo conversacional (LangGraph), regras de negócio e persistência.

## 2. Tecnologias utilizadas

- Python 3.12+
- python-telegram-bot
- LangGraph (LangChain apenas como dependência base do ecossistema)
- SQLite
- SQLAlchemy 2.x
- Pydantic + pydantic-settings
- python-dotenv
- pytest

## 3. Arquitetura

- **Handlers Telegram**: recebem mensagens/callbacks e delegam para serviços.
- **LangGraph**: controla estado (`action`, `step`, `data`) e transições do fluxo.
- **Services**: validação e regras de negócio.
- **Repositories**: acesso isolado ao banco.
- **Models**: entidades SQLAlchemy (`users`, `tasks`, `conversation_states`).

## 4. Estrutura de pastas

```text
app/
  main.py
  config/
  bot/
    handlers/
    keyboards/
    messages/
  graph/
    state.py
    graph.py
    nodes/
  database/
    database.py
    models/
    repositories/
  services/
  utils/
tests/
.env.example
pyproject.toml
```

## 5. Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## 6. Configuração do `.env`

Copie `.env.example` para `.env` e preencha:

```env
TELEGRAM_BOT_TOKEN=
DATABASE_URL=sqlite:///./data/bot.db
LOG_LEVEL=INFO
```

## 7. Criação do bot no BotFather

1. Abra `@BotFather` no Telegram.
2. Use `/newbot` e defina nome e username.
3. Copie o token gerado.
4. Cole em `TELEGRAM_BOT_TOKEN` no `.env`.

## 8. Execução local

```bash
python -m app.main
```

## 9. Execução dos testes

```bash
pytest
```

## 10. Fluxo do LangGraph

Fluxo principal:

- `START -> menu`
- `menu -> action_create|action_list|action_edit|action_delete`
- Criação: `waiting_title -> waiting_description -> waiting_status -> save -> menu`
- Edição: `select task -> select field -> validate/update -> menu`
- Exclusão: `select task -> confirm -> delete -> menu`
- Cancelamento global via callback `cancel`.

Estado é persistido por usuário em `conversation_states`, garantindo isolamento entre usuários.

## 11. Persistência

- `users`: usuário Telegram (`telegram_user_id` único).
- `tasks`: tarefas por usuário.
- `conversation_states`: estado da conversa por usuário.

Banco é criado automaticamente na inicialização (`Base.metadata.create_all`).

## 12. Exemplos de interação

- `/start` -> menu principal com botões.
- `➕ Criar` -> título -> descrição -> status -> confirmação.
- `📋 Listar` -> lista paginada.
- `✏️ Editar` -> seleção por botões -> campo -> novo valor.
- `🗑️ Excluir` -> seleção por botões -> confirmação `✅ Sim/❌ Não`.
