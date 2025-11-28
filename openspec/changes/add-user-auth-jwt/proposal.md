# Change: Adicionar autenticação de usuários com JWT

## Why
A aplicação não possui controle de acesso; é preciso permitir que usuários se cadastrem, façam login com credenciais e recebam um token para proteger o acesso à tela principal.

## What Changes
- Criar página e endpoint de cadastro para armazenar usuários com senha hasheada
- Criar fluxo de login que emite JWT assinado e o entrega ao cliente
- Proteger o acesso à tela principal exigindo JWT válido e redirecionando após login
- Documentar configuração de segredo e expiração do token

## Impact
- Affected specs: auth
- Affected code: main.py, endpoints (novo blueprint de auth), templates Jinja para login/cadastro e lógica de guarda de rota
