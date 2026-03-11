

# DocAI — Sistema de Consulta Inteligente de Biblioteca Técnica

Sistema de **indexação e consulta semântica de documentos técnicos** utilizando **RAG (Retrieval Augmented Generation)** rodando **100% local**.

O sistema transforma uma coleção de documentos técnicos em um **assistente técnico pesquisável**, capaz de responder perguntas utilizando conhecimento presente nos próprios documentos.

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

```bash
mkdir -p /opt/doc-ai
cd /opt/doc-ai
```

---

# 🐍 Criar ambiente virtual Python

```bash
python3 -m venv venv
```

Ativar:

```bash
source venv/bin/activate
```

---

# 📦 Instalar dependências

```bash
pip install langchain
pip install chromadb
pip install pypdf
pip install sentence-transformers
pip install langchain-text-splitters
pip install fastapi
pip install uvicorn
```

---

# 📦 Dependências adicionais (OCR e criptografia)

Alguns PDFs utilizam criptografia AES e outros exigem OCR.

Dependências Python:

```bash
pip install cryptography
pip install pytesseract
pip install pdf2image
pip install pillow
```

Dependências do sistema:

```bash
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-por
sudo apt install poppler-utils
```

---

# 📚 Transferência da Biblioteca

Transferência realizada com:

```bash
rsync -avh --progress epaminondas@10.0.0.5:/var/www/html/Biblioteca/ /opt/doc-ai/pdfs/
```

Verificação:

```bash
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

Características:

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
/opt/doc-ai/scripts/index_pdfs.py
```

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

Campos armazenados:

| Campo   | Descrição            |
| ------- | -------------------- |
| arquivo | nome do PDF          |
| pagina  | página do documento  |
| caminho | localização completa |

Isso permite **respostas com referência precisa da fonte**.

---

# ▶️ Executar Indexação

Ativar ambiente:

```bash
source /opt/doc-ai/venv/bin/activate
```

Executar:

```bash
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

A API fornece busca semântica.

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

```bash
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

O gateway roda no servidor:

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

```bash
watch -n 10 du -sh /opt/doc-ai/vector_db
```

Ver uso de CPU:

```bash
top
```

ou

```bash
htop
```

---

Perfeito. Vou montar o **índice com links clicáveis para o GitHub**, usando o caminho real do seu repositório:

```
https://github.com/Epaminondaslage/doc-ai
```

Assim você pode **copiar e colar direto no README.md**.

---

# 📚 Documentação do Sistema DocAI

A documentação detalhada do sistema está organizada no diretório **`doc/`** deste repositório.

Cada documento descreve um componente específico da arquitetura **DocAI + AI Gateway + RAG + Ollama**.

---

# 📑 Índice da Documentação

## 🧠 Sistema de Indexação

Documentação do processo de leitura dos PDFs, geração de embeddings e armazenamento no banco vetorial.

📄 **Indexador de PDFs**

Explica como funciona:

* pipeline de extração
* OCR automático
* divisão em chunks
* geração de embeddings
* armazenamento vetorial

🔗
[https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-AI-PDF-Indexer.md](https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-AI-PDF-Indexer.md)

---

# 🧠 Migração de Embeddings

Documentação da migração do modelo de embeddings utilizado no sistema.

📄 **Migração para Nomic Embed Text**

Este documento explica:

* mudança do modelo de embeddings
* impacto na qualidade da busca
* reindexação da biblioteca

🔗
[https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-AI-migracao-nomic-embed-text.md](https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-AI-migracao-nomic-embed-text.md)

---

# 🌐 Interface Web do DocAI

Documentação da interface web para consulta da biblioteca técnica.

📄 **Interface Web do DocAI**

Inclui:

* interface de busca
* visualização de resultados
* navegação entre documentos

🔗
[https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-AI–InterfaceWeb.md](https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-AI–InterfaceWeb.md)

---

# 🖥️ Frontend do Sistema

Documentação da camada de frontend da aplicação.

📄 **Frontend do DocAI**

Explica:

* estrutura HTML
* integração com a API
* funcionamento da interface

🔗
[https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-Ai-frontend.md](https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-Ai-frontend.md)

---

# 🧠 AI Gateway

Documentação do gateway que conecta o DocAI ao sistema Sentinela e aos modelos LLM.

---

📄 **Inicialização do AI Gateway**

Versão atual do processo de inicialização.

🔗
[https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-Ai-iniciar-gateway.md](https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-Ai-iniciar-gateway.md)

---

📄 **Inicialização do AI Gateway (versão v0.1)**

Versão inicial utilizada durante os primeiros testes do sistema.

🔗
[doc/Doc-Ai-iniciar-gateway%20-v0.1.md](doc/Doc-Ai-iniciar-gateway%20-v0.1.md)

---

# ⚙️ API DocAI como Serviço

Documentação da execução da API como serviço do sistema utilizando **systemd**.

📄 **DocAI API Service**

Explica:

* criação do serviço
* inicialização automática
* monitoramento do processo

🔗
[https://github.com/Epaminondaslage/doc-ai/blob/main/doc/DocAI%20-API-systemd.md](https://github.com/Epaminondaslage/doc-ai/blob/main/doc/DocAI%20-API-systemd.md)

---

# 📘 Documentação Histórica

Versão inicial do README do projeto.

📄 **README versão 0.1**

🔗
[https://github.com/Epaminondaslage/doc-ai/blob/main/doc/README-V0.1.md](https://github.com/Epaminondaslage/doc-ai/blob/main/doc/README-V0.1.md)

---

# 🧭 Estrutura da Documentação

```
doc/

Doc-AI-PDF-Indexer.md
Doc-AI-migracao-nomic-embed-text.md
Doc-AI–InterfaceWeb.md
Doc-Ai-frontend.md
Doc-Ai-iniciar-gateway.md
Doc-Ai-iniciar-gateway -v0.1.md
DocAI -API-systemd.md
README-V0.1.md
```

---

# 🔎 Ordem recomendada de leitura

Para entender completamente o sistema:

1️⃣ Indexação da biblioteca
[https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-AI-PDF-Indexer.md](https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-AI-PDF-Indexer.md)

2️⃣ Migração de embeddings
[https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-AI-migracao-nomic-embed-text.md](https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-AI-migracao-nomic-embed-text.md)

3️⃣ API DocAI como serviço
[https://github.com/Epaminondaslage/doc-ai/blob/main/doc/DocAI%20-API-systemd.md](https://github.com/Epaminondaslage/doc-ai/blob/main/doc/DocAI%20-API-systemd.md)

4️⃣ Inicialização do Gateway
[https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-Ai-iniciar-gateway.md](https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-Ai-iniciar-gateway.md)

5️⃣ Interface Web
[https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-AI–InterfaceWeb.md](https://github.com/Epaminondaslage/doc-ai/blob/main/doc/Doc-AI–InterfaceWeb.md)

---

