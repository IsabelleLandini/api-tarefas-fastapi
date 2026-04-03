# 📋 API de Tarefas

API para gerenciamento de tarefas, construída com FastAPI, com autenticação básica e banco de dados SQLite. O projeto é executado dentro de um contêiner Docker, garantindo um ambiente consistente e replicável.

---

## Sobre o projeto

Este projeto foi desenvolvido com o objetivo de praticar:

* Criação de APIs REST com FastAPI
* Integração com banco de dados usando SQLAlchemy
* Autenticação básica (HTTP Basic)
* Containerização com Docker/Podman
* Gerenciamento de dependências com Poetry

---

## Tecnologias utilizadas

* Python 3.12
* FastAPI
* SQLAlchemy (ORM)
* Pydantic (validação de dados)
* SQLite
* Poetry
* Docker / Podman
* Docker Compose

---

## Estrutura do projeto

```
.
├── main.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
├── .env
├── .gitignore
└── README.md
```

---

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```
DATABASE_URL=sqlite:///./tarefas.db
MEU_USUARIO=admin
MINHA_SENHA=1234
```

---

## 🐳 Como executar o projeto

### Clonar o repositório

```
git clone https://github.com/seu-usuario/api-tarefas-fastapi.git
cd api-tarefas-fastapi
```

---

### Subir a aplicação

#### Docker

```
docker-compose up --build -d
```

#### Podman

```
podman-compose up --build
```

---

### Acessar a API

* API: http://localhost:8000
* Documentação interativa: http://localhost:8000/docs

---

## Autenticação

A API utiliza autenticação básica (HTTP Basic).

No Swagger (`/docs`), clique em **Authorize** e utilize:

```
username: admin
password: 1234
```

---

## Endpoints principais

### Criar tarefa

`POST /adiciona`

```
{
  "nome_tarefa": "Estudar Docker",
  "descricao": "Praticar containers",
  "concluida": false
}
```

---

### Listar tarefas

`GET /tarefas`

---

### Atualizar tarefa

`PUT /atualiza/{id}`

```
{
  "nome_tarefa": "Estudar Docker",
  "descricao": "Já pratiquei",
  "concluida": true
}
```

---

### Deletar tarefa

`DELETE /deletar/{id}`

---

## Parar a aplicação

```
docker-compose down
```

ou

```
podman-compose down
```

---

## Observações

* O banco de dados é persistido utilizando volumes
* O código é sincronizado com o container (hot reload)
* Projeto estruturado para facilitar desenvolvimento e testes

---

## 👩‍💻 Autora

Desenvolvido por Isabelle Landini

---

## Objetivo

Projeto desenvolvido para fins de estudo e portfólio, com foco em backend moderno utilizando FastAPI e boas práticas de containerização.

---
