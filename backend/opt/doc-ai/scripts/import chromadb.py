# ##################################################################
# Este codigo deve ser instalado no serv 10.0.0.37/opt/doc-ai/scrips 
# Desenvolvido em 08-03-2026
# ##################################################################

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import ollama
import subprocess
import os
import json
from datetime import datetime

DB_DIR = "/opt/doc-ai/vector_db"
HISTORY_FILE = "/opt/doc-ai/history.json"

print("Carregando modelo de embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Conectando ao banco vetorial...")
client = chromadb.Client(Settings(persist_directory=DB_DIR))
collection = client.get_collection(name="biblioteca")

def salvar_historico(pergunta):
    entry = {
        "pergunta": pergunta,
        "data": datetime.now().isoformat()
    }

    if not os.path.exists(HISTORY_FILE):
        history = []
    else:
        with open(HISTORY_FILE) as f:
            history = json.load(f)

    history.append(entry)

    with open(HISTORY_FILE,"w") as f:
        json.dump(history,f,indent=2)

def abrir_pdf(caminho,pagina):
    try:
        subprocess.Popen([
            "xdg-open",
            caminho
        ])
    except:
        pass


print("\nDocAI pronto.")
print("Digite sua pergunta ou 'sair'\n")

if len(sys.argv) > 1:
    question = " ".join(sys.argv[1:])
    perguntas = [question]
else:
    perguntas = []

while True:

    if perguntas:
        question = perguntas.pop(0)
        print("Pergunta:", question)
    else:
        question = input("Pergunta: ")

    if question.lower() in ["sair","exit","quit"]:
        break

    if question.lower() in ["sair","exit","quit"]:
        break

    salvar_historico(question)

    print("\nGerando embedding...\n")

    embedding = model.encode(question)

    results = collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=5
    )

    documentos = results["documents"][0]
    metadados = results["metadatas"][0]
    distancias = results["distances"][0]

    print("\nResultados encontrados:\n")

    context = ""

    for i,(doc,meta,dist) in enumerate(zip(documentos,metadados,distancias)):

        score = round(1-dist,3)

        print(f"Resultado {i+1}")
        print("Relevância:",score)
        print("Arquivo:",meta["arquivo"])
        print("Página:",meta["pagina"])
        print("Trecho:\n")
        print(doc[:400])
        print("\n----------------------\n")

        context += doc + "\n\n"

    prompt = f"""
Você é um assistente técnico.

Use os documentos abaixo para responder a pergunta.

Documentos:

{context}

Pergunta:

{question}

Responda de forma clara e técnica.
Cite os documentos utilizados.
"""

    print("Consultando modelo...\n")

    response = ollama.chat(
        model="qwen2.5:0.5b",
        messages=[{"role":"user","content":prompt}]
    )

    print("\nResposta:\n")
    print(response["message"]["content"])

    print("\nFontes:\n")

    for meta in metadados:
        print("-",meta["arquivo"],"(página",meta["pagina"],")")

    abrir = input("\nAbrir primeiro PDF encontrado? (s/n) ")

    if abrir.lower()=="s":
        abrir_pdf(metadados[0]["caminho"],metadados[0]["pagina"])

    print("\n--------------------------------------\n")