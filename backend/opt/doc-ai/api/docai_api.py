# ###############################################################
# DocAI - API de Busca Vetorial de Documentos Técnicos
#
# Servidor: 10.0.0.37
# Sistema: Ubuntu Linux
#
# Local do arquivo:
# /opt/doc-ai/api/docai_api.py
#
# Serviço systemd:
# /etc/systemd/system/docai.service
#
# Porta da API:
# http://127.0.0.1:5005
#
# ###############################################################
# Descrição
#
# Esta API implementa o motor de busca do sistema DocAI.
# Ela consulta um banco vetorial (ChromaDB) contendo trechos
# indexados de documentos PDF e retorna os resultados mais
# semanticamente próximos da consulta do usuário.
#
# A API é utilizada pela interface web localizada em:
#
# /var/www/html/docai/
#
# A comunicação ocorre através de chamadas HTTP realizadas
# pelo script PHP:
#
# /var/www/html/docai/src/search.php
#
# ###############################################################
# Componentes utilizados
#
# FastAPI
# Framework de API REST em Python
#
# ChromaDB
# Banco vetorial onde estão armazenados os embeddings
#
# SentenceTransformers
# Modelo de embeddings utilizado para transformar a consulta
# do usuário em vetor semântico
#
# Modelo utilizado:
# sentence-transformers/all-MiniLM-L6-v2
#
# ###############################################################
# Banco Vetorial
#
# Local do banco:
# /opt/doc-ai/vector_db
#
# Collection utilizada:
# biblioteca
#
# Conteúdo:
# Trechos extraídos dos documentos PDF indexados pelo
# script de indexação DocAI.
#
# ###############################################################
# Endpoints disponíveis
#
# /search
# Realiza busca semântica nos documentos indexados
#
# Exemplo:
# http://127.0.0.1:5005/search?q=arduino
#
# Retorno JSON:
#
# {
#   "query": "arduino",
#   "results": [
#       {
#           "arquivo": "nome.pdf",
#           "pagina": 40,
#           "trecho": "texto encontrado...",
#           "caminho": "/opt/doc-ai/pdfs/...pdf",
#           "score": 0.63
#       }
#   ]
# }
#
# ---------------------------------------------------------------
#
# /stats
# Retorna estatísticas da base vetorial
#
# Exemplo:
# http://127.0.0.1:5005/stats
#
# Retorno:
#
# {
#   "chunks": 55635
# }
#
# ###############################################################
# Inicialização do serviço
#
# O serviço é iniciado automaticamente pelo systemd
# através do arquivo:
#
# /etc/systemd/system/docai.service
#
# Comando utilizado:
#
# /opt/doc-ai/venv/bin/uvicorn api.docai_api:app \
# --host 127.0.0.1 --port 5005
#
# ###############################################################
# Comandos úteis
#
# Reiniciar API
#
# sudo systemctl restart docai
#
# Ver status
#
# sudo systemctl status docai
#
# Testar busca
#
# curl "http://127.0.0.1:5005/search?q=arduino"
#
# Testar estatísticas
#
# curl http://127.0.0.1:5005/stats
#
# ###############################################################
# Autor
# Projeto DocAI - Motor de busca técnico local
#
# Desenvolvido para consulta inteligente de bibliotecas
# técnicas em PDF utilizando IA e busca vetorial.
# ###############################################################

from fastapi import FastAPI
import chromadb
from sentence_transformers import SentenceTransformer

app = FastAPI()

# abrir banco vetorial
client = chromadb.PersistentClient(
    path="/opt/doc-ai/vector_db"
)

collection = client.get_collection("biblioteca")

# modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")


# ==========================================
# BUSCA
# ==========================================

@app.get("/search")
def search(q: str):

    if not q.strip():
        return {
            "query": q,
            "results": []
        }

    embedding = model.encode(q).tolist()

    res = collection.query(
        query_embeddings=[embedding],
        n_results=20
    )

    results = []

    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dist = res.get("distances", [[]])[0]

    for i in range(len(docs)):

        meta = metas[i]

        results.append({
            "arquivo": meta.get("arquivo"),
            "pagina": meta.get("pagina"),
            "trecho": docs[i],
            "caminho": meta.get("caminho"),
            "score": dist[i]
        })

    return {
        "query": q,
        "results": results
    }


# ==========================================
# ESTATÍSTICAS
# ==========================================

@app.get("/stats")
def stats():

    total_chunks = collection.count()

    return {
        "chunks": total_chunks
    }