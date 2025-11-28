# Project Context

## Purpose
Plataforma Flask leve para envio e exposição de logs usados em testes de regras e validações de parse. Oferece landing page (Jinja + Tailwind CDN) e APIs para receber/servir payloads determinísticos, com opção de persistir logs em SQLite via ORM para simular fluxos de validação.

## Tech Stack
- Python 3.9+
- Flask 3.x for HTTP routing and JSON responses, organized com Blueprints
- Jinja2 para views server-side
- Tailwind CSS via CDN para estilizar as páginas renderizadas
- Gunicorn para desenvolvimento local
- SQLite3 com ORM (ex.: SQLAlchemy) para persistência simples
- Vercel Python Runtime for deployment as serverless functions
- Templates renderizados via Jinja; assets estáticos em `public/` (ex.: favicon); Tailwind carregado por CDN direto nos templates

## Project Conventions

### Code Style
- Follow PEP 8 with 4-space indents and double-quoted strings (matches current code)
- Prefer type hints on view parameters and return types when practical
- Keep Flask views small and stateless; build responses with `jsonify` and plain dicts/lists
- Organize endpoints behind blueprints; export the blueprint via `endpoints/__init__.py`

### Architecture Patterns
- `main.py` apenas instancia `app` via `app.create_app()`; toda a lógica fica em `app/`
- Pacote `app/` organizado por entidades: `auth/` (models/routes/security), `endpoints/` (APIs públicas), `db.py` (engine/sessão)
- Páginas renderizadas com Jinja2; use um layout base e partiais para componentes comuns
- Estilos fornecidos pelo Tailwind CDN diretamente nos templates (sem build step)
- API sob `/api/*` dentro do blueprint; mantenha handlers pequenos e coesos
- Persistência local com SQLite3 via ORM; centralize modelos e conexões em um módulo dedicado
- Keep serverless constraints in mind (stateless, short execution, minimal dependencies)

### Testing Strategy
- Sem uso de testes automatizados no momento
- Validação manual via `gunicorn main:app` (ou `flask run`) e requisições a `/api/data` e `/api/items/<id>`
- Conferir manualmente status code 200 e payload determinístico dos endpoints antes de publicar

### Git Workflow
- `main`: produção (deploy Vercel). Só recebe merge de releases vindas de `develop`
- `develop`: integração contínua. Toda `feature/*` nasce aqui e volta via PR
- `feature/*`: branch por mudança; merge em `develop` após revisão. Use nomes descritivos em kebab-case
- `hotfix/*`: somente quando partir de `main` para corrigir produção; mesclar de volta em `main` e `develop`
- Commits claros com prefixos (`feat|fix|chore|docs`) e smoke test local (`gunicorn main:app`) antes de mesclar

## Domain Context
- Plataforma foca em tráfego de logs para validar regras/parsers (payloads determinísticos para cenários de teste)
- APIs em `/api/data` e `/api/items/<id>` servem como exemplos de payload; auth via login/cadastro com JWT e cookie HttpOnly
- Persistência via SQLite3 fica disponível para armazenar/consultar logs que representam casos de teste

## Important Constraints
- Must remain stateless and compatible with Vercel serverless runtime (no background workers or long-running tasks)
- Para SQLite em ambiente serverless, espere armazenamento efêmero; use para dev/local ou dados descartáveis
- Avoid large dependencies that increase cold starts; mantenha o ORM enxuto
- Keep responses deterministic and lightweight to support caching and quick demos
- Do not commit secrets or environment-specific configuration

## External Dependencies
- Vercel for hosting/serverless execution
- SQLite3 local para persistência (arquivo gerenciado pelo app/ORM)
- Sem APIs externas no momento; dados servidos localmente
