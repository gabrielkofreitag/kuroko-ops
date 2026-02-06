### Kuroko-Ops

```text
██╗  ██╗██╗   ██╗██████╗  ██████╗ ██╗  ██╗ ██████╗       ██████╗ ██████╗ ███████╗
██║ ██╔╝██║   ██║██╔══██╗██╔═══██╗██║ ██╔╝██╔═══██╗     ██╔═══██╗██╔══██╗██╔════╝
█████╔╝ ██║   ██║██████╔╝██║   ██║█████╔╝ ██║   ██║     ██║   ██║██████╔╝███████╗
██╔═██╗ ██║   ██║██╔══██╗██║   ██║██╔═██╗ ██║   ██║     ██║   ██║██╔═══╝ ╚════██║
██║  ██╗╚██████╔╝██║  ██║╚██████╔╝██║  ██╗╚██████╔╝     ╚██████╔╝██║     ███████║
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝       ╚═════╝ ╚═╝     ╚══════╝
                                                         v0.1.0 :: kuroko-ops.work
```

**Fork aprimorado do [Auto-Claude](https://github.com/AndyMik90/Auto-Claude) por AndyMik90.**

kuroko-ops é um painel de orquestração de agentes de IA multi-LLM que permite gerenciar equipes virtuais de desenvolvimento: você explica a ideia para o Product Owner (PO), e ele planeja, delega tarefas, coordena coders, testers e reviewers — tudo rodando localmente ou em servidor, sem depender de um único provedor de IA.

### Principais diferenças em relação ao original:
- Suporte a qualquer LLM via OpenRouter (Claude, Gemini, Grok, DeepSeek, etc.)
- Remoção completa de dependência do Claude SDK e OAuth
- Persistência robusta (Zustand + SQLite)
- Migração para Material UI v6 (sem Tailwind)
- Roteamento inteligente de modelos (LiteLLM)
- Notificações via Telegram/Slack
- Docker-first com docker-compose pronto

**Licença:** AGPL-3.0 (mesma do upstream)  
**Créditos:** Baseado no excelente trabalho do [Auto-Claude](https://github.com/AndyMik90/Auto-Claude). Todas as modificações respeitam a licença original.

## Quick Start

```bash
git clone https://github.com/gabrielkf/kuroko-ops.git
cd kuroko-ops
cp .env.example .env
# Edite .env com sua OpenRouter API key
docker-compose up --build
