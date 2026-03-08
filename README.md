
# 📚 DocAI — Sistema de Consulta Inteligente de Biblioteca Técnica

Sistema de **indexação e consulta semântica de documentos técnicos** utilizando **RAG (Retrieval Augmented Generation)** rodando **100% local**.

O sistema permite transformar uma coleção de documentos em um **assistente técnico pesquisável**.

---

# 🎯 Objetivo

Permitir:

* indexar bibliotecas grandes de documentos
* criar embeddings semânticos
* buscar conhecimento técnico
* integrar com modelos locais (LLM)
* operar **offline**

---

# 🖥️ Infraestrutura

Servidor principal:

```text
10.0.0.37
```

Sistema operacional:

```text
Ubuntu Linux
```

Hardware:

```text
CPU only
```

Biblioteca técnica:

```text
1063 PDFs
≈22GB
```

Origem:

```text
10.0.0.5:/var/www/html/Biblioteca
```

Destino:

```text
/opt/doc-ai/pdfs
```

---

# 📁 Estrutura do Projeto

```text
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

```text
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

```text
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

```text
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

# 🧩 Pipeline RAG

```text
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
```

Dependências utilizadas:

| Biblioteca               | Função           |
| ------------------------ | ---------------- |
| langchain                | ferramentas RAG  |
| chromadb                 | banco vetorial   |
| pypdf                    | leitura de PDF   |
| sentence-transformers    | embeddings       |
| langchain-text-splitters | divisão de texto |

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

Resultado:

```text
1063
```

---

# 🧠 Modelo de Embeddings

Modelo utilizado:

```text
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

---

# 🧩 Script de Indexação

Localização:

```text
/opt/doc-ai/scripts/index_pdfs.py
```

Responsabilidades:

* percorrer biblioteca
* extrair texto
* dividir conteúdo
* gerar embeddings
* armazenar metadados

---

# 🧾 Metadados Indexados

O sistema também indexa metadados para cada trecho.

Estrutura:

```json
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

Esses dados permitem gerar respostas com **fonte e referência**.

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

```text
1063 PDFs
≈22GB
CPU only
```

Tempo esperado:

```text
40 minutos a 2 horas
```

---

# 🗂️ Banco Vetorial

Local:

```text
/opt/doc-ai/vector_db
```

Contém:

* embeddings
* texto indexado
* metadados

---

# 🔍 Consulta Semântica

Exemplos de perguntas possíveis:

```text
o que diz a NBR5410 sobre aterramento
```

```text
explique funcionamento de inversor de frequência
```

```text
quais documentos falam sobre redes de computadores
```

---

# 🤖 Modelos LLM

Servidor Ollama:

Modelos instalados:

```text
tinyllama
tinyllama-fast
qwen2.5:0.5b
```

Recomendado:

```text
qwen2.5
```

---

# 💬 Integração com OpenWebUI

OpenWebUI pode utilizar o banco vetorial para:

* chat com documentos
* busca técnica
* consulta semântica

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

# ⚠️ Limitações

PDFs escaneados podem não conter texto.

Nestes casos seria necessário:

```text
OCR (Tesseract)
```

---

# 🚀 Resultado Final

O sistema transforma a biblioteca em um:

```text
Assistente técnico inteligente
```

Capaz de consultar conhecimento sobre:

* eletrônica
* instalações elétricas
* automação
* programação
* normas técnicas

---

# 📈 Possíveis Evoluções

Melhorias futuras:

* OCR automático
* indexação incremental
* API de consulta
* interface web dedicada
* ranking de relevância
* integração com múltiplos LLMs

---

# 🧑‍💻 Autor

Projeto construído para ambiente de laboratório técnico e automação de conhecimento local.

