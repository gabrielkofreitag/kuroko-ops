# KUROKO-OPS — Plano Completo de Fork & Refactoring v0.1.0

> **Origem:** [AndyMik90/Auto-Claude](https://github.com/AndyMik90/Auto-Claude) (AGPL-3.0)
> **Alvo:** `kuroko-ops` — painel multi-LLM, Docker-first, MUI v6, sem lock-in
> **Licença:** AGPL-3.0 (mantida do upstream)
> **Domínio:** kuroko-ops.work
> **Data:** 2025-07

---

## PARTE 1 — PLANO GERAL

### 1.1 Análise do Repositório Original

| Camada | Pasta | Stack |
|--------|-------|-------|
| Backend | `apps/backend/` | Python 3.12+, `claude-agent-sdk`, FastAPI/Uvicorn, WebSocket |
| Frontend | `apps/frontend/` | Electron 39, React 19, TypeScript 5, Zustand 5, Tailwind v4, Vite |
| Testes | `tests/` | Pytest, Vitest |
| Scripts | `scripts/` | Shell helpers (build, clean, install) |
| Raiz | `.` | Monorepo, `pyproject.toml`, `package.json`, AGPL-3.0 |

### 1.2 Arquivos com Lock-in Claude (17 arquivos)

| Arquivo | Dependência | Ação |
|---------|-------------|------|
| `core/client.py` | `claude-agent-sdk` (ClaudeSDKClient) | Reescrever → `LLMClient` via OpenAI SDK |
| `core/simple_client.py` | `claude-agent-sdk` (SimpleClaudeClient) | Reescrever → `SimpleLLMClient` |
| `core/auth.py` | Claude OAuth (~1200 linhas) | Remover inteiro → env `OPENROUTER_API_KEY` |
| `core/config.py` | Referências `CLAUDE_*` env | Renomear para `OPENROUTER_*` / `LLM_*` |
| `core/claude_client.py` | SDK merge/analyzer | Reescrever → `core/llm_client.py` |
| `core/server.py` | Importa `ClaudeSDKClient` | Importar `LLMClient` |
| `core/session.py` | Sessão Claude SDK | Reescrever → `AgentSession` OpenAI-compatible |
| `core/tools/*.py` | Claude tool format (Read/Write/Bash/Glob/Grep) | Remover no MVP; reimplementar via function-calling |
| `apps/frontend/.../ClaudeOAuthFlow.tsx` | OAuth UI inteira | Remover → tela de API key |
| `apps/frontend/.../profile-service.ts` | `profileManager.getActiveProfile()` Claude | Simplificar → config.apiKey |
| `apps/frontend/.../config.ts` | `CLAUDE_API_*` constants | Renomear → `OPENROUTER_*` |
| `apps/frontend/.../api-client.ts` | Endpoint `/claude/*` | Renomear → `/llm/*` |
| `apps/frontend/.../stores/*.ts` | Zustand stores com refs Claude | Atualizar tipos/interfaces |
| `electron.vite.config.ts` | Nenhum lock-in direto | Manter |
| `tailwind.config.ts` | Tailwind v4 config | **REMOVER** (migração MUI) |
| `postcss.config.js` | PostCSS p/ Tailwind | **REMOVER** (migração MUI) |
| `CLAUDE.md` | Instruções para Claude Code | Renomear → `AGENTS.md` |

### 1.3 Mapeamento de Dependências

```
REMOVER (pip):
  claude-agent-sdk
  anthropic (se presente)

ADICIONAR (pip):
  openai >= 1.40
  litellm >= 1.40
  pydantic >= 2.0
  sqlmodel >= 0.0.16
  aiosqlite >= 0.20

REMOVER (npm):
  @anthropic-ai/sdk
  tailwindcss
  @tailwindcss/vite (ou postcss plugin)
  autoprefixer (se só para Tailwind)

ADICIONAR (npm):
  openai (npm)
  @mui/material >= 6.0
  @mui/icons-material
  @emotion/react
  @emotion/styled
  @mui/joy (Joy UI, componentes extras)
```

### 1.4 Arquitetura-Alvo

```
┌─────────────────────────────────────────────────────────┐
│                    kuroko-ops                            │
│                                                         │
│  ┌──────────────┐   WebSocket    ┌──────────────────┐   │
│  │   Electron   │◄──────────────►│  Python Backend  │   │
│  │  React + MUI │                │  FastAPI/Uvicorn  │   │
│  │  Zustand     │                │                    │  │
│  │  (persist)   │                │  ┌──────────────┐  │  │
│  └──────────────┘                │  │  LLMClient   │  │  │
│                                  │  │  (OpenAI SDK) │  │  │
│                                  │  │  base_url =   │  │  │
│                                  │  │  openrouter   │  │  │
│                                  │  └──────┬───────┘  │  │
│                                  │         │          │  │
│                                  │  ┌──────▼───────┐  │  │
│                                  │  │   LiteLLM    │  │  │
│                                  │  │   Router     │  │  │
│                                  │  │  (profiles)  │  │  │
│                                  │  └──────┬───────┘  │  │
│                                  │         │          │  │
│                                  │  ┌──────▼───────┐  │  │
│                                  │  │  Persistence │  │  │
│                                  │  │  SQLite +    │  │  │
│                                  │  │  JSON state  │  │  │
│                                  │  └──────────────┘  │  │
│                                  └──────────────────┘   │
│                                           │             │
│                                    ┌──────▼──────┐      │
│                                    │  OpenRouter │      │
│                                    │  API        │      │
│                                    └─────────────┘      │
└─────────────────────────────────────────────────────────┘
```

### 1.5 Escopo MVP v0.1.0

O v0.1.0 é a primeira versão funcional e **inclui obrigatoriamente**:

| # | Feature | Descrição |
|---|---------|-----------|
| 1 | **Core LLM Client** | OpenAI SDK → OpenRouter, streaming, error handling |
| 2 | **LiteLLM Routing** | Smart/cheap profiles por role, fallback, cost tracking |
| 3 | **Persistence** | Zustand persist, SQLite sessions, resume exato |
| 4 | **Agent Teams** | PO delega sub-times, handoff, spawn dinâmico |
| 5 | **Security** | Audit logs em Docker volume, allowlist UI, sandbox opcional |
| 6 | **MUI v6 Migration** | Remove Tailwind **inteiramente**, ThemeProvider com 7 temas |
| 7 | **UX Polish** | Docker wizard, webhooks Telegram/Slack, bug fixes |
| 8 | **Docker-first** | docker-compose up funcional, volumes, .env |

### 1.6 Princípios de Implementação

1. **Incrementalidade** — Cada sprint produz código testável e commit-ável
2. **Zero Tailwind** — Nenhuma classe utilitária `tw-*`/`bg-*`/`flex` sobrevive
3. **Provider-agnostic** — Qualquer LLM compatível OpenAI Chat Completions API
4. **Docker-first** — Se não roda em `docker-compose up`, não está pronto
5. **Auditabilidade** — Todo acesso a FS/shell/rede é logado
6. **Resumability** — Crash/restart não perde contexto de agentes

---

## PARTE 2 — SPRINTS (27 sprints em 7 fases)

### ═══════════════════════════════════════════
### FASE A — FUNDAÇÃO (Sprints 0–4)
### ═══════════════════════════════════════════

---

### Sprint 0 — Fork, rename & scaffolding

**Objetivo:** Criar o repositório kuroko-ops a partir do fork, renomear referências globais, setup de tooling.

**Tarefas:**

1. Fork `AndyMik90/Auto-Claude` → `kuroko-ops`
2. Busca global: substituir `Auto-Claude` → `kuroko-ops`, `auto-claude` → `kuroko-ops`
3. Renomear `CLAUDE.md` → `AGENTS.md` (manter conteúdo, adaptar referências)
4. Atualizar `package.json`:
   - `name` → `kuroko-ops`
   - `description` → atualizar
   - `repository.url` → novo repo
   - `license` → manter `AGPL-3.0`
5. Atualizar `pyproject.toml`:
   - `name` → `kuroko-ops`
   - Remover `claude-agent-sdk` de deps
   - Adicionar `openai`, `litellm`, `pydantic`, `sqlmodel`, `aiosqlite`
6. Criar `.env.example`:
   ```env
   OPENROUTER_API_KEY=sk-or-v1-...
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   DEFAULT_MODEL=anthropic/claude-sonnet-4-20250514
   SMART_MODEL=anthropic/claude-sonnet-4-20250514
   CHEAP_MODEL=google/gemini-2.0-flash-001
   CODING_MODEL=anthropic/claude-sonnet-4-20250514
   LOG_LEVEL=INFO
   DOCKER_WORKSPACE=/workspace
   ```
7. Criar `docker-compose.yml` (stub inicial)
8. Criar `Dockerfile` backend + `Dockerfile` frontend (stubs)
9. Adicionar `.gitignore` adequado (node_modules, __pycache__, .env, dist, *.db)
10. Commit inicial: `feat: fork auto-claude → kuroko-ops`

**Entregável:** Repositório renomeado, deps declaradas, builds quebrados (esperado).

**Critério de aceite:**
- `grep -r "Auto-Claude" . --include="*.py" --include="*.ts" --include="*.md"` → 0 resultados
- `.env.example` existe com todas as vars documentadas
- `pyproject.toml` lista `openai` e `litellm` como deps

---

### Sprint 1 — Core LLM Client (OpenAI SDK)

**Objetivo:** Criar `core/llm_client.py` — substituto direto do `ClaudeSDKClient`.

**Tarefas:**

1. Criar `core/llm_client.py`:
   ```python
   from openai import OpenAI
   import os

   class LLMClient:
       def __init__(self, model: str | None = None):
           self.client = OpenAI(
               api_key=os.getenv("OPENROUTER_API_KEY"),
               base_url=os.getenv("OPENROUTER_BASE_URL",
                                   "https://openrouter.ai/api/v1"),
           )
           self.model = model or os.getenv("DEFAULT_MODEL",
                                            "anthropic/claude-sonnet-4-20250514")

       def chat(self, messages: list[dict], **kwargs) -> str:
           response = self.client.chat.completions.create(
               model=self.model,
               messages=messages,
               **kwargs,
           )
           return response.choices[0].message.content

       def chat_stream(self, messages: list[dict], **kwargs):
           stream = self.client.chat.completions.create(
               model=self.model,
               messages=messages,
               stream=True,
               **kwargs,
           )
           for chunk in stream:
               delta = chunk.choices[0].delta
               if delta.content:
                   yield delta.content
   ```
2. Criar `core/async_llm_client.py` (versão AsyncOpenAI para WebSocket)
3. Criar `core/models.py` — Pydantic models:
   - `ChatMessage(role, content, name?, tool_calls?)`
   - `LLMResponse(content, model, usage, cost?)`
   - `AgentConfig(name, model, system_prompt, max_tokens)`
4. Criar `tests/test_llm_client.py`:
   - Mock do OpenAI client
   - Teste sync `chat()` → resposta correta
   - Teste `chat_stream()` → chunks iteráveis
   - Teste fallback de model via env var
5. Criar `core/__init__.py` exportando `LLMClient`

**Entregável:** Client funcional que conecta ao OpenRouter.

**Critério de aceite:**
- `pytest tests/test_llm_client.py` → passa
- `python -c "from core.llm_client import LLMClient; c = LLMClient(); print(c.chat([{'role':'user','content':'ping'}]))"` → resposta do modelo

---

### Sprint 2 — Remoção do Auth Claude OAuth

**Objetivo:** Eliminar o sistema OAuth Claude (~1200 linhas) e substituir por API key simples.

**Tarefas:**

1. **Deletar** `core/auth.py` (inteiro — OAuth Claude)
2. **Deletar** `apps/frontend/src/.../ClaudeOAuthFlow.tsx`
3. **Deletar** `apps/frontend/src/.../profile-service.ts` (gerenciador de perfis Claude)
4. Criar `core/auth.py` (novo, mínimo):
   ```python
   import os

   def get_api_key() -> str:
       key = os.getenv("OPENROUTER_API_KEY")
       if not key:
           raise ValueError(
               "OPENROUTER_API_KEY não definida. "
               "Copie .env.example → .env e preencha."
           )
       return key

   def validate_api_key(key: str) -> bool:
       """Testa a key fazendo um request mínimo ao OpenRouter."""
       from openai import OpenAI
       try:
           client = OpenAI(api_key=key,
                           base_url="https://openrouter.ai/api/v1")
           client.models.list()
           return True
       except Exception:
           return False
   ```
5. Criar `apps/frontend/src/components/ApiKeySetup.tsx`:
   - Input p/ colar API key
   - Botão "Validar" → chama backend `/api/auth/validate`
   - Salva em electron-store (criptografado)
   - Sem OAuth, sem redirects
6. Atualizar `core/config.py`:
   - Remover `CLAUDE_*` vars
   - Adicionar `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`
   - Adicionar `DEFAULT_MODEL`, `SMART_MODEL`, `CHEAP_MODEL`
7. Criar `tests/test_auth.py`:
   - Teste `get_api_key()` com env var presente
   - Teste `get_api_key()` sem env var → ValueError
   - Teste `validate_api_key()` com mock

**Entregável:** Zero código OAuth, auth por API key funcional.

**Critério de aceite:**
- `grep -r "OAuth\|claude.*auth\|ClaudeOAuth" --include="*.py" --include="*.ts"` → 0
- `validate_api_key()` retorna `True` com key válida
- `core/auth.py` < 50 linhas

---

### Sprint 3 — Refactor de Endpoints Backend

**Objetivo:** Substituir todas as rotas `/claude/*` por `/llm/*` e atualizar imports.

**Tarefas:**

1. Busca global em `core/server.py` e `core/routes/`:
   - `/claude/` → `/llm/`
   - `from core.client import ClaudeSDKClient` → `from core.llm_client import LLMClient`
   - `from core.simple_client import SimpleClaudeClient` → remover (usar LLMClient)
2. Atualizar WebSocket handlers:
   - `ClaudeSDKClient` context manager → `LLMClient` instância normal
   - `async for msg in client.receive_response()` → `for chunk in client.chat_stream()`
   - Manter protocolo WS existente para o frontend
3. Atualizar `core/session.py`:
   - `ClaudeSession` → `AgentSession`
   - Remover refs a `claude-agent-sdk` tools
   - Adicionar campo `model: str` por sessão
4. **Deletar** `core/client.py` (antigo Claude SDK client)
5. **Deletar** `core/simple_client.py`
6. **Deletar** `core/claude_client.py` (merge/analyzer)
7. Atualizar `apps/frontend/src/services/api-client.ts`:
   - Endpoints `/claude/*` → `/llm/*`
   - Remover imports de tipos Claude-specific
8. Criar `tests/test_server.py`:
   - Teste endpoint `POST /llm/chat`
   - Teste WebSocket `/ws/agent`
   - Teste 401 sem API key

**Entregável:** Backend funcional sem referências Claude.

**Critério de aceite:**
- `grep -r "claude" --include="*.py" apps/backend/ core/` → 0 (exceto comentários de migração)
- `pytest tests/test_server.py` → passa
- WebSocket conecta e recebe streaming

---

### Sprint 4 — Frontend: Limpeza Claude & API Key Flow

**Objetivo:** Frontend conecta ao novo backend sem refs Claude.

**Tarefas:**

1. Limpar `apps/frontend/src/`:
   - Remover imports/referências a `@anthropic-ai/sdk`
   - `npm uninstall @anthropic-ai/sdk`
   - Remover componentes Claude-specific (OAuth, profile switcher)
2. Atualizar Zustand stores:
   - `useAuthStore` → simplificar (apiKey string, isValidated boolean)
   - `useAgentStore` → remover refs a Claude models, adicionar `model: string`
   - `useSettingsStore` → remover Claude-specific settings
3. Integrar `ApiKeySetup.tsx` (Sprint 2) no fluxo de onboarding
4. Atualizar `config.ts`:
   - `API_BASE_URL` → manter
   - Remover `CLAUDE_API_*` constants
   - Adicionar `OPENROUTER_*` constants
5. Testar fluxo completo:
   - App abre → pede API key → valida → salva → redireciona ao dashboard
   - Chat envia mensagem → recebe stream do backend
6. **Não migrar CSS ainda** — Tailwind ainda funciona nesta fase (será removido na Fase D)

**Entregável:** Frontend funcional end-to-end com novo backend.

**Critério de aceite:**
- `npm run build` → sem erros
- `grep -r "anthropic\|claude-sdk\|ClaudeOAuth" --include="*.ts" --include="*.tsx"` → 0
- Fluxo: key setup → chat → streaming funciona

---

### ═══════════════════════════════════════════
### FASE B — MULTI-MODEL & PERSISTÊNCIA (Sprints 5–8)
### ═══════════════════════════════════════════

---

### Sprint 5 — LiteLLM Router & Model Profiles

**Objetivo:** Implementar roteamento inteligente de modelos via LiteLLM.

**Tarefas:**

1. Criar `core/router.py`:
   ```python
   from litellm import Router
   import os, json

   DEFAULT_PROFILES = {
       "smart": {
           "model": os.getenv("SMART_MODEL", "anthropic/claude-sonnet-4-20250514"),
           "description": "Raciocínio complexo, planejamento, revisão de código",
           "max_tokens": 8192,
       },
       "cheap": {
           "model": os.getenv("CHEAP_MODEL", "google/gemini-2.0-flash-001"),
           "description": "Tarefas simples, formatação, classificação",
           "max_tokens": 4096,
       },
       "coding": {
           "model": os.getenv("CODING_MODEL", "anthropic/claude-sonnet-4-20250514"),
           "description": "Geração e revisão de código",
           "max_tokens": 8192,
       },
       "fast": {
           "model": os.getenv("FAST_MODEL", "google/gemini-2.0-flash-001"),
           "description": "Respostas rápidas, low-latency",
           "max_tokens": 2048,
       },
   }

   class ModelRouter:
       def __init__(self):
           self.profiles = {**DEFAULT_PROFILES}
           custom = os.getenv("MODEL_PROFILES_JSON")
           if custom:
               self.profiles.update(json.loads(custom))

           self.router = Router(
               model_list=self._build_model_list(),
               routing_strategy="simple-shuffle",
               num_retries=2,
               fallbacks=[
                   {"smart": ["coding"]},
                   {"coding": ["smart"]},
               ],
           )

       def _build_model_list(self) -> list:
           # Constrói a lista de modelos para o LiteLLM Router
           models = []
           for profile_name, cfg in self.profiles.items():
               models.append({
                   "model_name": profile_name,
                   "litellm_params": {
                       "model": f"openrouter/{cfg['model']}",
                       "api_key": os.getenv("OPENROUTER_API_KEY"),
                       "api_base": os.getenv("OPENROUTER_BASE_URL",
                                              "https://openrouter.ai/api/v1"),
                   },
               })
           return models

       def resolve_model(self, role: str) -> str:
           """Dado um role de agente, retorna o profile adequado."""
           role_map = {
               "po": "smart",
               "architect": "smart",
               "developer": "coding",
               "reviewer": "smart",
               "tester": "coding",
               "writer": "cheap",
               "classifier": "fast",
           }
           return role_map.get(role, "cheap")

       async def chat(self, profile: str, messages: list, **kwargs):
           return await self.router.acompletion(
               model=profile,
               messages=messages,
               **kwargs,
           )
   ```
2. Criar `core/cost_tracker.py`:
   ```python
   from dataclasses import dataclass, field
   from datetime import datetime
   import json, os

   @dataclass
   class UsageRecord:
       timestamp: str
       model: str
       profile: str
       prompt_tokens: int
       completion_tokens: int
       cost_usd: float
       session_id: str

   class CostTracker:
       def __init__(self, budget_usd: float = 10.0):
           self.budget = budget_usd
           self.records: list[UsageRecord] = []

       @property
       def total_cost(self) -> float:
           return sum(r.cost_usd for r in self.records)

       @property
       def remaining(self) -> float:
           return max(0, self.budget - self.total_cost)

       def record(self, model: str, profile: str, usage: dict,
                  session_id: str) -> UsageRecord:
           # LiteLLM retorna cost via completion_cost()
           from litellm import completion_cost
           cost = completion_cost(
               model=model,
               prompt=str(usage.get("prompt_tokens", 0)),
               completion=str(usage.get("completion_tokens", 0)),
           )
           rec = UsageRecord(
               timestamp=datetime.utcnow().isoformat(),
               model=model, profile=profile,
               prompt_tokens=usage.get("prompt_tokens", 0),
               completion_tokens=usage.get("completion_tokens", 0),
               cost_usd=cost, session_id=session_id,
           )
           self.records.append(rec)
           return rec

       def check_budget(self) -> bool:
           """Retorna False se o budget foi excedido."""
           return self.total_cost < self.budget

       def export_json(self) -> str:
           return json.dumps([r.__dict__ for r in self.records], indent=2)
   ```
3. Integrar `ModelRouter` no `LLMClient`:
   - `LLMClient.__init__` recebe `router: ModelRouter | None`
   - Se `router` presente, delega via `router.chat(profile, messages)`
   - Se não, usa OpenAI SDK diretamente (fallback simples)
4. Criar `core/budget_alert.py`:
   - Webhook genérico (HTTP POST) quando custo atinge 50%, 80%, 100% do budget
   - Base para integração Telegram/Slack (Sprint 21)
5. Endpoint `GET /api/costs`:
   - Retorna `{ total_cost, budget, remaining, records[] }`
6. Criar `tests/test_router.py`:
   - Teste `resolve_model("po")` → `"smart"`
   - Teste `resolve_model("unknown")` → `"cheap"`
   - Teste fallback `smart` → `coding`
7. Criar `tests/test_cost_tracker.py`:
   - Teste `record()` com mock de `completion_cost`
   - Teste `check_budget()` com budget excedido

**Entregável:** Roteamento multi-model funcional com tracking de custo.

**Critério de aceite:**
- `pytest tests/test_router.py tests/test_cost_tracker.py` → passa
- Agente PO usa model `smart`, agente writer usa `cheap`
- `GET /api/costs` retorna JSON com totais corretos

---

### Sprint 6 — Zustand Persist & State Hydration

**Objetivo:** Persistir todo o estado do frontend para sobreviver a crashes/restarts.

**Tarefas:**

1. Instalar `zustand/middleware`:
   - Já incluído no Zustand 5
   - Configurar `persist` middleware em todos os stores
2. Atualizar `useAuthStore`:
   ```typescript
   import { create } from 'zustand';
   import { persist, createJSONStorage } from 'zustand/middleware';

   interface AuthState {
     apiKey: string | null;
     isValidated: boolean;
     setApiKey: (key: string) => void;
     clearAuth: () => void;
   }

   export const useAuthStore = create<AuthState>()(
     persist(
       (set) => ({
         apiKey: null,
         isValidated: false,
         setApiKey: (key) => set({ apiKey: key, isValidated: true }),
         clearAuth: () => set({ apiKey: null, isValidated: false }),
       }),
       {
         name: 'kuroko-auth',
         storage: createJSONStorage(() => localStorage),
         // API key NÃO persiste em localStorage em produção
         // Usar electron-store com encryption
         partialize: (state) => ({ isValidated: state.isValidated }),
       }
     )
   );
   ```
3. Atualizar `useAgentStore` com persist:
   - Persistir: lista de agentes, status, tarefas atribuídas
   - NÃO persistir: WebSocket connection, streaming state
   - `partialize` para excluir campos voláteis
4. Atualizar `useProjectStore` com persist:
   - Persistir: lista de projetos, projeto ativo, configurações
   - Versioning: `version: 1` no persist config para migrações futuras
5. Criar `useSessionStore` (novo):
   ```typescript
   interface SessionState {
     sessions: Record<string, SessionData>;
     activeSessionId: string | null;
     // SessionData inclui: messages[], agentConfig, timestamps
   }
   ```
   - Persistir sessões completas para resume
6. Electron-specific storage adapter:
   ```typescript
   // Para Electron, usar electron-store em vez de localStorage
   import Store from 'electron-store';
   const electronStorage = {
     getItem: (name: string) => electronStore.get(name),
     setItem: (name: string, value: string) => electronStore.set(name, value),
     removeItem: (name: string) => electronStore.delete(name),
   };
   ```
7. Criar `apps/frontend/src/utils/state-migration.ts`:
   - Funções de migração de versão do state
   - `migrate(persistedState, version)` → estado atualizado
8. Testar:
   - Refresh da página → state restaurado
   - Kill electron → reabrir → state restaurado
   - State corrupto → fallback para defaults

**Entregável:** Estado do frontend sobrevive a restarts.

**Critério de aceite:**
- Fechar e reabrir app → projetos, agentes, e configurações mantidos
- `localStorage` (ou electron-store) contém os dados persistidos
- State version migration funciona

---

### Sprint 7 — SQLite Backend Persistence

**Objetivo:** Persistir sessões, mensagens e estado de agentes no backend via SQLite.

**Tarefas:**

1. Criar `core/database.py`:
   ```python
   from sqlmodel import SQLModel, create_engine, Session, Field
   from datetime import datetime
   import os

   DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/kuroko.db")
   engine = create_engine(DATABASE_URL, echo=False)

   class AgentSessionDB(SQLModel, table=True):
       id: str = Field(primary_key=True)
       agent_name: str
       model: str
       profile: str
       system_prompt: str
       status: str = "active"  # active, paused, completed, failed
       created_at: datetime = Field(default_factory=datetime.utcnow)
       updated_at: datetime = Field(default_factory=datetime.utcnow)
       metadata_json: str = "{}"

   class MessageDB(SQLModel, table=True):
       id: int = Field(primary_key=True)
       session_id: str = Field(foreign_key="agentsessiondb.id")
       role: str  # system, user, assistant, tool
       content: str
       token_count: int = 0
       cost_usd: float = 0.0
       created_at: datetime = Field(default_factory=datetime.utcnow)

   class TaskDB(SQLModel, table=True):
       id: str = Field(primary_key=True)
       session_id: str = Field(foreign_key="agentsessiondb.id")
       title: str
       description: str = ""
       status: str = "pending"  # pending, in_progress, done, failed
       assigned_agent: str = ""
       parent_task_id: str | None = None
       created_at: datetime = Field(default_factory=datetime.utcnow)
       completed_at: datetime | None = None

   def init_db():
       SQLModel.metadata.create_all(engine)

   def get_session():
       with Session(engine) as session:
           yield session
   ```
2. Criar `core/persistence.py`:
   ```python
   class PersistenceManager:
       """Gerencia save/load de sessões de agente."""

       def save_session(self, session: AgentSession) -> None: ...
       def load_session(self, session_id: str) -> AgentSession: ...
       def list_sessions(self, status: str = None) -> list: ...

       def save_message(self, session_id: str, msg: ChatMessage) -> None: ...
       def get_messages(self, session_id: str) -> list[ChatMessage]: ...

       def save_task(self, task: TaskDB) -> None: ...
       def get_tasks(self, session_id: str) -> list[TaskDB]: ...

       def resume_session(self, session_id: str) -> AgentSession:
           """Reconstrói uma sessão completa a partir do DB."""
           session = self.load_session(session_id)
           session.messages = self.get_messages(session_id)
           session.tasks = self.get_tasks(session_id)
           return session
   ```
3. Criar endpoint `POST /api/sessions/resume/{session_id}`:
   - Carrega sessão do SQLite
   - Restaura contexto completo (messages, tasks, config)
   - Re-inicia agent loop com estado restaurado
4. Criar endpoint `GET /api/sessions`:
   - Lista sessões com filtros (status, agent_name, date_range)
5. Criar endpoint `GET /api/sessions/{id}/messages`:
   - Retorna histórico completo de mensagens
6. Docker volume mapping:
   - `./data:/app/data` no docker-compose
   - SQLite db persiste entre restarts do container
7. Auto-save:
   - Backend salva cada mensagem no DB em tempo real
   - Flush a cada 5 mensagens ou 30 segundos (batch insert)
8. Criar `tests/test_persistence.py`:
   - Teste save/load session roundtrip
   - Teste resume com messages e tasks
   - Teste list com filtros

**Entregável:** Backend persiste tudo em SQLite, sessions resumíveis.

**Critério de aceite:**
- `docker-compose down && docker-compose up` → sessões anteriores listáveis
- `POST /api/sessions/resume/{id}` → agente continua de onde parou
- `pytest tests/test_persistence.py` → passa
- DB file em `data/kuroko.db` contém tabelas corretas

---

### Sprint 8 — AGENTS.md Auto-Update & Graphiti Integration

**Objetivo:** Agentes aprendem e documentam padrões automaticamente.

**Tarefas:**

1. Criar `core/agents_md.py`:
   ```python
   class AgentsMDManager:
       """Gerencia AGENTS.md como knowledge base viva."""

       def __init__(self, path: str = "AGENTS.md"):
           self.path = path

       def read(self) -> str: ...
       def write(self, content: str) -> None: ...

       def append_pattern(self, section: str, pattern: str) -> None:
           """Adiciona um padrão aprendido a uma seção."""
           # Seções: ## Gotchas, ## Patterns, ## Architecture Decisions
           ...

       def append_gotcha(self, gotcha: str) -> None:
           """Registra um erro/problema encontrado para evitar repetição."""
           ...

       def update_task_history(self, task: str, result: str,
                               agent: str) -> None:
           """Registra resultado de tarefa para histórico."""
           ...
   ```
2. Criar `core/session_summary.py`:
   - Ao fim de cada sessão (ou a cada N mensagens):
     - LLM (modelo `cheap`) gera resumo da sessão
     - Extrai: decisões tomadas, padrões aprendidos, gotchas
     - Salva no SQLite + opcional no AGENTS.md
3. Criar `core/knowledge_store.py`:
   - Abstração sobre SQLite para knowledge base
   - Tabela `knowledge_entries`:
     - `id`, `category` (pattern|gotcha|decision|metric), `content`, `source_session_id`, `created_at`
   - Query por categoria, busca texto
   - Integração futura com Graphiti (graph-based memory) — stub interface agora
4. Injetar knowledge no system prompt:
   - Ao criar sessão, `AgentSession.__init__` lê AGENTS.md relevante
   - Injeta seções relevantes ao role do agente no system prompt
   - Max 2000 tokens de contexto de knowledge
5. Endpoint `GET /api/knowledge`:
   - Lista entradas de knowledge
   - Filtro por categoria
6. Endpoint `POST /api/knowledge`:
   - Adiciona entrada manual de knowledge
7. Criar `tests/test_agents_md.py`:
   - Teste append pattern
   - Teste append gotcha
   - Teste parse de AGENTS.md existente

**Entregável:** Agentes aprendem padrões e evitam erros repetidos.

**Critério de aceite:**
- Após sessão, AGENTS.md contém novos patterns/gotchas
- Knowledge entries salvos no SQLite
- System prompt inclui conhecimento relevante ao role
- `pytest tests/test_agents_md.py` → passa

---

### ═══════════════════════════════════════════
### FASE C — ARQUITETURA DE AGENTES (Sprints 9–11)
### ═══════════════════════════════════════════

---

### Sprint 9 — Agent Teams & PO Delegation

**Objetivo:** Implementar hierarquia de agentes com PO delegando sub-times.

**Tarefas:**

1. Criar `core/agent_team.py`:
   ```python
   from dataclasses import dataclass, field
   from enum import Enum

   class AgentRole(str, Enum):
       PO = "po"
       ARCHITECT = "architect"
       DEVELOPER = "developer"
       REVIEWER = "reviewer"
       TESTER = "tester"
       WRITER = "writer"
       DEVOPS = "devops"

   @dataclass
   class Agent:
       id: str
       name: str
       role: AgentRole
       model_profile: str  # via ModelRouter.resolve_model()
       system_prompt: str
       status: str = "idle"  # idle, working, waiting, done
       current_task: str | None = None

   @dataclass
   class AgentTeam:
       id: str
       name: str
       po: Agent
       members: list[Agent] = field(default_factory=list)
       task_queue: list = field(default_factory=list)

       def assign_task(self, task_id: str, agent_id: str) -> None: ...
       def get_available_agents(self) -> list[Agent]: ...
       def get_agent_by_role(self, role: AgentRole) -> Agent | None: ...
   ```
2. Criar `core/orchestrator.py`:
   ```python
   class Orchestrator:
       """Orquestra agent teams e delegação de tarefas."""

       def __init__(self, team: AgentTeam, router: ModelRouter,
                    persistence: PersistenceManager):
           self.team = team
           self.router = router
           self.persistence = persistence

       async def process_user_request(self, request: str) -> None:
           """PO recebe request, decompõe em tasks, delega."""
           # 1. PO analisa request e gera task decomposition
           po_response = await self._ask_agent(
               self.team.po,
               f"Decompose this request into tasks: {request}"
           )
           tasks = self._parse_tasks(po_response)

           # 2. PO atribui tasks a agentes por role
           for task in tasks:
               agent = self.team.get_agent_by_role(task.required_role)
               if agent:
                   self.team.assign_task(task.id, agent.id)
                   await self._execute_task(agent, task)

       async def _ask_agent(self, agent: Agent, prompt: str) -> str:
           profile = self.router.resolve_model(agent.role.value)
           messages = [
               {"role": "system", "content": agent.system_prompt},
               {"role": "user", "content": prompt},
           ]
           return await self.router.chat(profile, messages)

       async def _execute_task(self, agent: Agent, task) -> None:
           agent.status = "working"
           agent.current_task = task.id
           # Execute e salva resultado
           result = await self._ask_agent(agent, task.description)
           task.status = "done"
           task.result = result
           agent.status = "idle"
           # Persistir
           self.persistence.save_task(task)
   ```
3. Criar `core/handoff.py`:
   ```python
   @dataclass
   class Handoff:
       from_agent: str
       to_agent: str
       context: str  # Resumo do trabalho feito
       artifacts: list[str]  # Arquivos criados/modificados
       pending_questions: list[str]

   class HandoffManager:
       def create_handoff(self, from_a: Agent, to_a: Agent,
                          session: AgentSession) -> Handoff: ...
       def apply_handoff(self, handoff: Handoff,
                         target_session: AgentSession) -> None: ...
   ```
4. Endpoints:
   - `POST /api/teams` — criar team com agentes
   - `GET /api/teams/{id}` — detalhes do team
   - `POST /api/teams/{id}/tasks` — submeter tarefa ao PO
   - `GET /api/teams/{id}/status` — status de todos os agentes
5. Frontend updates (ainda com Tailwind — será migrado na Fase D):
   - Componente `TeamView` mostrando agentes e status
   - Componente `TaskBoard` (Kanban) com tarefas e atribuições
6. Criar `tests/test_orchestrator.py`:
   - Teste decomposição de task pelo PO
   - Teste atribuição por role
   - Teste handoff entre agentes

**Entregável:** PO recebe requests, decompõe e delega a sub-agentes.

**Critério de aceite:**
- `POST /api/teams/{id}/tasks` → PO decompõe e atribui
- Cada agente usa modelo adequado ao role
- Handoff inclui contexto e artefatos
- `pytest tests/test_orchestrator.py` → passa

---

### Sprint 10 — Dynamic Agent Spawning

**Objetivo:** PO pode criar novos agentes sob demanda conforme a complexidade da tarefa.

**Tarefas:**

1. Atualizar `core/orchestrator.py`:
   ```python
   class Orchestrator:
       async def spawn_agent(self, role: AgentRole, task: Task) -> Agent:
           """PO decide que precisa de mais um agente."""
           agent = Agent(
               id=str(uuid4()),
               name=f"{role.value}-{task.id[:8]}",
               role=role,
               model_profile=self.router.resolve_model(role.value),
               system_prompt=self._generate_system_prompt(role, task),
           )
           self.team.members.append(agent)
           # Criar sessão no DB
           self.persistence.save_session(AgentSession(
               id=agent.id,
               agent_name=agent.name,
               model=agent.model_profile,
               profile=agent.model_profile,
               system_prompt=agent.system_prompt,
           ))
           return agent

       def _generate_system_prompt(self, role: AgentRole,
                                    task: Task) -> str:
           """Gera system prompt baseado no role e task."""
           base_prompts = {
               AgentRole.DEVELOPER: "You are a senior developer...",
               AgentRole.REVIEWER: "You are a code reviewer...",
               AgentRole.TESTER: "You are a QA engineer...",
               # ...
           }
           prompt = base_prompts.get(role, "You are a helpful assistant.")
           # Injetar knowledge relevante do AGENTS.md
           knowledge = self.knowledge_store.get_relevant(
               role.value, max_tokens=1000
           )
           return f"{prompt}\n\n## Knowledge Base\n{knowledge}"
   ```
2. Regras de spawning:
   - Max agentes simultâneos: configurável (default 5)
   - Budget check antes de spawn (via CostTracker)
   - Auto-cleanup: agentes idle > 5 min são removidos
3. Lifecycle management:
   ```python
   class AgentLifecycle:
       IDLE_TIMEOUT = 300  # 5 min
       MAX_AGENTS = int(os.getenv("MAX_AGENTS", "5"))

       async def cleanup_idle(self, team: AgentTeam) -> list[str]:
           """Remove agentes idle por mais de IDLE_TIMEOUT."""
           removed = []
           for agent in team.members:
               if agent.status == "idle" and agent.idle_since:
                   if (now() - agent.idle_since).seconds > self.IDLE_TIMEOUT:
                       team.members.remove(agent)
                       removed.append(agent.id)
           return removed
   ```
4. WebSocket events para spawn/despawn:
   - `agent:spawned` → frontend adiciona agente ao board
   - `agent:despawned` → frontend remove
   - `agent:status_changed` → frontend atualiza
5. Criar `tests/test_spawn.py`:
   - Teste spawn cria agente com role correto
   - Teste max agents limit
   - Teste cleanup idle
   - Teste budget check before spawn

**Entregável:** Equipe de agentes escala dinamicamente.

**Critério de aceite:**
- PO spawna developer quando recebe task de código
- Max 5 agentes simultâneos (default)
- Agentes idle são removidos após 5min
- WebSocket notifica frontend de spawn/despawn

---

### Sprint 11 — Self-Improvement & AGENTS.md Feedback Loop

**Objetivo:** Agentes registram aprendizados e melhoram iterativamente.

**Tarefas:**

1. Criar `core/self_improve.py`:
   ```python
   class SelfImprover:
       """Analisa resultados de tarefas e gera melhorias."""

       def __init__(self, llm: LLMClient, knowledge: KnowledgeStore,
                    agents_md: AgentsMDManager):
           self.llm = llm
           self.knowledge = knowledge
           self.agents_md = agents_md

       async def analyze_session(self, session: AgentSession) -> dict:
           """Após sessão, extrai aprendizados."""
           summary_prompt = f"""
           Analyze this agent session and extract:
           1. Patterns: reusable approaches that worked
           2. Gotchas: mistakes or issues to avoid
           3. Decisions: architectural decisions made and why
           4. Metrics: time spent, tokens used, success rate

           Session messages:
           {self._format_messages(session.messages[-50:])}
           """
           analysis = self.llm.chat([
               {"role": "system", "content": "You are a meta-analyst..."},
               {"role": "user", "content": summary_prompt},
           ])
           # Parse structured output
           return self._parse_analysis(analysis)

       async def apply_learnings(self, analysis: dict) -> None:
           """Salva aprendizados no knowledge store e AGENTS.md."""
           for pattern in analysis.get("patterns", []):
               self.knowledge.add("pattern", pattern)
               self.agents_md.append_pattern("Patterns", pattern)
           for gotcha in analysis.get("gotchas", []):
               self.knowledge.add("gotcha", gotcha)
               self.agents_md.append_gotcha(gotcha)
   ```
2. Hook no `Orchestrator`:
   - Após cada task concluída: `SelfImprover.analyze_session()`
   - Usar modelo `cheap` para a análise (economia)
3. Quality metrics per agent:
   ```python
   @dataclass
   class AgentMetrics:
       agent_id: str
       tasks_completed: int = 0
       tasks_failed: int = 0
       avg_tokens_per_task: float = 0
       avg_cost_per_task: float = 0
       patterns_contributed: int = 0
       gotchas_contributed: int = 0

       @property
       def success_rate(self) -> float:
           total = self.tasks_completed + self.tasks_failed
           return self.tasks_completed / total if total > 0 else 0
   ```
4. Endpoint `GET /api/agents/{id}/metrics`:
   - Retorna métricas do agente
5. Criar dashboard widget (frontend, ainda Tailwind):
   - Agent performance cards
   - Recent learnings feed
6. Criar `tests/test_self_improve.py`:
   - Teste análise gera patterns e gotchas
   - Teste apply_learnings salva no DB
   - Teste métricas calculadas corretamente

**Entregável:** Agentes melhoram performance iterativamente.

**Critério de aceite:**
- Após 3+ tasks, AGENTS.md contém novos patterns
- Métricas por agente acessíveis via API
- Modelo `cheap` usado para análise (verificar cost tracker)
- `pytest tests/test_self_improve.py` → passa

---

### ═══════════════════════════════════════════
### FASE D — MIGRAÇÃO FRONTEND MUI v6 (Sprints 12–16)
### ═══════════════════════════════════════════

> **PRINCÍPIO:** Tailwind é removido **inteiramente**. Nenhuma classe utilitária
> `bg-*`, `text-*`, `flex`, `p-*`, `m-*` sobrevive no código final.
> Todo styling via MUI `sx` prop, `styled()`, ou theme tokens.

---

### Sprint 12 — MUI v6 Setup & ThemeProvider

**Objetivo:** Instalar MUI, criar ThemeProvider com 7 temas, garantir coexistência temporária com Tailwind.

**Tarefas:**

1. Instalar dependências:
   ```bash
   npm install @mui/material @mui/icons-material @emotion/react @emotion/styled
   npm install @mui/joy  # Joy UI para componentes adicionais
   ```
2. Criar `apps/frontend/src/theme/`:
   ```
   theme/
   ├── index.ts          # createTheme + ThemeProvider wrapper
   ├── palette.ts        # 7 palettes do Auto-Claude original
   ├── typography.ts     # Font config (JetBrains Mono para code)
   ├── components.ts     # Component overrides globais
   └── shadows.ts        # Shadow tokens
   ```
3. Criar as 7 palettes (baseadas nos temas originais do Auto-Claude):
   ```typescript
   // palette.ts
   export const palettes = {
     dark: {
       mode: 'dark',
       primary: { main: '#6366f1' },     // Indigo
       secondary: { main: '#8b5cf6' },   // Violet
       background: { default: '#0f0f23', paper: '#1a1a2e' },
       text: { primary: '#e2e8f0' },
     },
     midnight: { /* ... */ },
     cyberpunk: { /* ... */ },
     forest: { /* ... */ },
     ocean: { /* ... */ },
     sunset: { /* ... */ },
     monochrome: { /* ... */ },
   };
   ```
4. Criar `ThemeProvider` wrapper:
   ```typescript
   // theme/index.ts
   import { createTheme, ThemeProvider as MUIProvider } from '@mui/material';
   import CssBaseline from '@mui/material/CssBaseline';

   export function KurokoThemeProvider({ children }: { children: React.ReactNode }) {
     const { theme: themeName } = useSettingsStore();
     const muiTheme = createTheme({
       palette: palettes[themeName] || palettes.dark,
       typography: typographyConfig,
       components: componentOverrides,
       shape: { borderRadius: 8 },
     });

     return (
       <MUIProvider theme={muiTheme}>
         <CssBaseline />
         {children}
       </MUIProvider>
     );
   }
   ```
5. Adicionar `KurokoThemeProvider` no `App.tsx` (sem remover Tailwind ainda)
6. Verificar que MUI + Tailwind coexistem sem conflitos visuais
7. Criar `apps/frontend/src/theme/README.md`:
   - Documentar cada palette
   - Guia: "Como usar sx prop em vez de className Tailwind"
   - Exemplos de migração: `className="bg-gray-800 p-4"` → `sx={{ bgcolor: 'background.paper', p: 2 }}`

**Entregável:** ThemeProvider funcional com 7 temas, MUI instalado.

**Critério de aceite:**
- `npm run build` → sem erros
- Toggle de tema funciona (dark ↔ midnight ↔ cyberpunk ...)
- CssBaseline aplica reset global
- MUI components renderizam corretamente

---

### Sprint 13 — Migração de Layout & Navigation

**Objetivo:** Migrar layout principal (sidebar, header, content area) de Tailwind para MUI.

**Tarefas:**

1. Migrar **Sidebar** (`Sidebar.tsx`):
   - `className="flex flex-col bg-gray-900 w-64"` → MUI `Drawer` component
   ```typescript
   import { Drawer, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';

   export function Sidebar() {
     return (
       <Drawer
         variant="permanent"
         sx={{
           width: 256,
           '& .MuiDrawer-paper': {
             width: 256,
             bgcolor: 'background.paper',
             borderRight: 1,
             borderColor: 'divider',
           },
         }}
       >
         <List>
           {/* menu items */}
         </List>
       </Drawer>
     );
   }
   ```
2. Migrar **Header** (`Header.tsx`):
   - MUI `AppBar` + `Toolbar`
   - Theme switcher usando `IconButton` + `Menu`
3. Migrar **Content Area**:
   - MUI `Box` com `sx` prop
   - Grid layout via MUI `Grid2` (v6)
4. Migrar **Tabs/Navigation**:
   - MUI `Tabs` + `Tab` components
5. Remover todas as classes Tailwind dos componentes migrados
6. Verificar responsividade com MUI breakpoints

**Entregável:** Layout shell inteiro em MUI.

**Critério de aceite:**
- Layout idêntico ou melhor que o original
- 0 classes Tailwind nos componentes migrados
- Responsive em desktop (Electron window resize)

---

### Sprint 14 — Migração de Componentes Core

**Objetivo:** Migrar os componentes principais do app: Chat, Terminal, Kanban, Modals.

**Tarefas:**

1. **Chat** (`ChatView.tsx`, `MessageBubble.tsx`):
   - Input → MUI `TextField` com `multiline`
   - Message bubbles → MUI `Paper` + `Typography`
   - Code blocks → MUI `Paper` com `sx={{ fontFamily: 'monospace' }}`
   - Streaming indicator → MUI `LinearProgress` ou `CircularProgress`
   ```typescript
   <Paper
     elevation={0}
     sx={{
       p: 2,
       mb: 1,
       bgcolor: isUser ? 'primary.dark' : 'background.paper',
       borderRadius: 2,
       maxWidth: '80%',
       alignSelf: isUser ? 'flex-end' : 'flex-start',
     }}
   >
     <Typography variant="body1">{message.content}</Typography>
   </Paper>
   ```
2. **Terminal** (`TerminalView.tsx`):
   - Container → MUI `Paper` com `bgcolor: '#000'`
   - xterm.js integration mantida (não é Tailwind)
   - Toolbar → MUI `Toolbar` com `IconButton`s
3. **Kanban Board** (`KanbanBoard.tsx`, `KanbanColumn.tsx`, `KanbanCard.tsx`):
   - Columns → MUI `Paper` com drag-and-drop
   - Cards → MUI `Card` + `CardContent` + `Chip` para tags
   - Drag handle → MUI `IconButton` com `DragIndicator` icon
   ```typescript
   <Card
     sx={{
       mb: 1,
       cursor: 'grab',
       '&:hover': { boxShadow: 4 },
       transition: 'box-shadow 0.2s',
     }}
   >
     <CardContent>
       <Typography variant="subtitle2">{task.title}</Typography>
       <Stack direction="row" spacing={0.5} mt={1}>
         <Chip label={task.status} size="small" color="primary" />
         <Chip label={task.agent} size="small" variant="outlined" />
       </Stack>
     </CardContent>
   </Card>
   ```
4. **Modals** (`CreateProjectModal.tsx`, `SettingsModal.tsx`, etc.):
   - MUI `Dialog` + `DialogTitle` + `DialogContent` + `DialogActions`
   - Form fields → MUI `TextField`, `Select`, `Switch`
   - Confirmation dialogs → MUI `Dialog` com `Button` actions
5. **Notifications/Toasts**:
   - MUI `Snackbar` + `Alert`
6. Remover todas as classes Tailwind dos componentes migrados

**Entregável:** Todos os componentes core em MUI.

**Critério de aceite:**
- Chat, Terminal, Kanban, Modals renderizam corretamente
- 0 classes Tailwind nos componentes migrados
- Temas aplicam corretamente em todos os componentes

---

### Sprint 15 — Migração de Componentes Auxiliares & Forms

**Objetivo:** Migrar componentes menores: forms, settings, agent cards, status badges.

**Tarefas:**

1. **Agent Cards** (`AgentCard.tsx`):
   - MUI `Card` com `Avatar`, `CardHeader`, `CardContent`
   - Status badge → MUI `Badge` com cor por status
   - Metrics → MUI `LinearProgress` para success rate
2. **Settings Panel** (`SettingsPanel.tsx`):
   - MUI `Accordion` para seções
   - Toggle settings → MUI `Switch` + `FormControlLabel`
   - API key input → MUI `TextField` type="password"
   - Model selector → MUI `Select` com `MenuItem`
3. **Project Setup** (`ProjectSetup.tsx`):
   - Stepper → MUI `Stepper` + `Step` + `StepLabel`
   - File picker → MUI `Button` + hidden input
4. **Tables** (se houver):
   - MUI `Table` + `TableHead` + `TableBody` + `TableCell`
   - Sorting/filtering via MUI `TableSortLabel`
5. **Tooltips** → MUI `Tooltip`
6. **Loading states** → MUI `Skeleton`
7. **Empty states** → MUI `Box` + `Typography` + ilustração
8. Busca completa por classes Tailwind remanescentes:
   ```bash
   grep -r "className=" --include="*.tsx" --include="*.ts" apps/frontend/src/
   ```
   - Migrar qualquer remanescente

**Entregável:** Todos os componentes migrados para MUI.

**Critério de aceite:**
- `grep -r "className=\"[^\"]*bg-\|className=\"[^\"]*text-\|className=\"[^\"]*flex\|className=\"[^\"]*p-\|className=\"[^\"]*m-" --include="*.tsx" --include="*.ts" apps/frontend/src/` → 0 resultados
- Todos os componentes renderizam com temas

---

### Sprint 16 — Remoção Total do Tailwind

**Objetivo:** Purgar Tailwind CSS do projeto inteiro. Nenhum vestígio.

**Tarefas:**

1. `npm uninstall tailwindcss @tailwindcss/vite autoprefixer` (ou equivalentes v4)
2. **Deletar** `tailwind.config.ts`
3. **Deletar** `postcss.config.js` (ou remover Tailwind dele se PostCSS ainda necessário)
4. Remover `@tailwind` directives de qualquer CSS:
   ```css
   /* REMOVER: */
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```
5. Remover import do Tailwind CSS no entry point (`main.tsx` ou `index.css`)
6. Atualizar `electron.vite.config.ts`:
   - Remover Tailwind plugin (se presente)
7. Busca final — nenhuma classe Tailwind:
   ```bash
   # Classes Tailwind comuns
   grep -rn "bg-\|text-\|flex \|flex-\|grid \|grid-\|p-\|px-\|py-\|m-\|mx-\|my-\|w-\|h-\|min-\|max-\|border-\|rounded-\|shadow-\|hover:\|focus:\|dark:\|sm:\|md:\|lg:" \
     --include="*.tsx" --include="*.ts" --include="*.css" \
     apps/frontend/src/
   ```
   - Se algum resultado: migrar para MUI `sx`
8. Busca por `className=` residual:
   - `className` com strings de Tailwind → converter para `sx`
   - `className` para CSS modules/custom classes → aceitar (não é Tailwind)
9. `npm run build` → verificar que builda sem erros
10. Visual check: todos os temas funcion corretos

**Entregável:** Tailwind completamente removido.

**Critério de aceite:**
- `tailwindcss` não aparece em `package.json`
- `tailwind.config.ts` e `postcss.config.js` deletados
- `grep -r "tailwind\|@tailwind" --include="*.ts" --include="*.tsx" --include="*.css" --include="*.json"` → 0
- `npm run build` → sem erros
- App renderiza corretamente com todos 7 temas

**Fallback:** Se MUI v6 causar conflitos extremos com algum componente específico:
- Considerar Shadcn UI **somente** como componente individual, não como framework
- Documentar razão no AGENTS.md
- **Jamais** reintroduzir Tailwind

---

### ═══════════════════════════════════════════
### FASE E — SEGURANÇA & DEVOPS (Sprints 17–19)
### ═══════════════════════════════════════════

---

### Sprint 17 — Audit Logging

**Objetivo:** Toda ação de agente (FS, shell, rede) é logada em audit trail persistente.

**Tarefas:**

1. Criar `core/audit.py`:
   ```python
   from dataclasses import dataclass
   from datetime import datetime
   from enum import Enum
   import json, os

   class AuditAction(str, Enum):
       FILE_READ = "file:read"
       FILE_WRITE = "file:write"
       FILE_DELETE = "file:delete"
       SHELL_EXEC = "shell:exec"
       NET_REQUEST = "net:request"
       LLM_CALL = "llm:call"
       AGENT_SPAWN = "agent:spawn"
       AGENT_DESPAWN = "agent:despawn"
       CONFIG_CHANGE = "config:change"

   @dataclass
   class AuditEntry:
       timestamp: str
       action: AuditAction
       agent_id: str
       agent_name: str
       details: dict  # action-specific data
       session_id: str
       approved: bool = True  # se passou pelo allowlist

   class AuditLogger:
       def __init__(self, log_dir: str = "/data/audit"):
           self.log_dir = log_dir
           os.makedirs(log_dir, exist_ok=True)

       def log(self, entry: AuditEntry) -> None:
           """Append entry to daily log file."""
           date = datetime.utcnow().strftime("%Y-%m-%d")
           path = os.path.join(self.log_dir, f"audit-{date}.jsonl")
           with open(path, "a") as f:
               f.write(json.dumps(entry.__dict__) + "\n")

       def query(self, agent_id: str = None,
                 action: AuditAction = None,
                 since: str = None) -> list[AuditEntry]: ...
   ```
2. Integrar AuditLogger em:
   - `LLMClient.chat()` → loga `LLM_CALL` com model, tokens, cost
   - `Orchestrator.spawn_agent()` → loga `AGENT_SPAWN`
   - Qualquer tool execution → loga `SHELL_EXEC`, `FILE_READ/WRITE`
3. Docker volume para audit logs:
   ```yaml
   # docker-compose.yml
   volumes:
     - ./data/audit:/data/audit
   ```
4. Endpoint `GET /api/audit`:
   - Query logs com filtros (agent, action, date range)
   - Paginação
5. Criar `tests/test_audit.py`:
   - Teste log cria arquivo JSONL
   - Teste query com filtros
   - Teste file rotation por dia

**Entregável:** Audit trail completo de todas as ações.

**Critério de aceite:**
- Toda chamada LLM gera entry em `/data/audit/audit-YYYY-MM-DD.jsonl`
- Spawn/despawn de agentes logado
- `GET /api/audit` retorna entries filtráveis
- Logs persistem entre restarts (Docker volume)

---

### Sprint 18 — Allowlist & Permission System

**Objetivo:** Controle granular de o que agentes podem acessar (FS paths, comandos shell, URLs).

**Tarefas:**

1. Criar `core/allowlist.py`:
   ```python
   from dataclasses import dataclass, field
   import fnmatch, re

   @dataclass
   class AllowlistConfig:
       # File system
       allowed_paths: list[str] = field(default_factory=lambda: [
           "/workspace/**",
       ])
       denied_paths: list[str] = field(default_factory=lambda: [
           "/etc/**", "/root/**", "/proc/**", "/sys/**",
           "**/.env", "**/*.key", "**/*.pem",
       ])
       # Shell commands
       allowed_commands: list[str] = field(default_factory=lambda: [
           "ls", "cat", "grep", "find", "echo", "mkdir", "cp", "mv",
           "git *", "npm *", "node *", "python *", "pip *",
       ])
       denied_commands: list[str] = field(default_factory=lambda: [
           "rm -rf /", "sudo *", "chmod 777 *", "curl * | sh",
           "wget * | sh", "dd *",
       ])
       # Network
       allowed_urls: list[str] = field(default_factory=lambda: [
           "https://openrouter.ai/**",
           "https://api.github.com/**",
           "https://registry.npmjs.org/**",
           "https://pypi.org/**",
       ])

   class AllowlistChecker:
       def __init__(self, config: AllowlistConfig):
           self.config = config

       def check_path(self, path: str) -> bool:
           for denied in self.config.denied_paths:
               if fnmatch.fnmatch(path, denied):
                   return False
           for allowed in self.config.allowed_paths:
               if fnmatch.fnmatch(path, allowed):
                   return True
           return False  # default deny

       def check_command(self, cmd: str) -> bool: ...
       def check_url(self, url: str) -> bool: ...
   ```
2. Middleware no backend:
   - Todo file access passa por `AllowlistChecker.check_path()`
   - Todo shell exec passa por `AllowlistChecker.check_command()`
   - Blocked actions logadas no audit com `approved=False`
3. Frontend UI para allowlist:
   - Settings → Security tab
   - Editar allowed/denied paths, commands, URLs
   - MUI `List` com `TextField` para add/edit + `IconButton` delete
   - Presets: "Permissive", "Moderate", "Strict"
4. Endpoint `GET/PUT /api/settings/allowlist`:
   - Read/update allowlist config
   - Salva em `data/allowlist.json`
5. Criar `tests/test_allowlist.py`:
   - Teste path checking (allowed, denied, default deny)
   - Teste command checking
   - Teste URL checking

**Entregável:** Agentes limitados a ações permitidas.

**Critério de aceite:**
- Agente tentando acessar `/etc/passwd` → bloqueado + audit log
- Agente tentando `rm -rf /` → bloqueado + audit log
- UI permite editar allowlist
- `pytest tests/test_allowlist.py` → passa

---

### Sprint 19 — Docker-in-Docker Sandbox (Opcional)

**Objetivo:** Agentes executam comandos em container isolado (sandbox).

**Tarefas:**

1. Criar `core/sandbox.py`:
   ```python
   import docker
   import os

   class DockerSandbox:
       """Executa comandos de agentes em container isolado."""

       def __init__(self):
           self.docker = docker.from_env()
           self.image = os.getenv("SANDBOX_IMAGE", "python:3.12-slim")
           self.workspace = os.getenv("SANDBOX_WORKSPACE", "/workspace")

       def exec(self, command: str, timeout: int = 30) -> tuple[str, int]:
           """Executa comando no sandbox e retorna (output, exit_code)."""
           container = self.docker.containers.run(
               self.image,
               command=f"bash -c '{command}'",
               volumes={
                   self.workspace: {"bind": "/workspace", "mode": "rw"},
               },
               network_mode="none",  # sem acesso à rede
               mem_limit="512m",
               cpu_period=100000,
               cpu_quota=50000,  # 50% CPU
               detach=True,
               remove=False,
           )
           try:
               result = container.wait(timeout=timeout)
               output = container.logs().decode()
               return output, result["StatusCode"]
           finally:
               container.remove(force=True)
   ```
2. Config flag `SANDBOX_ENABLED=true/false`:
   - Se `true`: todos os `SHELL_EXEC` passam pelo sandbox
   - Se `false`: execução direta (default para dev)
3. Docker-compose service:
   ```yaml
   services:
     sandbox:
       image: docker:dind
       privileged: true
       volumes:
         - /var/run/docker.sock:/var/run/docker.sock
         - ./workspace:/workspace
   ```
4. Frontend toggle em Settings → Security:
   - "Enable sandbox execution" switch
5. Criar `tests/test_sandbox.py`:
   - Teste exec com comando simples
   - Teste timeout
   - Teste sem acesso à rede

**Entregável:** Sandbox Docker opcional para execução isolada.

**Critério de aceite:**
- `SANDBOX_ENABLED=true` → comandos rodam em container isolado
- Container sem rede (`network_mode=none`)
- Timeout funciona
- `SANDBOX_ENABLED=false` → execução direta (fallback)

---

### ═══════════════════════════════════════════
### FASE F — UX POLISH & INTEGRAÇÃO (Sprints 20–23)
### ═══════════════════════════════════════════

---

### Sprint 20 — Docker Setup Wizard

**Objetivo:** First-run wizard que configura tudo: API key, git mount, model selection.

**Tarefas:**

1. Criar `apps/frontend/src/components/SetupWizard.tsx`:
   ```typescript
   import { Stepper, Step, StepLabel, TextField, Button, Box } from '@mui/material';

   const steps = [
     'API Key',
     'Workspace',
     'Model Selection',
     'Verify',
   ];

   export function SetupWizard() {
     const [activeStep, setActiveStep] = useState(0);

     return (
       <Box sx={{ maxWidth: 600, mx: 'auto', mt: 8 }}>
         <Stepper activeStep={activeStep}>
           {steps.map((label) => (
             <Step key={label}>
               <StepLabel>{label}</StepLabel>
             </Step>
           ))}
         </Stepper>

         {activeStep === 0 && <ApiKeyStep />}
         {activeStep === 1 && <WorkspaceStep />}
         {activeStep === 2 && <ModelStep />}
         {activeStep === 3 && <VerifyStep />}
       </Box>
     );
   }
   ```
2. **Step 1 — API Key:**
   - Input para OpenRouter API key
   - Botão "Validate" → chama backend
   - Mostra saldo/créditos do OpenRouter (se API disponível)
3. **Step 2 — Workspace:**
   - Seletor de diretório para montar no Docker
   - Preview dos arquivos no diretório
   - Gera `docker-compose.yml` com volume correto
4. **Step 3 — Model Selection:**
   - Lista de modelos disponíveis no OpenRouter
   - Preset profiles (Smart, Cheap, Coding, Fast)
   - Cost estimate por profile
5. **Step 4 — Verify:**
   - Resumo de configuração
   - Teste de conexão
   - "Start" → salva `.env` + inicia containers
6. Detectar first-run:
   - Se `.env` não existe ou API key não validada → mostra wizard
   - Se já configurado → pula para dashboard

**Entregável:** Setup zero-friction para novos usuários.

**Critério de aceite:**
- First run → wizard aparece
- Wizard gera `.env` funcional
- Após wizard, app funciona sem configuração adicional
- Re-run → pula wizard, vai direto ao dashboard

---

### Sprint 21 — Webhook Notifications (Telegram/Slack)

**Objetivo:** PO envia updates de progresso via Telegram e/ou Slack.

**Tarefas:**

1. Criar `core/webhooks.py`:
   ```python
   import httpx
   import os
   from typing import Protocol

   class WebhookProvider(Protocol):
       async def send(self, message: str) -> bool: ...

   class TelegramWebhook:
       def __init__(self):
           self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
           self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

       async def send(self, message: str) -> bool:
           if not self.bot_token or not self.chat_id:
               return False
           async with httpx.AsyncClient() as client:
               r = await client.post(
                   f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
                   json={"chat_id": self.chat_id, "text": message,
                          "parse_mode": "Markdown"},
               )
               return r.status_code == 200

   class SlackWebhook:
       def __init__(self):
           self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

       async def send(self, message: str) -> bool:
           if not self.webhook_url:
               return False
           async with httpx.AsyncClient() as client:
               r = await client.post(
                   self.webhook_url,
                   json={"text": message},
               )
               return r.status_code == 200

   class WebhookManager:
       def __init__(self):
           self.providers: list[WebhookProvider] = []
           if os.getenv("TELEGRAM_BOT_TOKEN"):
               self.providers.append(TelegramWebhook())
           if os.getenv("SLACK_WEBHOOK_URL"):
               self.providers.append(SlackWebhook())

       async def notify(self, event: str, details: str) -> None:
           message = f"🤖 *kuroko-ops* | {event}\n{details}"
           for provider in self.providers:
               await provider.send(message)
   ```
2. Eventos que disparam notificação:
   - Task concluída pelo PO
   - Sprint finalizada
   - Budget 80%/100% atingido
   - Erro crítico de agente
   - Build success/failure
3. `.env.example` atualizar com:
   ```env
   TELEGRAM_BOT_TOKEN=
   TELEGRAM_CHAT_ID=
   SLACK_WEBHOOK_URL=
   ```
4. Settings UI:
   - Webhook configuration section
   - Test button → envia mensagem de teste
   - Toggle por tipo de evento
5. Criar `tests/test_webhooks.py`:
   - Teste Telegram com mock httpx
   - Teste Slack com mock httpx
   - Teste WebhookManager com múltiplos providers

**Entregável:** Notificações automáticas via Telegram/Slack.

**Critério de aceite:**
- Task concluída → mensagem no Telegram (se configurado)
- Budget alert → mensagem no Slack (se configurado)
- Sem providers configurados → no-op (sem erros)
- `pytest tests/test_webhooks.py` → passa

---

### Sprint 22 — Bug Fixes & Edge Cases

**Objetivo:** Corrigir bugs conhecidos do upstream e edge cases da migração.

**Tarefas:**

1. **Bug: Tarefas ficando stuck ("in_progress" infinito)**
   - Adicionar timeout por task (default 10 min)
   - Task timeout → status `failed` + notify PO
   - PO pode retry ou reassign
   ```python
   class TaskWatchdog:
       TASK_TIMEOUT = int(os.getenv("TASK_TIMEOUT_SECONDS", "600"))

       async def check_stuck_tasks(self, team: AgentTeam) -> list[Task]:
           stuck = []
           for task in team.task_queue:
               if task.status == "in_progress":
                   elapsed = (now() - task.started_at).seconds
                   if elapsed > self.TASK_TIMEOUT:
                       task.status = "failed"
                       task.error = "Timeout exceeded"
                       stuck.append(task)
           return stuck
   ```
2. **Bug: spec.md não gerado em novos projetos**
   - Ao criar projeto, template de `spec.md` gerado automaticamente
   - PO popula spec via prompt de discovery
3. **Bug: Roadmap não renderiza no frontend**
   - Verificar parsing de Markdown no componente Roadmap
   - Garantir que `react-markdown` (ou alternativa MUI) renderiza corretamente
   - Substituir por MUI `Typography` + custom renderer se necessário
4. **Edge case: WebSocket disconnect durante streaming**
   - Auto-reconnect com exponential backoff
   - Mensagens parciais salvas no DB (persistence)
   - Resume do ponto exato após reconnect
5. **Edge case: Model indisponível no OpenRouter**
   - Fallback automático via LiteLLM Router
   - Notificação ao usuário sobre fallback
6. **Edge case: Concurrent agent writes ao mesmo arquivo**
   - File locking via `fcntl` ou equivalent
   - Queue de file operations por path

**Entregável:** App mais estável e resiliente.

**Critério de aceite:**
- Tasks com timeout não ficam stuck
- Novo projeto gera spec.md
- Roadmap renderiza corretamente
- WebSocket reconnect funciona

---

### Sprint 23 — Docker-Compose Production Setup

**Objetivo:** `docker-compose up` funcional para deploy.

**Tarefas:**

1. Finalizar `Dockerfile.backend`:
   ```dockerfile
   FROM python:3.12-slim

   WORKDIR /app

   COPY pyproject.toml .
   RUN pip install --no-cache-dir .

   COPY core/ core/
   COPY apps/backend/ apps/backend/

   EXPOSE 8000

   CMD ["uvicorn", "core.server:app", "--host", "0.0.0.0", "--port", "8000"]
   ```
2. Finalizar `Dockerfile.frontend`:
   ```dockerfile
   FROM node:20-slim AS builder

   WORKDIR /app

   COPY package.json package-lock.json ./
   RUN npm ci

   COPY apps/frontend/ apps/frontend/
   COPY electron.vite.config.ts .
   RUN npm run build

   FROM electronuserland/builder:wine
   # Electron packaging
   ```
3. Finalizar `docker-compose.yml`:
   ```yaml
   version: '3.8'

   services:
     backend:
       build:
         context: .
         dockerfile: Dockerfile.backend
       ports:
         - "8000:8000"
       env_file: .env
       volumes:
         - ./data:/app/data
         - ./data/audit:/data/audit
         - ${WORKSPACE_PATH:-.}:/workspace:rw
       restart: unless-stopped

     frontend:
       build:
         context: .
         dockerfile: Dockerfile.frontend
       depends_on:
         - backend
       ports:
         - "3000:3000"
       environment:
         - VITE_API_URL=http://backend:8000

   volumes:
     data:
   ```
4. Health checks:
   ```yaml
   healthcheck:
     test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
     interval: 30s
     timeout: 10s
     retries: 3
   ```
5. `.dockerignore`:
   ```
   node_modules
   __pycache__
   .env
   data/
   .git
   *.db
   ```
6. `Makefile` ou scripts:
   ```makefile
   up:
       docker-compose up -d --build
   down:
       docker-compose down
   logs:
       docker-compose logs -f
   reset:
       docker-compose down -v
       rm -rf data/
   ```
7. Testar:
   - `docker-compose up --build` → inicia sem erros
   - Backend health check → 200
   - Frontend acessível em `http://localhost:3000`
   - WebSocket funciona entre containers
   - Data persiste após restart

**Entregável:** Deploy via `docker-compose up` funcional.

**Critério de aceite:**
- `docker-compose up --build` → 0 erros
- `curl http://localhost:8000/health` → 200
- Frontend renderiza e conecta ao backend
- Restart mantém dados (SQLite + audit logs)

---

### ═══════════════════════════════════════════
### FASE G — TESTING & RELEASE (Sprints 24–26)
### ═══════════════════════════════════════════

---

### Sprint 24 — Testes Unitários Completos

**Objetivo:** Coverage >80% em todos os módulos core.

**Tarefas:**

1. Completar testes para todos os módulos:
   | Módulo | Arquivo de teste | Prioridade |
   |--------|-----------------|------------|
   | `core/llm_client.py` | `tests/test_llm_client.py` | Alta |
   | `core/router.py` | `tests/test_router.py` | Alta |
   | `core/database.py` | `tests/test_database.py` | Alta |
   | `core/persistence.py` | `tests/test_persistence.py` | Alta |
   | `core/orchestrator.py` | `tests/test_orchestrator.py` | Alta |
   | `core/agent_team.py` | `tests/test_agent_team.py` | Média |
   | `core/handoff.py` | `tests/test_handoff.py` | Média |
   | `core/audit.py` | `tests/test_audit.py` | Média |
   | `core/allowlist.py` | `tests/test_allowlist.py` | Média |
   | `core/sandbox.py` | `tests/test_sandbox.py` | Baixa |
   | `core/webhooks.py` | `tests/test_webhooks.py` | Baixa |
   | `core/cost_tracker.py` | `tests/test_cost_tracker.py` | Alta |
   | `core/self_improve.py` | `tests/test_self_improve.py` | Média |
   | `core/agents_md.py` | `tests/test_agents_md.py` | Baixa |
2. Frontend tests (Vitest):
   - Store tests: auth, agent, project, session, settings
   - Component tests: SetupWizard, ChatView, KanbanBoard
   - Theme tests: todas 7 palettes renderizam
3. Configurar `pytest.ini`:
   ```ini
   [pytest]
   testpaths = tests
   asyncio_mode = auto
   ```
4. Configurar coverage:
   ```bash
   pytest --cov=core --cov-report=html --cov-report=term-missing
   ```
5. CI check:
   - `pytest` → passa
   - Coverage > 80%
   - `npm run test` → passa

**Entregável:** Test suite completo.

**Critério de aceite:**
- `pytest --cov=core` → >80% coverage
- `npm run test` → passa
- Nenhum teste flaky

---

### Sprint 25 — Testes E2E & Integração

**Objetivo:** Testes end-to-end do fluxo completo.

**Tarefas:**

1. Criar `tests/e2e/`:
   ```
   tests/e2e/
   ├── test_setup_wizard.py     # Wizard flow
   ├── test_chat_flow.py        # Send message → receive streaming
   ├── test_agent_team.py       # Create team → assign task → complete
   ├── test_persistence.py      # Send messages → restart → resume
   ├── test_cost_tracking.py    # Multiple calls → check costs
   ├── test_audit_trail.py      # Actions → check audit logs
   └── conftest.py              # Fixtures (test server, test DB)
   ```
2. E2E test flow:
   ```python
   async def test_full_workflow():
       # 1. Setup API key
       r = await client.post("/api/auth/validate", json={"key": test_key})
       assert r.status_code == 200

       # 2. Create team
       r = await client.post("/api/teams", json={...})
       team_id = r.json()["id"]

       # 3. Submit task
       r = await client.post(f"/api/teams/{team_id}/tasks",
                              json={"description": "Create a hello world"})
       task_id = r.json()["task_id"]

       # 4. Wait for completion
       while True:
           r = await client.get(f"/api/teams/{team_id}/status")
           if r.json()["tasks"][task_id]["status"] == "done":
               break
           await asyncio.sleep(1)

       # 5. Check audit trail
       r = await client.get("/api/audit")
       assert len(r.json()["entries"]) > 0

       # 6. Check costs
       r = await client.get("/api/costs")
       assert r.json()["total_cost"] > 0
   ```
3. Docker E2E:
   - `docker-compose -f docker-compose.test.yml up --build`
   - Roda testes contra containers reais
   - Limpa após execução
4. Frontend E2E (Playwright ou Cypress — sugestão Playwright):
   - Setup wizard flow
   - Chat send/receive
   - Theme switching
   - Settings modification

**Entregável:** E2E tests cobrindo fluxos críticos.

**Critério de aceite:**
- `pytest tests/e2e/` → passa (com test API key)
- Docker E2E → passa
- Playwright smoke test → passa

---

### Sprint 26 — Cleanup, Docs & Release v0.1.0

**Objetivo:** Limpar código, finalizar documentação, tag release.

**Tarefas:**

1. **Code cleanup:**
   - Remover TODOs de migração
   - Remover imports não usados
   - Formatar com `black` (Python) e `prettier` (TS)
   - Lint com `ruff` (Python) e `eslint` (TS)
2. **Verificação final de refs Claude:**
   ```bash
   grep -rni "claude\|anthropic" --include="*.py" --include="*.ts" \
     --include="*.tsx" --include="*.json" --include="*.yaml" \
     --exclude-dir=node_modules --exclude-dir=.git
   ```
   - Aceitar: nomes de modelo ("anthropic/claude-sonnet-4-20250514"), comentários de histórico
   - Rejeitar: imports, endpoints, classes, variáveis com nome Claude
3. **Verificação final de Tailwind:**
   ```bash
   grep -rni "tailwind\|@tailwind\|tw-" --include="*.ts" --include="*.tsx" \
     --include="*.css" --include="*.json"
   ```
   - Deve retornar 0 resultados
4. **README.md final** (ver Parte 3 abaixo)
5. **CHANGELOG.md:**
   ```markdown
   ## [0.1.0] - 2025-XX-XX

   ### Added
   - Multi-LLM support via OpenRouter (OpenAI SDK compatible)
   - LiteLLM routing with smart/cheap/coding/fast profiles
   - Agent teams with PO delegation and handoff
   - Dynamic agent spawning and lifecycle management
   - SQLite persistence with session resume
   - AGENTS.md auto-update with learned patterns
   - MUI v6 UI with 7 themes (no Tailwind)
   - Docker-first deployment
   - Audit logging with file/shell/network tracking
   - Allowlist permission system
   - Optional Docker-in-Docker sandbox
   - Cost tracking with budget alerts
   - Telegram/Slack webhook notifications
   - Setup wizard for first-run configuration

   ### Removed
   - Claude SDK dependency
   - Claude OAuth system (~1200 lines)
   - Tailwind CSS (entire framework)
   - MCP server integration (planned for v0.2.0)

   ### Changed
   - Auth: OAuth → API key
   - Backend: claude-agent-sdk → openai SDK
   - Frontend: Tailwind → MUI v6
   - State: ephemeral → persistent (Zustand + SQLite)
   ```
6. **LICENSE:** Verificar AGPL-3.0 está correto + copyright notice atualizado
7. **Git tag:**
   ```bash
   git tag -a v0.1.0 -m "Initial multi-LLM release"
   git push origin v0.1.0
   ```

**Entregável:** Release v0.1.0 pronto.

**Critério de aceite:**
- `black --check core/` → ok
- `ruff check core/` → 0 errors
- `prettier --check apps/frontend/src/` → ok
- `eslint apps/frontend/src/` → 0 errors
- `docker-compose up --build` → funcional
- `pytest` → passa
- README, CHANGELOG, LICENSE atualizados
- Tag `v0.1.0` criada

---

## PARTE 3 — README.md (DRAFT)

```markdown
# kuroko-ops

```
██╗  ██╗██╗   ██╗██████╗  ██████╗ ██╗  ██╗ ██████╗        ██████╗ ██████╗ ███████╗
██║ ██╔╝██║   ██║██╔══██╗██╔═══██╗██║ ██╔╝██╔═══██╗      ██╔═══██╗██╔══██╗██╔════╝
█████╔╝ ██║   ██║██████╔╝██║   ██║█████╔╝ ██║   ██║█████╗██║   ██║██████╔╝███████╗
██╔═██╗ ██║   ██║██╔══██╗██║   ██║██╔═██╗ ██║   ██║╚════╝██║   ██║██╔═══╝ ╚════██║
██║  ██╗╚██████╔╝██║  ██║╚██████╔╝██║  ██╗╚██████╔╝      ╚██████╔╝██║     ███████║
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝       ╚═════╝ ╚═╝     ╚══════╝
```

> **Multi-LLM AI agent orchestration panel — Docker-first, provider-agnostic, MUI v6.**

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg)](docker-compose.yml)

## What is kuroko-ops?

kuroko-ops is an AI agent orchestration panel that lets you manage teams of LLM-powered agents
working together on software projects. Think of it as a virtual dev team with a Product Owner
that decomposes tasks, delegates to specialized agents, and reports progress.

**Key differentiators from the upstream [Auto-Claude](https://github.com/AndyMik90/Auto-Claude):**

| Feature | Auto-Claude | kuroko-ops |
|---------|-------------|------------|
| LLM Provider | Claude only | Any (via OpenRouter) |
| Auth | Claude OAuth (~1200 LOC) | API key (50 LOC) |
| Model Routing | Single model | LiteLLM profiles (smart/cheap/coding/fast) |
| Persistence | Ephemeral | SQLite + Zustand persist |
| Agent Architecture | Single agent | Agent teams with PO delegation |
| UI Framework | Tailwind CSS | Material UI v6 with 7 themes |
| Security | Basic | Audit logs + Allowlist + Sandbox |
| Deployment | Manual | Docker-first |
| Self-improvement | None | AGENTS.md auto-update |
| Notifications | None | Telegram/Slack webhooks |

## Quick Start

```bash
git clone https://github.com/YOUR_USER/kuroko-ops.git
cd kuroko-ops
cp .env.example .env
# Edit .env with your OpenRouter API key
docker-compose up --build
```

Open `http://localhost:3000` — the setup wizard will guide you through configuration.

## Requirements

- Docker & Docker Compose
- OpenRouter API key ([get one here](https://openrouter.ai/keys))
- Git (for workspace mounting)

## Architecture

```
Electron/React (MUI v6) ←→ FastAPI/Uvicorn (Python)
                              ├── LLMClient (OpenAI SDK → OpenRouter)
                              ├── LiteLLM Router (model profiles)
                              ├── Orchestrator (agent teams)
                              ├── Persistence (SQLite)
                              ├── Audit Logger
                              └── Webhook Manager
```

## Model Profiles

| Profile | Default Model | Use Case |
|---------|---------------|----------|
| `smart` | claude-sonnet-4-20250514 | Planning, review, complex reasoning |
| `cheap` | gemini-2.0-flash | Formatting, classification, summaries |
| `coding` | claude-sonnet-4-20250514 | Code generation and review |
| `fast` | gemini-2.0-flash | Low-latency responses |

Profiles are configurable via `.env` or the settings UI.

## Themes

7 built-in themes powered by MUI v6: **Dark**, **Midnight**, **Cyberpunk**,
**Forest**, **Ocean**, **Sunset**, **Monochrome**.

## Security

- **Audit Logs:** Every agent action (file, shell, network, LLM) logged in JSONL
- **Allowlist:** Granular control over paths, commands, and URLs
- **Sandbox:** Optional Docker-in-Docker isolation for agent commands
- **Budget:** Configurable cost limits with alerts

## License

[AGPL-3.0](LICENSE) — same as upstream.

## Credits

Forked from [Auto-Claude](https://github.com/AndyMik90/Auto-Claude) by AndyMik90.
```

---

## PARTE 4 — RESUMO DE SPRINTS

| Fase | Sprint | Nome | Entregável principal |
|------|--------|------|----------------------|
| **A** | 0 | Fork & Scaffolding | Repo renomeado, deps declaradas |
| **A** | 1 | Core LLM Client | OpenAI SDK → OpenRouter funcional |
| **A** | 2 | Auth Cleanup | OAuth removido, API key setup |
| **A** | 3 | Backend Refactor | Endpoints `/llm/*`, zero Claude |
| **A** | 4 | Frontend Cleanup | Frontend conecta ao novo backend |
| **B** | 5 | LiteLLM Router | Multi-model routing + cost tracking |
| **B** | 6 | Zustand Persist | State sobrevive restarts |
| **B** | 7 | SQLite Persistence | Sessions/messages/tasks no DB |
| **B** | 8 | AGENTS.md Auto-Update | Knowledge base viva |
| **C** | 9 | Agent Teams | PO delegation + handoff |
| **C** | 10 | Dynamic Spawning | Agentes criados sob demanda |
| **C** | 11 | Self-Improvement | Feedback loop + métricas |
| **D** | 12 | MUI Setup | ThemeProvider + 7 palettes |
| **D** | 13 | Layout Migration | Sidebar/Header/Tabs em MUI |
| **D** | 14 | Core Components | Chat/Kanban/Terminal/Modals em MUI |
| **D** | 15 | Aux Components | Forms/Cards/Settings em MUI |
| **D** | 16 | Tailwind Purge | **Zero Tailwind** no projeto |
| **E** | 17 | Audit Logging | JSONL audit trail completo |
| **E** | 18 | Allowlist | Permissões granulares |
| **E** | 19 | Docker Sandbox | Execução isolada opcional |
| **F** | 20 | Setup Wizard | First-run zero-friction |
| **F** | 21 | Webhooks | Telegram/Slack notifications |
| **F** | 22 | Bug Fixes | Stuck tasks, spec.md, roadmap |
| **F** | 23 | Docker Production | `docker-compose up` funcional |
| **G** | 24 | Unit Tests | Coverage >80% |
| **G** | 25 | E2E Tests | Fluxos críticos cobertos |
| **G** | 26 | Release v0.1.0 | Cleanup, docs, tag |

**Total: 27 sprints em 7 fases.**

---

## PARTE 5 — RISCOS & MITIGAÇÕES

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| OpenRouter rate limits | Alto | Média | LiteLLM retry + fallback models |
| MUI v6 conflito com libs existentes | Médio | Baixa | Migração incremental; fallback Shadcn UI individual |
| LiteLLM breaking changes | Médio | Baixa | Pin version, testes de integração |
| SQLite concurrency em Docker | Médio | Média | WAL mode, connection pooling via sqlmodel |
| Zustand persist schema break | Baixo | Média | Version field + migration functions |
| Docker-in-Docker security | Alto | Baixa | Default OFF, documentação clara |
| Token context overflow em agent teams | Alto | Alta | Summary compaction, sliding window, cheap model p/ resumo |
| Cost overrun com multi-model | Alto | Média | Budget alerts, hard limit, auto-pause |

---

## PARTE 6 — DECISÕES ARQUITETURAIS (ADRs)

### ADR-001: OpenAI SDK em vez de SDK proprietário
- **Contexto:** Lock-in é o problema central
- **Decisão:** `openai` SDK com `base_url` apontando para OpenRouter
- **Consequência:** Qualquer provider OpenAI-compatible funciona

### ADR-002: LiteLLM para routing
- **Contexto:** Diferentes tarefas precisam de diferentes modelos
- **Decisão:** LiteLLM Router com profiles nomeados
- **Consequência:** Custo otimizado, fallback automático

### ADR-003: MUI v6 em vez de Tailwind
- **Contexto:** Tailwind utility classes não são desejadas
- **Decisão:** MUI v6 com `sx` prop e `styled()`
- **Consequência:** Temas coerentes, component library rica, zero utility classes

### ADR-004: SQLite em vez de PostgreSQL
- **Contexto:** Docker-first, simplicidade, single-node
- **Decisão:** SQLite com WAL mode via SQLModel
- **Consequência:** Zero infra extra, portável, backup = copiar arquivo

### ADR-005: AGENTS.md como knowledge base
- **Contexto:** Agentes precisam evitar erros repetidos
- **Decisão:** Arquivo Markdown + SQLite knowledge_entries
- **Consequência:** Versionável (git), legível por humanos e LLMs

### ADR-006: AGPL-3.0 mantida
- **Contexto:** Upstream é AGPL-3.0
- **Decisão:** Manter a mesma licença
- **Consequência:** Legal compliance, contribuições upstream possíveis

---

*Fim do plano. Cada sprint é autônoma, testável e commit-ável.*
*Foco em viabilidade incremental — cada fase produz valor utilizável.*
