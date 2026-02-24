# API Gateway & Auth

Um API Gateway de alta performance construído com **FastAPI**, projetado para servir como ponto de entrada central para microsserviços. Ele gerencia roteamento, autenticação e limite de taxa (rate limiting) para garantir um gerenciamento de tráfego seguro e eficiente.

## 🚀 Funcionalidades

- **Roteamento Dinâmico**: Encaminha automaticamente as requisições para os microsserviços de backend com base no caminho da URL.
- **Autenticação JWT**: Camada de segurança integrada usando JSON Web Tokens (JWT) para verificar a identidade do usuário.
- **Limite de Taxa (Rate Limiting)**: Sistema integrado baseado em Redis para prevenir abusos e garantir a disponibilidade do serviço.
- **Integração de Microsserviços**: Roteamento pré-configurado para os serviços de `users`, `orders` e `payments`.
- **Gerenciamento de Ambiente**: Sistema de configuração robusto utilizando Pydantic Settings.

## 🛠️ Tecnologias

- **FastAPI**: Framwork web moderno e rápido para construção de APIs com Python.
- **Redis**: Armazenamento de estrutura de dados em memória utilizado para o limite de taxa.
- **PyJWT**: Biblioteca para codificação e decodificação de JSON Web Tokens.
- **HTTPX**: Cliente HTTP completo para requisições assíncronas aos serviços de backend.
- **Pydantic**: Validação de dados e gerenciamento de configurações usando anotações de tipo Python.

## 📦 Instalação e Configuração

### Pré-requisitos
- Python 3.12+
- Servidor Redis (rodando localmente na porta 6379)
- Poetry (para gerenciamento de dependências)

### Instalação

1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd api-gateway-auth
   ```

2. **Instale as dependências**:
   ```bash
   poetry install
   ```

3. **Configure as Variáveis de Ambiente**:
   Crie um arquivo `.env` na raiz do diretório:
   ```env
   API_GATEWAY_AUTH_SECRET_KEY=sua_chave_secreta_aqui
   API_GATEWAY_AUTH_ALGORITHM=HS256
   API_GATEWAY_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Execute a Aplicação**:
   ```bash
   fastapi dev src/gateway/main.py
   ```

## 🔌 Rotas da API

O gateway intercepta as requisições e as encaminha com base no nome do serviço:

- `GET /users/{path}` -> Encaminha para o Serviço de Usuários
- `GET /orders/{path}` -> Encaminha para o Serviço de Pedidos
- `GET /payments/{path}` -> Encaminha para o Serviço de Pagamentos

Todas as requisições exigem um token JWT válido na camada de autenticação e estão sujeitas às políticas de limite de taxa.

## 📁 Estrutura do Projeto

```text
api-gateway-auth/
├── src/
│   └── gateway/
│       ├── auth.py         # Lógica de JWT
│       ├── main.py         # Ponto de Entrada da Aplicação
│       ├── rate_limit.py   # Limitador de Taxa com Redis
│       ├── router.py       # Lógica de Roteamento de Serviços
│       └── settings.py     # Configurações Globais
├── tests/                  # Testes Automatizados
├── pyproject.toml          # Metadados e Dependências do Projeto
└── .env                    # Variáveis de Ambiente
```

## 📄 Licença

Este projeto está licenciado sob a Licença MIT.
