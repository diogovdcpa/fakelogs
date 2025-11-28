## ADDED Requirements
### Requirement: Cadastro de usuário
O sistema SHALL expor página e endpoint de cadastro para criar usuário com email e senha, armazenando a senha hasheada e impedindo emails duplicados.

#### Scenario: Cadastro bem-sucedido
- **WHEN** o usuário envia email e senha válidos
- **THEN** o cadastro é criado com senha armazenada em hash
- **AND** a resposta confirma criação sem expor a senha ou o hash

#### Scenario: Email duplicado
- **WHEN** o usuário tenta cadastrar um email já existente
- **THEN** o sistema retorna erro de validação e não cria novo registro

### Requirement: Login com JWT
O sistema SHALL autenticar usuários via email e senha, emitindo JWT assinado com segredo configurável e expiração definida para controlar sessões.

#### Scenario: Login válido retorna JWT
- **WHEN** credenciais corretas são enviadas
- **THEN** o sistema emite JWT com identificação do usuário e expiração configurada
- **AND** retorna o token ao cliente e o define como cookie HttpOnly com SameSite=Lax

#### Scenario: Credenciais inválidas
- **WHEN** email ou senha estão incorretos
- **THEN** o sistema responde com 401 e não emite token

### Requirement: Navegação autenticada e redirecionamento
O sistema SHALL exigir JWT válido para acessar a tela principal e SHALL redirecionar o usuário autenticado para essa tela após login.

#### Scenario: Redirecionamento após login
- **WHEN** o login é bem-sucedido
- **THEN** o usuário é enviado para a tela principal com sessão baseada no JWT emitido

#### Scenario: Acesso sem token
- **WHEN** o usuário tenta acessar a tela principal sem JWT válido
- **THEN** é redirecionado para a página de login e orientado a autenticar

#### Scenario: Token expirado ou inválido
- **WHEN** a requisição contém token expirado ou inválido
- **THEN** o sistema invalida a sessão, remove o cookie e exige novo login
