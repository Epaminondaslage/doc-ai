
# Vamos iniciar o gateway Ai 

No servidor **10.0.0.139**, execute exatamente esta sequência:

### 1️⃣ Ir para o projeto

```bash
cd /opt/sentinela/ai-gateway
```

---

### 2️⃣ Ativar o ambiente virtual

```bash
source venv/bin/activate
```

O prompt deve ficar assim:

```text
(venv) epaminondas@homeassistant:/opt/sentinela/ai-gateway$
```

---

### 3️⃣ Iniciar o servidor

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Você deve ver algo parecido com:

```text
INFO:     Started server process
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

⚠️ **Deixe essa janela aberta**.

---

# Depois disso

Abra outro terminal e teste:

```bash
curl http://10.0.0.139:8000
```

Resposta esperada:

```json
{"status":"Sentinela AI Gateway ativo"}
```

---

