
# DocAI — Execução da API como Serviço (systemd)

## Visão Geral

Para garantir que a API do **DocAI** permaneça ativa mesmo após reinicializações do servidor ou fechamento do terminal, ela deve ser executada como um **serviço do systemd**.

Isso permite:

* iniciar automaticamente com o sistema
* reiniciar automaticamente se ocorrer falha
* executar em background
* gerenciamento centralizado via `systemctl`

---

# Arquitetura do Serviço

O serviço executa a API Python usando **Uvicorn**, que expõe o endpoint de busca para o backend PHP.

Fluxo do sistema:

```
Usuário
   │
   ▼
Apache (index.html)
   │
   ▼
search.php
   │
   ▼
DocAI API (systemd)
   │
   ▼
ChromaDB
   │
   ▼
Biblioteca de PDFs
```

---

# Localização da API

A API está localizada em:

```
/opt/doc-ai/api/docai_api.py
```

O ambiente Python usado:

```
/opt/doc-ai/venv
```

O banco vetorial:

```
/opt/doc-ai/vector_db
```

---

# Arquivo do Serviço

Criar o arquivo:

```
/etc/systemd/system/docai.service
```

Conteúdo do serviço:

```
[Unit]
Description=DocAI API
After=network.target

[Service]

User=epaminondas
WorkingDirectory=/opt/doc-ai

ExecStart=/opt/doc-ai/venv/bin/uvicorn api.docai_api:app --host 127.0.0.1 --port 5005

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Descrição dos parâmetros:

| Parâmetro        | Função                           |
| ---------------- | -------------------------------- |
| User             | usuário que executa a API        |
| WorkingDirectory | diretório base da aplicação      |
| ExecStart        | comando que inicia o servidor    |
| Restart          | reinicia automaticamente se cair |
| RestartSec       | intervalo antes de reiniciar     |

---

# Atualizar o systemd

Após criar ou alterar o serviço, atualizar o systemd:

```
sudo systemctl daemon-reload
```

---

# Ativar o serviço no boot

Para iniciar automaticamente quando o servidor ligar:

```
sudo systemctl enable docai
```

---

# Iniciar o serviço

Executar:

```
sudo systemctl start docai
```

---

# Verificar o status

```
sudo systemctl status docai
```

Saída esperada:

```
docai.service - DocAI API
Loaded: loaded (/etc/systemd/system/docai.service)
Active: active (running)
```

---

# Verificar logs do serviço

Caso ocorra erro durante a inicialização:

```
journalctl -u docai -n 50
```

Para acompanhar logs em tempo real:

```
journalctl -u docai -f
```

---

# Reiniciar o serviço

Se o código da API for alterado:

```
sudo systemctl restart docai
```

---

# Parar o serviço

```
sudo systemctl stop docai
```

---

# Testar funcionamento da API

Depois que o serviço estiver ativo, testar via terminal:

```
curl "http://127.0.0.1:5005/search?q=arduino"
```

Exemplo de resposta:

```
{
 "query":"arduino",
 "results":[
   {
     "arquivo":"Arduino completo.pdf",
     "pagina":30,
     "trecho":"plataforma Arduino",
     "score":0.71
   }
 ]
}
```

---

# Porta utilizada

A API escuta em:

```
127.0.0.1:5005
```

Isso significa:

* acessível apenas localmente
* protegido da rede externa
* utilizado pelo backend PHP

---

# Integração com o Front-End

A interface web consulta a API através do arquivo:

```
/var/www/html/docai/src/search.php
```

O PHP envia requisições para:

```
http://127.0.0.1:5005/search
```

---

# Manutenção

Após alterações no código da API:

```
sudo systemctl restart docai
```

Para verificar se o serviço iniciou corretamente:

```
sudo systemctl status docai
```

---

# Estrutura do Projeto

```
/opt/doc-ai
│
├── api
│   └── docai_api.py
│
├── pdfs
│
├── scripts
│   └── index_pdfs_v5_1.py
│
├── vector_db
│   └── chroma.sqlite3
│
└── venv
```

---

# Observações

* O serviço depende do ambiente virtual Python localizado em `/opt/doc-ai/venv`
* O banco vetorial deve estar previamente indexado
* O Apache deve estar ativo para servir a interface web

---

# Resultado Final

Após a ativação do serviço:

* a API inicia automaticamente
* consultas podem ser feitas pela interface web
* o sistema DocAI fica permanentemente disponível no servidor

---

