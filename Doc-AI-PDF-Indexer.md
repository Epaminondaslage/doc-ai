# Doc-AI PDF Indexer   index_pdfs_v2.py   versão melhorada

## Descrição

O **Doc-AI PDF Indexer** é um script em Python responsável por **processar arquivos PDF e gerar embeddings vetoriais** para uso em sistemas de **RAG (Retrieval Augmented Generation)**, motores de busca semânticos ou chatbots baseados em documentos.

O sistema:

* percorre recursivamente um diretório de PDFs
* extrai o texto das páginas
* aplica OCR automaticamente quando necessário
* divide o conteúdo em trechos (chunks)
* gera embeddings utilizando **SentenceTransformers**
* armazena os vetores em um **banco vetorial ChromaDB**

O script também possui:

* retomada automática de indexação
* registro de PDFs já processados
* parada segura com `CTRL+C`
* persistência automática do banco vetorial

---

# Estrutura do Projeto

Exemplo de estrutura recomendada:

```
/opt/doc-ai
│
├── pdfs/                # Diretório contendo os PDFs
│
├── scripts/
│   └── index_pdfs.py    # Script de indexação
│
├── vector_db/           # Banco vetorial (ChromaDB)
│
├── indexados.txt        # Controle de PDFs já indexados
│
└── venv/                # Ambiente virtual Python
```

---

# Requisitos

Sistema operacional:

* Linux (Ubuntu recomendado)

Python:

* Python 3.10 ou superior

Bibliotecas necessárias:

```
pypdf
sentence-transformers
langchain-text-splitters
chromadb
pytesseract
pdf2image
torch
```

---

# Instalação

Criar diretório do projeto:

```
sudo mkdir -p /opt/doc-ai
```

Criar ambiente virtual:

```
python3 -m venv /opt/doc-ai/venv
```

Ativar o ambiente virtual:

```
source /opt/doc-ai/venv/bin/activate
```

Instalar dependências:

```
pip install pypdf sentence-transformers langchain-text-splitters chromadb pytesseract pdf2image torch
```

Instalar dependências do sistema:

```
sudo apt install tesseract-ocr
sudo apt install poppler-utils
```

---

# Configuração

No script `index_pdfs.py`, verifique os caminhos principais:

```
PDF_DIR = "/opt/doc-ai/pdfs"
DB_DIR = "/opt/doc-ai/vector_db"
INDEX_FILE = "/opt/doc-ai/indexados.txt"
```

Onde:

| Variável   | Descrição                                  |
| ---------- | ------------------------------------------ |
| PDF_DIR    | diretório contendo os PDFs                 |
| DB_DIR     | diretório onde o banco vetorial será salvo |
| INDEX_FILE | lista de PDFs já indexados                 |

---

# Execução

Entrar no ambiente virtual:

```
source /opt/doc-ai/venv/bin/activate
```

Executar o indexador:

```
python /opt/doc-ai/scripts/index_pdfs.py
```

---

# Funcionamento do Processo

Para cada PDF o sistema executa:

1. leitura do documento
2. extração de texto página a página
3. OCR automático caso não haja texto
4. divisão do texto em blocos (chunks)
5. geração de embeddings
6. armazenamento no banco vetorial

Cada trecho é identificado por um **hash único**, evitando duplicações.

---

# Retomada Automática

O arquivo:

```
/opt/doc-ai/indexados.txt
```

contém a lista de PDFs já processados.

Se o script for interrompido, ao executar novamente ele **continua do ponto onde parou**.

Exemplo:

```
Já indexado: /opt/doc-ai/pdfs/livro1.pdf
Já indexado: /opt/doc-ai/pdfs/livro2.pdf
Indexando: /opt/doc-ai/pdfs/livro3.pdf
```

---

# Parada Segura

Durante a execução é possível interromper o processo com:

```
CTRL + C
```

O sistema irá:

1. salvar o banco vetorial
2. manter o progresso atual
3. encerrar o processo com segurança

---

# Saída do Programa

Ao final da execução são exibidas estatísticas:

```
===============================
Indexação concluída
===============================

PDFs indexados nesta execução: 45
Trechos criados: 18234
Páginas processadas com OCR: 210
PDFs com erro: 2
Total de PDFs registrados: 145
```

---

# Banco Vetorial

O banco é armazenado em:

```
/opt/doc-ai/vector_db
```

Tecnologia utilizada:

**ChromaDB**

Cada registro contém:

* trecho de texto
* embedding vetorial
* nome do arquivo
* página de origem
* caminho completo do documento

---

# Performance

Tempo médio de indexação:

| Tipo de PDF | Tempo aproximado |
| ----------- | ---------------- |
| PDF pequeno | 2–10 segundos    |
| Livro médio | 1–3 minutos      |
| PDF com OCR | 3–10 minutos     |

A indexação inicial pode levar **várias horas** dependendo da quantidade de documentos.

---

# Avisos Importantes

OCR é automaticamente ativado quando o PDF não possui texto selecionável.

PDFs criptografados podem ser ignorados caso não possam ser descriptografados.

Arquivos corrompidos podem gerar mensagens como:

```
EOF marker not found
```
---

## Servidor de instalação:

```
10.0.0.37
```

Diretório principal:

```
/opt/doc-ai
```

