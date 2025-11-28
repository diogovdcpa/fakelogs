# Fakelogs (Flask + JWT + SQLite)

Plataforma simples para envio e exposição de logs falsos usados em testes de regras e validações de parse. Inclui autenticação com JWT, páginas renderizadas em Jinja + Tailwind CDN e endpoints de mock data.

## Stack
- Flask 3.x com Blueprints
- Jinja2 + Tailwind via CDN
- SQLite3 com SQLAlchemy (ORM)
- PyJWT para emissão/validação de tokens
- Gunicorn para desenvolvimento local e Vercel Python Runtime para deploy

## Configuração de ambiente
Defina variáveis para o fluxo de autenticação e banco:
- `JWT_SECRET`: segredo para assinar tokens (obrigatório em produção; padrão `dev-secret` para dev)
- `JWT_EXP_MINUTES`: expiração do JWT em minutos (padrão `60`)
- `JWT_COOKIE_NAME`: nome do cookie com o token (padrão `auth_token`)
- `JWT_COOKIE_SECURE`: use `true` em produção para marcar o cookie como `Secure` (padrão `false`)
- `DATABASE_URL`: URL do SQLite (padrão `sqlite:///./data.db`; em serverless o armazenamento é efêmero)

## Rodando localmente
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
export JWT_SECRET=dev-secret
gunicorn main:app
```
O app fica disponível em `http://localhost:8000` por padrão (porta do Gunicorn).

## Fluxo de autenticação
- Páginas: `/auth/signup` (cadastro) e `/auth/login` (login). Sucesso no login define cookie HttpOnly `auth_token` com SameSite=Lax e expiração configurável.
- APIs:
  - `POST /auth/signup`: cria usuário com email único e senha hasheada (JSON ou formulário). Sucesso retorna 201 com mensagem ou redireciona para login.
  - `POST /auth/login`: valida credenciais, emite JWT e retorna `{"token": "...", "token_type": "Bearer", "user": {...}}` além de setar o cookie.
  - `GET /auth/logout`: limpa o cookie e redireciona para login.
- A rota `/` é protegida: sem token válido o usuário é redirecionado para login; token inválido/expirado remove o cookie e exige nova autenticação.

## Endpoints de mock data
- `GET /api/data`: lista de itens determinísticos para testes.
- `GET /api/items/<id>`: item individual baseado no id.

## Observações de persistência
- Em ambientes serverless (Vercel), o SQLite é efêmero; use apenas para dados de teste. Para persistência real, configure um banco externo e ajuste `DATABASE_URL`.

## Fluxo de branches (git)
- `main`: produção (deploy Vercel). Só recebe merge vindo de `develop` quando está pronto para publicar.
- `develop`: integração contínua. Toda feature sai daqui e volta para cá via PR/merge.
- `feature/*`: branches por mudança (`git checkout -b feature/nome` a partir de `develop`), revisadas e mescladas em `develop`.
- Releases: quando `develop` estiver estável, abrir PR/merge para `main` e disparar o deploy.
- Hotfix: se urgente em produção, criar `hotfix/*` a partir de `main`, depois mesclar em `main` e também em `develop` para não divergir.
