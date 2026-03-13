
# Sentinela DocAI — Sistema de Consulta Inteligente de Biblioteca Técnica

Sistema de **indexação e consulta semântica de documentos técnicos** utilizando **RAG (Retrieval Augmented Generation)** rodando **100% local**. O sistema transforma uma coleção de documentos técnicos em um **assistente técnico pesquisável**, capaz de responder perguntas utilizando conhecimento presente nos próprios documentos.

O Sentinela atua como a camada de orquestração e inteligência do ecossistema, integrando diferentes fontes de dados e serviços de IA. Dentro dessa arquitetura, o Sentinela DocAI funciona como o módulo especializado em consulta semântica de documentação técnica, permitindo que o sistema Sentinela utilize o conhecimento presente em bibliotecas de PDFs, manuais e normas técnicas. Quando uma consulta é realizada, o Sentinela encaminha a pergunta para o DocAI, que executa a busca vetorial na base indexada, recupera os trechos mais relevantes e os retorna como contexto técnico. Esse contexto pode então ser utilizado diretamente ou combinado com modelos LLM locais para gerar respostas estruturadas, transformando a biblioteca técnica em uma base de conhecimento ativa integrada ao sistema Sentinela.

---

# 📑 Índice

* [🎯 Objetivo](#-objetivo)
* [🖥️ Infraestrutura](#️-infraestrutura)
* [🖥️ Servidores](#️-servidores)
* [📚 Biblioteca Técnica](#-biblioteca-técnica)
* [📁 Estrutura do Projeto](#-estrutura-do-projeto)
* [🧠 Arquitetura do Sistema](#-arquitetura-do-sistema)
* [📊 Diagrama de Arquitetura](#-diagrama-de-arquitetura)
* [🔎 Pipeline de Indexação](#-pipeline-de-indexação)
* [🔎 Pipeline de Indexação com OCR](#-pipeline-de-indexação-com-ocr)
* [🧩 Pipeline RAG](#-pipeline-rag)
* [📦 Preparação do Ambiente](#-preparação-do-ambiente)
* [📚 Transferência da Biblioteca](#-transferência-da-biblioteca)
* [🧠 Modelo de Embeddings](#-modelo-de-embeddings)
* [🧩 Script de Indexação](#-script-de-indexação)
* [🧾 Metadados Indexados](#-metadados-indexados)
* [▶️ Executar Indexação](#️-executar-indexação)
* [⏱️ Tempo de Indexação](#️-tempo-de-indexação)
* [🗂️ Banco Vetorial](#️-banco-vetorial)
* [🔍 API DocAI](#-api-docai)
* [🤖 Modelos LLM](#-modelos-llm)
* [💬 Integração com AI Gateway](#-integração-com-ai-gateway)
* [🧪 Monitoramento](#-monitoramento)
* [📚 Documentação do Sistema DocAI](#-documentação-do-sistema-docai)

---

# 🎯 Objetivo

Permitir:

* indexar bibliotecas grandes de documentos
* criar embeddings semânticos
* buscar conhecimento técnico
* integrar com modelos LLM locais
* operar completamente offline
* integrar com sistemas externos via API

---

# 🖥️ Infraestrutura

Arquitetura atual do sistema:

```
Usuário
 ↓
OpenWebUI
 ↓
Sentinela AI Gateway (10.0.0.139)
 ↓
DocAI API (10.0.0.37)
 ↓
Banco Vetorial (ChromaDB)
 ↓
Ollama LLM (10.0.0.37)
```

---

# 🖥️ Servidores

## Servidor DocAI

```
10.0.0.37
```

Sistema operacional:

```
Ubuntu Linux
```

Hardware:

```
CPU only
```

---

## Servidor AI Gateway

```
10.0.0.139
```

Responsável por:

* orquestrar consultas
* integrar DocAI
* integrar MySQL
* enviar prompts para Ollama

---

# 📚 Biblioteca Técnica

Quantidade de documentos:

```
1063 PDFs
≈22GB
```

Origem da biblioteca:

```
10.0.0.5:/var/www/html/Biblioteca
```

Destino no servidor DocAI:

```
/opt/doc-ai/pdfs
```

---

# 📁 Estrutura do Projeto

```
/opt/doc-ai
│
├── pdfs
│   └── Biblioteca completa (1063 PDFs)
│
├── scripts
│   └── index_pdfs.py
│
├── vector_db
│   └── Banco vetorial ChromaDB
│
├── api
│   └── docai_api.py
│
├── venv
│   └── ambiente Python isolado
│
└── README.md
```

---

# 🧠 Arquitetura do Sistema

```
PDFs
 ↓
extração de texto
 ↓
divisão em trechos
 ↓
geração de embeddings
 ↓
armazenamento vetorial
 ↓
consulta semântica
 ↓
LLM (Ollama)
 ↓
resposta
```

---

# 📊 Diagrama de Arquitetura

```
             +------------------+
             |  Biblioteca PDF  |
             |  1063 arquivos   |
             +---------+--------+
                       |
                       v
               +----------------+
               | Indexador PDF  |
               | Python Script  |
               +-------+--------+
                       |
                       v
               +----------------+
               |   ChromaDB     |
               | Banco Vetorial |
               +-------+--------+
                       |
                       v
               +----------------+
               |  API DocAI     |
               | FastAPI        |
               +-------+--------+
                       |
         +-------------+-------------+
         |                           |
         v                           v
   +------------+              +-------------+
   | Ollama LLM |              | AI Gateway  |
   +------------+              +-------------+
```

---

# 🔎 Pipeline de Indexação

Pipeline principal:

```
PDF
 ↓
extração de texto (pypdf)
 ↓
divisão em chunks
 ↓
geração de embeddings
 ↓
armazenamento no ChromaDB
```

---

# 🔎 Pipeline de Indexação com OCR

Alguns documentos da biblioteca são **PDFs escaneados (imagem)**.

Nestes casos o sistema executa **OCR automático**.

Pipeline:

```
PDF
 ↓
extração de texto (pypdf)
 ↓
se texto inexistente
 ↓
OCR (Tesseract)
 ↓
texto recuperado
 ↓
divisão em chunks
 ↓
geração de embeddings
 ↓
armazenamento vetorial
```

Isso permite indexar:

* revistas escaneadas
* apostilas digitalizadas
* manuais antigos

---

# 🧩 Pipeline RAG

```
Pergunta do usuário
 ↓
embedding da pergunta
 ↓
busca vetorial
 ↓
retorno de trechos relevantes
 ↓
envio para LLM
 ↓
geração da resposta
```

---

# 📦 Preparação do Ambiente

Criar diretório do projeto:

```
mkdir -p /opt/doc-ai
cd /opt/doc-ai
```

---

## 🐍 Criar ambiente virtual Python

```
python3 -m venv venv
```

Ativar:

```
source venv/bin/activate
```

---

## 📦 Instalar dependências

```
pip install langchain
pip install chromadb
pip install pypdf
pip install sentence-transformers
pip install langchain-text-splitters
pip install fastapi
pip install uvicorn
```

---

## 📦 Dependências adicionais (OCR e criptografia)

Dependências Python:

```
pip install cryptography
pip install pytesseract
pip install pdf2image
pip install pillow
```

Dependências do sistema:

```
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-por
sudo apt install poppler-utils
```

---

# 📚 Transferência da Biblioteca

Transferência realizada com:

```
rsync -avh --progress epaminondas@10.0.0.5:/var/www/html/Biblioteca/ /opt/doc-ai/pdfs/
```

Verificação:

```
find /opt/doc-ai/pdfs -type f -iname "*.pdf" | wc -l
```

Resultado esperado:

```
1063
```

---

# 🧠 Modelo de Embeddings

Modelo utilizado:

```
sentence-transformers/all-MiniLM-L6-v2
```

| Propriedade | Valor          |
| ----------- | -------------- |
| Dimensão    | 384            |
| RAM         | baixa          |
| Velocidade  | alta           |
| Qualidade   | ótima para RAG |

Motivo da escolha:

* melhor desempenho em CPU
* rápido para bibliotecas grandes
* boa qualidade sem GPU

---

# 🧩 Script de Indexação

Localização:

```
/opt/doc-ai/scripts/index_pdfs_v6.py
```

Verificar nos diretório qual a **última versão em uso**.

Responsabilidades:

* percorrer biblioteca
* extrair texto
* aplicar OCR quando necessário
* dividir conteúdo em chunks
* gerar embeddings
* armazenar metadados
* tratar PDFs criptografados

---

# 🧾 Metadados Indexados

Cada trecho armazena:

```
{
  "arquivo": "NBR5410.pdf",
  "pagina": 114,
  "caminho": "/opt/doc-ai/pdfs/Instalações Elétricas/NBR5410.pdf"
}
```

| Campo   | Descrição            |
| ------- | -------------------- |
| arquivo | nome do PDF          |
| pagina  | página do documento  |
| caminho | localização completa |

Isso permite **respostas com referência precisa da fonte**.

---

# ▶️ Executar Indexação

Ativar ambiente:

```
source /opt/doc-ai/venv/bin/activate
```

Executar:

```
python /opt/doc-ai/scripts/index_pdfs.py
```

---

# ⏱️ Tempo de Indexação

Para biblioteca atual:

```
1063 PDFs
≈22GB
CPU only
```

Tempo típico:

```
2 a 6 horas
```

(depende da quantidade de páginas que exigem OCR)

---

# 🗂️ Banco Vetorial

Local:

```
/opt/doc-ai/vector_db
```

Contém:

* embeddings
* texto indexado
* metadados

---

# 🔍 API DocAI

Servidor:

```
http://10.0.0.37:5005
```

Documentação:

```
http://10.0.0.37:5005/docs
```

Endpoint principal:

```
/search?q=pergunta
```

Exemplo:

```
curl "http://10.0.0.37:5005/search?q=MQTT"
```

Resposta:

```
trechos relevantes do PDF
```

---

# 🤖 Modelos LLM

Servidor Ollama:

```
10.0.0.37
porta 11434
```

Modelos instalados:

```
tinyllama
tinyllama-fast
qwen2.5:0.5b
qwen2.5:1.5b
```

Modelo recomendado:

```
qwen2.5:1.5b
```

Melhor qualidade para respostas técnicas em CPU.

---

# 💬 Integração com AI Gateway

Gateway:

```
10.0.0.139
```

Fluxo:

```
pergunta
 ↓
AI Gateway
 ↓
DocAI search
 ↓
contexto técnico
 ↓
Ollama
 ↓
resposta final
```

---

# 🧪 Monitoramento

Ver crescimento do banco vetorial:

```
watch -n 10 du -sh /opt/doc-ai/vector_db
```

Ver uso de CPU:

```
top
```

ou

```
htop
```

---

# 📚 Documentação do Sistema DocAI

A documentação detalhada está no diretório **doc/**.

### Sistema de Indexação

🔗 doc/Doc-AI-PDF-Indexer.md

### Migração de Embeddings

🔗 doc/Doc-AI-migracao-nomic-embed-text.md

### Interface Web

🔗 doc/Doc-AI–InterfaceWeb.md

### Frontend

🔗 doc/Doc-Ai-frontend.md

### AI Gateway

🔗 doc/Doc-Ai-iniciar-gateway.md
🔗 doc/Doc-Ai-iniciar-gateway%20-v0.1.md

### API DocAI como Serviço

🔗 doc/DocAI%20-API-systemd.md

### Documentação Histórica

🔗 doc/README-V0.1.md

---

Se quiser, no próximo passo posso também te gerar **3 melhorias muito úteis para esse repositório**:

1️⃣ **Diagrama visual da arquitetura (SVG para GitHub)**
2️⃣ **Badges profissionais no topo do README**
3️⃣ **Seção "Quick Start (5 minutos)"** para quem clonar o projeto.
