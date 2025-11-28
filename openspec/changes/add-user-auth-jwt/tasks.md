## 1. Implementação
- [x] 1.1 Criar modelo/armazenamento de usuário com senha hasheada e índice único para email
- [x] 1.2 Implementar endpoint de cadastro (ex.: POST /api/auth/signup) com validação de duplicidade e resposta coerente
- [x] 1.3 Implementar endpoint de login (ex.: POST /api/auth/login) que valida credenciais, emite JWT assinado com expiração e retorna/define cookie HttpOnly
- [x] 1.4 Proteger rotas/telas que exigem autenticação, redirecionando para login quando não houver token válido e levando o usuário à tela principal após autenticar
- [x] 1.5 Criar páginas Jinja para login e cadastro com formulários integrados aos endpoints de auth
- [x] 1.6 Configurar variáveis de ambiente (segredo JWT, expiração) e registrar no README/env de desenvolvimento
- [ ] 1.7 Validar manualmente fluxo de cadastro, login, acesso autenticado e expiracão do token
