# Backend do Sistema de Controle de Estacionamento

API REST desenvolvida com FastAPI para gerenciar o sistema de controle de estacionamento.

## Funcionalidades

- Autenticação de usuários (JWT + Cognito)
- Gerenciamento de veículos
- Controle de vagas de estacionamento
- Registro de entrada/saída de veículos
- Integração com câmeras para reconhecimento de placas
- Upload de imagens para S3

## Requisitos

- Python 3.8+
- MySQL/MariaDB
- AWS Account (S3, Cognito)

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

## Executando

1. Ative o ambiente virtual (se não estiver ativo)
2. Execute o servidor:
   ```bash
   uvicorn main:app --reload
   ```

3. Acesse a documentação da API:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Estrutura do Projeto

```
backend/
├── app/
│   ├── models/      # Modelos SQLAlchemy
│   ├── routes/      # Rotas da API
│   ├── schemas/     # Schemas Pydantic
│   └── utils/       # Funções utilitárias
├── requirements.txt # Dependências
├── main.py         # Ponto de entrada
└── .env           # Variáveis de ambiente
```

## Endpoints Principais

- `POST /auth/register`: Registro de usuário
- `POST /auth/token`: Login (obter token)
- `GET /vehicles`: Listar veículos do usuário
- `POST /vehicles`: Cadastrar novo veículo
- `GET /parking/map`: Visualizar mapa do estacionamento
- `POST /parking/entry`: Registrar entrada de veículo
- `POST /parking/exit/{record_id}`: Registrar saída de veículo
- `POST /camera/process-entry`: Processar imagem de entrada
- `POST /camera/process-exit`: Processar imagem de saída

## Desenvolvimento

Para contribuir com o projeto:

1. Crie uma branch para sua feature
2. Faça suas alterações
3. Execute os testes
4. Envie um pull request

## Próximos Passos

- Implementar reconhecimento de placas com AWS Rekognition
- Adicionar testes automatizados
- Implementar cache com Redis
- Adicionar logging estruturado
- Configurar CI/CD 