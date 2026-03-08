# Doc-AI – Interface Web de Busca Semântica

## Visão Geral

A interface web do **Doc-AI** fornece um mecanismo de **busca semântica em documentos PDF**, semelhante ao funcionamento de um mecanismo de busca moderno.
O usuário pode digitar uma pergunta ou palavra-chave em um campo de pesquisa, e o sistema retorna os trechos mais relevantes encontrados na base de documentos indexada.

A experiência visual é inspirada em interfaces minimalistas de buscadores modernos, priorizando:

* simplicidade
* velocidade
* clareza visual
* foco no campo de busca

O sistema consulta diretamente o **banco vetorial ChromaDB**, gerado pelo indexador de PDFs.

---

## Objetivo da Interface

A interface gráfica tem como finalidade permitir que qualquer usuário:

* pesquise informações dentro de milhares de documentos
* encontre rapidamente trechos relevantes
* visualize de qual arquivo e página o conteúdo foi extraído
* acessar rapidamente o PDF original

---

## Arquitetura do Sistema

A interface web utiliza uma arquitetura simples e eficiente.

```
Usuário
   │
   ▼
Interface Web (HTML + CSS + JavaScript)
   │
   ▼
Backend de busca (Python ou PHP)
   │
   ▼
Banco Vetorial (ChromaDB)
   │
   ▼
Embeddings gerados pelo indexador
```

Componentes principais:

| Componente     | Função                               |
| -------------- | ------------------------------------ |
| Interface HTML | Página de pesquisa                   |
| CSS            | Estilo visual                        |
| JavaScript     | Comunicação assíncrona com o backend |
| Backend API    | Executa consultas vetoriais          |
| ChromaDB       | Armazena embeddings                  |
| Indexador      | Processa PDFs e cria vetores         |

---

## Layout da Interface

A interface foi projetada para ser **limpa e intuitiva**, semelhante ao estilo de buscadores modernos.

Elementos principais da página:

```
+--------------------------------------------------+
|                                                  |
|                  DOC-AI                          |
|                                                  |
|         [ Campo de busca semântica ]             |
|                                                  |
|                ( Botão Buscar )                  |
|                                                  |
+--------------------------------------------------+
```

Após uma busca:

```
+--------------------------------------------------+
| DOC-AI                                           |
|                                                  |
| [ Pergunta digitada ] [Buscar]                   |
|                                                  |
| Resultado 1                                      |
| Arquivo: manual_arduino.pdf                      |
| Página: 34                                       |
| Trecho encontrado:                               |
| "...o Arduino utiliza microcontrolador AVR..."   |
|                                                  |
| Resultado 2                                      |
| Arquivo: redes.pdf                               |
| Página: 78                                       |
| "...protocolos TCP/IP são utilizados..."         |
|                                                  |
+--------------------------------------------------+
```

---

## Página Inicial

A página inicial contém:

* logotipo ou título do sistema
* campo de pesquisa centralizado
* botão de execução da busca

Características visuais:

* fundo claro
* layout centralizado
* tipografia simples
* responsivo para dispositivos móveis

---

## Campo de Busca

O campo de busca permite inserir:

* perguntas completas
* palavras-chave
* frases técnicas

Exemplos de consultas:

```
como funciona PWM no Arduino
```

```
controle de motores trifásicos
```

```
o que é protocolo TCP/IP
```

A consulta é enviada ao backend que gera o embedding da pergunta e executa a busca vetorial.

---

## Funcionamento da Busca

Processo interno ao realizar uma pesquisa:

1. usuário digita a consulta
2. o texto é enviado ao backend
3. o backend gera um embedding da pergunta
4. o banco vetorial retorna os vetores mais próximos
5. os trechos correspondentes são exibidos na interface

Fluxo simplificado:

```
Pergunta do usuário
       │
       ▼
Embedding da pergunta
       │
       ▼
Busca vetorial
       │
       ▼
Trechos mais similares
       │
       ▼
Resultados exibidos
```

---

## Resultados da Pesquisa

Cada resultado exibido contém:

| Campo   | Descrição                  |
| ------- | -------------------------- |
| Trecho  | Texto relevante encontrado |
| Arquivo | Nome do PDF                |
| Página  | Página de origem           |
| Caminho | Localização do documento   |

Exemplo visual:

```
Arquivo: Arduino_Basico.pdf
Página: 52

Trecho encontrado:
"O PWM (Pulse Width Modulation) permite controlar
a potência entregue a um dispositivo..."
```

---

## Ordenação dos Resultados

Os resultados são exibidos por **similaridade semântica**, do mais relevante para o menos relevante.

Critério utilizado:

```
distância vetorial entre embeddings
```

Quanto menor a distância, maior a relevância.

---

## Recursos da Interface

Funcionalidades atuais:

* busca semântica em linguagem natural
* resposta em tempo real
* listagem de trechos relevantes
* exibição da página de origem
* suporte a milhares de documentos

---

## Tecnologias Utilizadas

Frontend:

* HTML5
* CSS3
* JavaScript

Backend:

* Python

Bibliotecas principais:

* SentenceTransformers
* ChromaDB
* LangChain

OCR:

* Tesseract OCR

Processamento de PDF:

* pypdf
* pdf2image

---

## Segurança

Medidas básicas implementadas:

* validação de entrada do usuário
* limitação do tamanho da consulta
* prevenção de injeção de código

---

## Performance

O tempo médio de resposta depende do tamanho da base vetorial.

Estimativas típicas:

| Base de documentos | Tempo de resposta |
| ------------------ | ----------------- |
| 100 PDFs           | < 1 segundo       |
| 1000 PDFs          | 1 a 2 segundos    |
| 5000 PDFs          | 2 a 4 segundos    |

---

## Escalabilidade

O sistema pode ser expandido para suportar:

* dezenas de milhares de documentos
* múltiplos usuários simultâneos
* clusters de banco vetorial

---

## Possíveis Melhorias Futuras

Recursos planejados:

* visualização direta da página do PDF
* destaque do trecho encontrado
* histórico de pesquisas
* sugestões automáticas
* interface estilo chatbot
* integração com LLM local
* ranking de relevância aprimorado

---

## Exemplo de Uso

Um usuário deseja descobrir informações sobre **PWM em Arduino**.

Ele digita:

```
como funciona PWM no Arduino
```

O sistema retorna trechos relevantes encontrados em vários documentos técnicos, mostrando onde cada explicação aparece.

---

## Público-Alvo

A interface é útil para:

* pesquisadores
* estudantes
* engenheiros
* analistas de documentação
* suporte técnico
* equipes de desenvolvimento

---
