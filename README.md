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

**An enhanced fork of [Auto-Claude](https://github.com/AndyMik90/Auto-Claude) by AndyMik90.**

kuroko-ops is a multi-LLM AI agent orchestration dashboard that allows you to manage virtual development teams: you explain the idea to the Product Owner (PO), and they plan, delegate tasks, coordinate coders, testers, and reviewers—all running locally or on a server, without relying on a single AI provider.

### Main differences from the original:
- Support for any LLM via OpenRouter (Claude, Gemini, Grok, DeepSeek, etc.)
- Complete removal of dependency on the Claude SDK and OAuth
- Robust persistence (Zustand + SQLite)
- Migration to Material UI v6 (without Tailwind)
- Intelligent model routing (LiteLLM)
- Notifications via Telegram/Slack
- Docker-first with ready-to-use docker-compose

**License:** AGPL-3.0 (same as upstream)
**Credits:** Based on the excellent work of [Auto-Claude](https://github.com/AndyMik90/Auto-Claude). All modifications respect the original license.

## Quick Start

```bash
git clone https://github.com/gabrielkf/kuroko-ops.git
cd kuroko-ops
cp .env.example .env
# Edite .env com sua OpenRouter API key
docker-compose up --build
