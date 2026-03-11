

# DocAI   versão 0.1

## Sistema de Consulta Inteligente de Biblioteca Técnica

Sistema de **indexação e consulta semântica de documentos técnicos** baseado em **RAG (Retrieval Augmented Generation)** operando **100% local**, sem dependência de serviços externos.

O sistema transforma uma biblioteca de documentos em um **assistente técnico capaz de responder perguntas com base no conteúdo dos arquivos**.

---

## Visão Geral

DocAI permite:

* indexar bibliotecas grandes de documentos técnicos
* realizar busca semântica
* responder perguntas técnicas
* citar fontes e páginas dos documentos
* operar totalmente offline
* integrar com LLMs locais

A arquitetura foi projetada para **CPU only**, permitindo execução em hardware simples.

---

## Arquitetura Geral

```
Biblioteca de PDFs
        │
        ▼
  Indexador Python
        │
        ▼
   ChromaDB
(banco vetorial)
        │
        ▼
 Sistema RAG
        │
 ┌──────┴──────┐
 ▼             ▼
Ollama CLI   OpenWebUI
```

---

## Infraestrutura

Servidor principal

```
10.0.0.37
```

Sistema operacional

```
Ubuntu Linux
```

Hardware

```
CPU only
```

Biblioteca técnica

```
1063 PDFs
≈22GB
```

Origem

```
10.0.0.5:/var/www/html/Biblioteca
```

Destino

```
/opt/doc-ai/pdfs
```

---

## Estrutura do Projeto

```
/opt/doc-ai
│
├── pdfs
│   Biblioteca completa
│
├── scripts
│   index_pdfs.py
│
├── vector_db
│   Banco vetorial ChromaDB
│
├── venv
│   ambiente Python
│
└── README.md
```

---

## Arquitetura de IA

DocAI utiliza **RAG (Retrieval Augmented Generation)**.

Fluxo:

```
Pergunta do usuário
        │
        ▼
Embedding da pergunta
        │
        ▼
Busca vetorial (ChromaDB)
        │
        ▼
Trechos relevantes
        │
        ▼
LLM (Ollama)
        │
        ▼
Resposta com fonte
```

---

## Pipeline de Indexação

```
PDF
 │
 ▼
Extração de texto
(pypdf)
 │
 ▼
OCR automático
(Tesseract)
 │
 ▼
Divisão em chunks
 │
 ▼
Embeddings
(SentenceTransformers)
 │
 ▼
Armazenamento
(ChromaDB)
```

---

## Pipeline OCR

Alguns PDFs são escaneados.

Nestes casos:

```
PDF
 │
 ▼
Sem texto detectado
 │
 ▼
OCR
 │
 ▼
Texto recuperado
```

Isso permite indexar:

* revistas digitalizadas
* apostilas escaneadas
* manuais antigos

---

## Banco Vetorial

Local:

```
/opt/doc-ai/vector_db
```

Contém:

* embeddings
* texto indexado
* metadados

Cada chunk contém:

```
texto
embedding
arquivo
pagina
caminho
```

Exemplo de metadado

```
{
 "arquivo": "NBR5410.pdf",
 "pagina": 114,
 "caminho": "/opt/doc-ai/pdfs/Instalações Elétricas/NBR5410.pdf"
}
```

---

## Modelo de Embeddings

Modelo utilizado

```
sentence-transformers/all-MiniLM-L6-v2
```

Características

| Propriedade | Valor          |
| ----------- | -------------- |
| Dimensão    | 384            |
| RAM         | baixa          |
| Velocidade  | alta           |
| Qualidade   | ótima para CPU |

Motivo da escolha

* ótimo custo-benefício
* rápido para bibliotecas grandes
* compatível com CPU

---

# Modelos LLM

Servidor Ollama

Modelos instalados

```
tinyllama
tinyllama-fast
qwen2.5:0.5b
```

Modelo recomendado

```
qwen2.5
```

---

## Preparação do Ambiente

Criar diretório

```
mkdir -p /opt/doc-ai
cd /opt/doc-ai
```

---

## Criar ambiente virtual

```
python3 -m venv venv
```

Ativar

```
source venv/bin/activate
```

---

# Instalar dependências

```
pip install langchain
pip install chromadb
pip install pypdf
pip install sentence-transformers
pip install langchain-text-splitters
```

Dependências adicionais

```
pip install cryptography
pip install pytesseract
pip install pdf2image
pip install pillow
```

Dependências do sistema

```
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-por
sudo apt install poppler-utils
```

---

## Transferência da Biblioteca

Transferência via rsync

```
rsync -avh --progress epaminondas@10.0.0.5:/var/www/html/Biblioteca/ /opt/doc-ai/pdfs/
```

Verificação

```
find /opt/doc-ai/pdfs -type f -iname "*.pdf" | wc -l
```

Resultado

```
1063
```

---

## Execução da Indexação

Ativar ambiente

```
source /opt/doc-ai/venv/bin/activate
```

Executar

```
python /opt/doc-ai/scripts/index_pdfs.py
```

---

## Monitoramento

Ver crescimento do banco vetorial

```
watch -n 10 du -sh /opt/doc-ai/vector_db
```

Monitorar CPU

```
top
```

ou

```
htop
```


---

## Exemplos de Perguntas

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

## Resultado Final

O sistema transforma a biblioteca em um:

**Assistente técnico inteligente**

Capaz de consultar conhecimento sobre

* eletrônica
* instalações elétricas
* automação
* programação
* normas técnicas
* redes de computadores

## Executar o indexador com tmux

```
epaminondas@Ubuntu-desktop:~$ pwd
/home/epaminondas
epaminondas@Ubuntu-desktop:~$ ls tmux-docai.sh 
tmux-docai.sh```
```

## ver o que voi feito enter comandos  de status.sh

```
epaminondas@Ubuntu-desktop:/opt/doc-ai$ ls
api  index_checkpoint.txt  index_status.log  logs  pdfs  scripts  status.sh  vector_db  venv
epaminondas@Ubuntu-desktop:/opt/doc-ai$ pwd
/opt/doc-ai
epaminondas@Ubuntu-desktop:/opt/doc-ai$ ls
api  index_checkpoint.txt  index_status.log  logs  pdfs  scripts  status.sh  vector_db  venv
epaminondas@Ubuntu-desktop:/opt/doc-ai$ ./status.sh 

========================================
        Status da Indexação DocAI
========================================

Data atual        : 2026-03-11 06:21:02
PDFs biblioteca   : 1063
PDFs indexados    : 281
PDFs restantes    : 782
Progresso         : 26 %

Novos PDFs        : 0
Tempo decorrido   : 10 min
Velocidade        : 0 PDFs/hora

Histórico salvo em:
/opt/doc-ai/index_status.log

```
## Ajuda tmux

```
epaminondas@Ubuntu-desktop:/opt/doc-ai$ cd /home/epaminondas/
epaminondas@Ubuntu-desktop:~$ cat help-tmux.txt 

##############################################################
TMUX - GUIA RÁPIDO
Multiplexador de terminal para Linux
###############################################################
O tmux permite criar múltiplos terminais dentro de um único
terminal e manter processos rodando mesmo após fechar o SSH.

É muito útil para:

- indexação de documentos, execução de scripts longos, monitoramento
 de logs, administração remota de servidores.
===============================================================
1 - INSTALAÇÃO
===============================================================
Instalar tmux:

sudo apt install tmux
===============================================================
2 - CRIAR UMA SESSÃO
===============================================================
Criar uma nova sessão chamada "docai":

tmux new -s docai

Agora você está dentro da sessão tmux.
===============================================================
3 - SAIR DA SESSÃO SEM PARAR OS PROCESSOS
===============================================================
Pressione:

CTRL + B
D

Isso faz o "detach".  A sessão continua rodando em segundo plano.
===============================================================
4 - LISTAR SESSÕES ATIVAS
===============================================================
tmux ls
Exemplo de saída:

0: docai (Detached)
===============================================================
5 - VOLTAR PARA UMA SESSÃO
===============================================================
tmux attach -t docai
===============================================================
6 - FECHAR UMA SESSÃO
===============================================================
Dentro do tmux:
exit
ou
CTRL + D
===============================================================
7 - DIVIDIR A TELA
===============================================================
Dividir horizontal:
CTRL + B
"

Dividir vertical:
CTRL + B
%
===============================================================
8 - MUDAR ENTRE PAINÉIS
===============================================================
CTRL + B
seta para cima / baixo / esquerda / direita
===============================================================
9 - ANEXAR SESSÃO
===============================================================
tmux attach -t nome
===============================================================
10 - MATAR UMA SESSÃO
===============================================================
tmux kill-session -t nome
===============================================================

```

---
