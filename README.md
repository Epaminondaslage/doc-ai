
# DocAI — Sistema de Consulta Inteligente de Biblioteca Técnica

Sistema de **indexação e consulta semântica de documentos técnicos utilizando RAG (Retrieval Augmented Generation)** rodando **100% local**.

O sistema permite transformar uma coleção de documentos em um **assistente técnico pesquisável**, capaz de responder perguntas técnicas utilizando documentos da própria biblioteca.

---

# 🎯 Objetivo

Permitir:

* indexar bibliotecas grandes de documentos
* criar embeddings semânticos
* buscar conhecimento técnico
* integrar com modelos locais (LLM)
* operar completamente **offline**

---

# 🖥️ Infraestrutura

Servidor principal:

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

Biblioteca técnica:

```
1063 PDFs
≈22GB
```

Origem da biblioteca:

```
10.0.0.5:/var/www/html/Biblioteca
```

Destino:

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
                       |
                       v
               +----------------+
               | Indexador PDF  |
               | Python Script  |
               +-------+--------+
                       |
                       |
                       v
               +----------------+
               |   ChromaDB     |
               | Banco Vetorial |
               +-------+--------+
                       |
                       |
                       v
               +----------------+
               |  Sistema RAG   |
               +-------+--------+
                       |
         +-------------+-------------+
         |                           |
         v                           v
   +------------+              +-------------+
   | Ollama CLI |              | OpenWebUI   |
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

# 🔎 Pipeline de Indexação Atualizado (com OCR)

Alguns documentos da biblioteca são **PDFs escaneados** (imagem).

Nestes casos o sistema executa **OCR automático**.

Pipeline atualizado:

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

# 🐍 Criar ambiente virtual Python

```
python3 -m venv venv
```

Ativar:

```
source venv/bin/activate
```

---

# 📦 Instalar dependências

```
pip install langchain
pip install chromadb
pip install pypdf
pip install sentence-transformers
pip install langchain-text-splitters
```

---

# 📦 Dependências adicionais (OCR e criptografia)

Alguns PDFs utilizam **criptografia AES** e outros exigem **OCR**.

Dependências extras:

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

Resultado:

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
* boa qualidade sem necessidade de GPU

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
* dividir conteúdo
* gerar embeddings
* armazenar metadados
* tratar PDFs criptografados

---

# 🧾 Metadados Indexados

O sistema indexa metadados para cada trecho.

Estrutura:

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

Esses dados permitem gerar respostas com **fonte e referência precisa**.

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

# 🔍 Consulta Semântica

Exemplos de perguntas possíveis:

```
o que diz a NBR5410 sobre aterramento
```

```
explique funcionamento de inversor de frequência
```

```
quais documentos falam sobre redes de computadores
```

---

# 🤖 Modelos LLM

Servidor Ollama.

Modelos instalados:

```
tinyllama
tinyllama-fast
qwen2.5:0.5b
```

Recomendado:

```
qwen2.5
```

Melhor qualidade para respostas técnicas.

---

# 💬 Integração com OpenWebUI

OpenWebUI pode utilizar o banco vetorial para:

* chat com documentos
* busca técnica
* consulta semântica
* respostas com referência de fonte

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

# ⚠️ Limitações

Alguns PDFs podem estar:

* protegidos
* criptografados
* corrompidos

Nestes casos o indexador ignora o documento.

---

# 🚀 Resultado Final

O sistema transforma a biblioteca em um:

**Assistente técnico inteligente local**

Capaz de consultar conhecimento sobre:

* eletrônica
* instalações elétricas
* automação
* programação
* normas técnicas

---

# 📈 Possíveis Evoluções

Melhorias futuras:

* indexação incremental automática
* API de consulta REST
* interface web dedicada
* ranking de relevância
* múltiplos modelos de embeddings
* cache de respostas

---

```
