
# DocAI — Migração para Embeddings `nomic-embed-text`

### Procedimento pós-indexação

Este documento descreve o procedimento para **atualizar o mecanismo de embeddings do DocAI** para o modelo `nomic-embed-text`, melhorando significativamente a qualidade da busca semântica.

Este procedimento **deve ser executado apenas após o término da indexação atual**, para evitar inconsistência entre vetores gerados por modelos diferentes.

---

# 1. Situação atual

O DocAI está executando atualmente:

```
PDF
 ↓
extração de texto
 ↓
chunk
 ↓
embedding (modelo atual)
 ↓
ChromaDB
```

Durante a indexação atual **não devemos alterar o modelo de embedding**, pois isso geraria vetores incompatíveis dentro do mesmo banco.

Exemplo do problema:

```
documento A → embedding modelo antigo
documento B → embedding nomic-embed-text
```

Isso quebra a busca vetorial.

Portanto:

**A indexação atual deve terminar completamente antes da migração.**

---

# 2. Verificar término da indexação

Confirmar que o indexador terminou.

Exemplo de verificação:

```
ps aux | grep index
```

ou observar logs do indexador.

---

# 3. Verificar instalação do modelo de embeddings

Confirmar que o modelo já está disponível no Ollama.

```
ollama list
```

Resultado esperado:

```
nomic-embed-text
tinyllama
qwen2.5
```

Caso não esteja presente:

```
ollama pull nomic-embed-text
```

---

# 4. Backup do banco vetorial atual

Antes de qualquer alteração, realizar backup do banco do Chroma.

Local típico:

```
/opt/doc-ai/chroma
```

ou

```
openwebui/data/vector_db
```

Backup:

```
cp -r chroma chroma_backup_$(date +%Y%m%d)
```

---

# 5. Ajustar o modelo de embeddings no indexador

Localizar o script responsável pela geração de embeddings.

Exemplo típico:

```
/var/www/html/docai/src
```

ou

```
/opt/doc-ai/indexer
```

Localizar código semelhante a:

```
embedding_model = "tinyllama"
```

ou

```
model="llama"
```

Substituir por:

```
model = "nomic-embed-text"
```

Endpoint usado:

```
http://localhost:11434/api/embeddings
```

Exemplo Python:

```
requests.post(
    "http://localhost:11434/api/embeddings",
    json={
        "model": "nomic-embed-text",
        "prompt": texto
    }
)
```

---

# 6. Melhorar o chunking de documentos

Aproveitar a reindexação para melhorar o tamanho dos chunks.

Configuração recomendada:

```
chunk_size = 500 tokens
chunk_overlap = 80 tokens
```

Isso evita problemas como:

```
"112"
"1N4148"
"10"
```

que prejudicam a busca semântica.

---

# 7. Limpar o banco vetorial

Remover o banco atual para evitar mistura de embeddings.

Exemplo:

```
rm -rf /opt/doc-ai/chroma
```

ou

```
rm -rf openwebui/data/vector_db
```

Confirmar que o diretório foi removido.

---

# 8. Reiniciar o processo de indexação

Executar novamente o indexador.

Exemplo:

```
python index_pdfs.py
```

Fluxo esperado:

```
PDF
 ↓
extração texto
 ↓
chunk 500 tokens
 ↓
embedding nomic-embed-text
 ↓
ChromaDB
```

---

# 9. Testar a busca vetorial

Após indexação inicial, testar:

```
curl "http://127.0.0.1:5005/search?q=dht11"
```

Resultados esperados:

```
manual_dht11.pdf
Arduino sensors
temperature humidity sensor
```

Resultados irrelevantes devem diminuir significativamente.

---

# 10. Benefícios da migração

Após a migração:

Melhorias esperadas:

* maior precisão semântica
* melhor recuperação de contexto
* melhor desempenho em RAG
* melhor integração com LLM

---

# 11. Impacto na arquitetura Sentinela

Essa melhoria afeta diretamente o desempenho do:

```
Sentinela AI Gateway
```

Fluxo final:

```
OpenWebUI
     ↓
AI Gateway
     ↓
DocAI (ChromaDB + nomic embeddings)
     ↓
Ollama
```

Isso permite respostas mais precisas sobre:

* sensores
* automação
* documentação técnica
* manuais

---

# 12. Próximos passos após migração

Após a reindexação completa, recomenda-se implementar:

1. metadados de documentos
2. classificação automática de PDFs
3. filtros por categoria
4. melhoria da API `/search`

Essas melhorias permitirão transformar o DocAI em uma **biblioteca técnica cognitiva do Sentinela**.

---

# Observação

Este procedimento **não altera a interface web do DocAI**.

A migração afeta apenas:

```
modelo de embeddings
chunking
banco vetorial
```

A interface e a API permanecem compatíveis.

---

Se quiser, depois que a indexação terminar, posso também te mostrar **uma melhoria muito poderosa no DocAI que quase ninguém implementa**, mas que melhora o RAG em **10×**:
👉 **separar o vector database por domínio (Arduino / eletrônica / redes / sensores)**.
