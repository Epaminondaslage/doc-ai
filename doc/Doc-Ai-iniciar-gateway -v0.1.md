
# README — Ativação do **DocAI API Server**

Servidor: **10.0.0.37**

Este documento explica como iniciar e manter ativo o servidor **DocAI**, responsável por fornecer busca semântica nos PDFs para o sistema Sentinela.

Arquitetura:

```
AI Gateway (10.0.0.139)
        ↓
DocAI API (10.0.0.37:5005)
        ↓
Banco vetorial dos PDFs
        ↓
Resultados RAG
```

---

# 1. Acessar o servidor

Conectar via SSH:

```bash
ssh epaminondas@10.0.0.37
```

---

# 2. Diretório do projeto

Ir para o diretório do DocAI:

```bash
cd /opt/doc-ai
```

Estrutura esperada:

```
/opt/doc-ai

api/
scripts/
pdfs/
index/
venv/
```

---

# 3. Ativar ambiente Python

Ativar o ambiente virtual:

```bash
source venv/bin/activate
```

Se ativado corretamente o terminal ficará assim:

```
(venv) epaminondas@Ubuntu-desktop:/opt/doc-ai$
```

---

# 4. Verificar se o serviço está rodando

Executar:

```bash
ss -lntp | grep 5005
```

Se estiver ativo aparecerá:

```
LISTEN 0 2048 0.0.0.0:5005
```

---

# 5. Iniciar manualmente (modo teste)

Caso precise iniciar manualmente:

```bash
uvicorn api.docai_api:app --host 0.0.0.0 --port 5005
```

Mensagem esperada:

```
Uvicorn running on http://0.0.0.0:5005
```

---

# 6. Testar API

Testar no próprio servidor:

```bash
curl http://localhost:5005/docs
```

ou

```bash
curl http://localhost:5005/search?q=teste
```

Exemplo de resposta:

```json
{
 "query": "teste",
 "results": [...]
}
```

---

# 7. Criar serviço automático (systemd)

Arquivo do serviço:

```
/etc/systemd/system/docai.service
```

Criar ou editar:

```bash
sudo nano /etc/systemd/system/docai.service
```

Conteúdo:

```ini
[Unit]
Description=DocAI API
After=network.target

[Service]
User=epaminondas
WorkingDirectory=/opt/doc-ai

ExecStart=/opt/doc-ai/venv/bin/uvicorn api.docai_api:app --host 0.0.0.0 --port 5005

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

# 8. Recarregar systemd

```bash
sudo systemctl daemon-reload
```

---

# 9. Iniciar serviço

```bash
sudo systemctl start docai
```

---

# 10. Habilitar auto start

```bash
sudo systemctl enable docai
```

Assim o DocAI inicia automaticamente quando o servidor reiniciar.

---

# 11. Verificar status

```bash
sudo systemctl status docai
```

Exemplo esperado:

```
docai.service - DocAI API
Active: active (running)
```

---

# 12. Verificar logs

Caso ocorra erro:

```bash
journalctl -u docai -f
```

---

# 13. Teste remoto

De outro servidor da rede:

```bash
curl http://10.0.0.37:5005/search?q=arduino
```

Resposta esperada:

```
JSON com resultados do PDF
```

---

# 14. Porta utilizada

```
5005
```

Caso exista firewall:

```bash
sudo ufw allow 5005
```

---

# 15. Integração com o AI Gateway

Servidor:

```
10.0.0.139
```

Endpoint usado pelo gateway:

```
http://10.0.0.37:5005/search?q=pergunta
```

---

# 16. Estrutura do DocAI

```
/opt/doc-ai

api/
   docai_api.py

scripts/
   index_pdfs_v6.py

pdfs/
   (biblioteca técnica)

index/
   (vetores)

venv/
```

---

# 17. Reindexar PDFs

Caso novos PDFs sejam adicionados:

```bash
cd /opt/doc-ai
source venv/bin/activate

python scripts/index_pdfs_v6.py
```

---

# 18. Monitorar indexação

Ver processo:

```bash
top
```

ou

```bash
ps aux | grep index_pdfs
```

---

# 19. Teste completo do sistema

Fluxo final:

```
OpenWebUI
     ↓
AI Gateway
     ↓
DocAI
     ↓
Ollama
     ↓
Resposta
```

---

# 20. Comandos rápidos

Ver serviço:

```bash
systemctl status docai
```

Reiniciar:

```bash
sudo systemctl restart docai
```

Logs:

```bash
journalctl -u docai -f
```

---
