#==============================
#   API de Tarefas - FastAPI   
#==============================

# Importações principais
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Validação de dados
from pydantic import BaseModel 

# Tipagem
from typing import List

# Segurança
import secrets

# Variáveis de ambiente
import os

# SQLAlchemy 
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# CONFIGURAÇÃO DO BANCO DE DADOS

# Vem do .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise Exception("DATABASE_URL não definida no .env")

# Criação da engine (conexão com o banco)
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL, 
        connect_args={'check_same_thread':False}
    )
else:
    engine = create_engine(DATABASE_URL)

# Sessão do banco
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# Base para criação das tabelas
Base = declarative_base()

# CONFIGURAÇÃO DA API

app = FastAPI(
    title= "API de Tarefas",
    description= "API para gerenciar Tarefas.",
    version="1.0.0",
    contact={
        "name": "Isabelle Landini",
        "email": "isa_landini@hotmail.com"
    } 
)

# AUTENTICAÇÃO

MEU_USUARIO = os.getenv("MEU_USUARIO")
MINHA_SENHA = os.getenv("MINHA_SENHA")
if not MEU_USUARIO or not MINHA_SENHA:
    raise Exception("Credenciais não configuradas no .env")

security = HTTPBasic()

def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Valida usuário e senha
    """
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"}
        )
    return credentials

# Modelos

# Banco (SQLAlchemy)
class TarefaDB(Base):
    """
    Representa a tabela de tarefas no banco
    """
    __tablename__ = 'tarefas'

    id = Column(Integer, primary_key=True, index=True)
    nome_tarefa = Column(String, index=True)
    descricao = Column(String)
    concluida = Column(Boolean, default=False)

# Entrada (POST/PUT) 
class Tarefa(BaseModel):
    """
    Modelo de entrada da API
    """
    nome_tarefa: str
    descricao: str
    concluida: bool = False

# Saída (GET)
class TarefaRead(BaseModel):
    id: int
    nome_tarefa: str
    descricao: str
    concluida: bool

    class Config:
        from_attributes = True # Permite que o Pydantic leia objetos do SQLAlchemy

class TarefaPaginada(BaseModel):
    page: int
    limit: int
    total: int
    tarefas: List[TarefaRead]

# Cria as tabelas automaticamente   
Base.metadata.create_all(bind=engine)

# DEPENDÊNCIA DO BANCO

def sessao_db():
    """
    Cria e fecha sessão com o banco
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ROTAS

@app.get("/")
def home():
    """
    Rota inicial
    """
    return {"message": "API de tarefas rodando!"}


@app.get("/tarefas", response_model=TarefaPaginada)
def get_tarefas(
    page: int = 1, 
    limit: int = 10, 
    db: Session = Depends(sessao_db),
    credentials: HTTPBasicCredentials = Depends(autenticar_usuario)
):
    """
    Lista tarefas com paginação
    """
    if page < 1 or limit < 1:
       raise HTTPException(
           status_code=400, 
           detail= 'Page e Limit estão com valores inválidos.'
        )
    
    tarefas = db.query(TarefaDB).offset((page-1) * limit).limit(limit).all()
    total_tarefas = db.query(TarefaDB).count()

    return {
            'page': page,
            'limit': limit,
            'total': total_tarefas,
            'tarefas': tarefas,
    } 


@app.post("/tarefas", response_model=TarefaRead)
def post_tarefas(
    tarefa: Tarefa, 
    db: Session = Depends(sessao_db),
    credentials: HTTPBasicCredentials = Depends(autenticar_usuario)
):
    """
    Adiciona nova tarefa
    """
    db_tarefa = db.query(TarefaDB).filter(
        TarefaDB.nome_tarefa == tarefa.nome_tarefa, 
        TarefaDB.descricao == tarefa.descricao
    ).first()

    if db_tarefa:
        raise HTTPException(
            status_code=400, 
            detail="Essa tarefa já existe no catálogo."
        )
    
    nova_tarefa = TarefaDB(
        nome_tarefa = tarefa.nome_tarefa, 
        descricao = tarefa.descricao, 
        concluida = tarefa.concluida
    )
    
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    
    return nova_tarefa


@app.put("/tarefas/{id_tarefa}", response_model=TarefaRead)
def put_tarefas (
    id_tarefa: int, 
    tarefa: Tarefa, 
    db: Session = Depends(sessao_db),
    credentials: HTTPBasicCredentials = Depends(autenticar_usuario)
):
    """
    Atualiza tarefa
    """
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.id == id_tarefa).first()
    
    if not db_tarefa:
        raise HTTPException(
            status_code=404, 
            detail= "Essa tarefa não foi encontrada.")
    
    db_tarefa.nome_tarefa = tarefa.nome_tarefa
    db_tarefa.descricao = tarefa.descricao
    db_tarefa.concluida = tarefa.concluida

    db.commit()
    db.refresh(db_tarefa)

    return db_tarefa

 
@app.delete("/tarefas/{id_tarefa}")
def delete_tarefa(
    id_tarefa: int, 
    db: Session = Depends(sessao_db),
    credentials: HTTPBasicCredentials = Depends(autenticar_usuario)
):
    """
    Remove tarefa
    """
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.id == id_tarefa).first()
    
    if not db_tarefa:
        raise HTTPException(
            status_code=404, 
            detail= "Tarefa não foi encontrada."
        )
    
    db.delete(db_tarefa)
    db.commit()

    return {"message": "Tarefa deletada com sucesso!"}
    


