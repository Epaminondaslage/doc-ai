Segue um **README completo do Front-End do DocAI**, focado apenas na **interface web**, inicialização e acesso.
Ele foi escrito para ficar dentro do projeto:

```
/var/www/html/docai/README.md
```

---

# DocAI — Interface Web de Pesquisa

## Visão Geral

O **DocAI** é uma interface web para pesquisa em uma biblioteca técnica baseada em **busca vetorial em documentos PDF**.

A interface permite que o usuário faça perguntas em linguagem natural e receba:

* trechos relevantes de documentos
* referência ao arquivo original
* link direto para a página do PDF

A interface foi projetada com um layout simples e eficiente, inspirado em motores de busca como Google.

---

# Arquitetura do Sistema

O front-end não executa a busca diretamente.
Ele apenas envia a pergunta ao backend.

Fluxo completo:

```
Usuário
   │
   ▼
index.html
   │
   ▼
app.js (AJAX)
   │
   ▼
search.php
   │
HTTP local
   │
   ▼
DocAI API (Python)
   │
   ▼
ChromaDB
   │
   ▼
Documentos PDF
```

---

# Estrutura do Front-End

Localização no servidor:

```
/var/www/html/docai
```

Estrutura do projeto:

```
docai
│
├── index.html
│
├── css
│   └── style.css
│
├── js
│   └── app.js
│
└── src
    └── search.php
```

Descrição dos arquivos:

| Arquivo    | Função                                        |
| ---------- | --------------------------------------------- |
| index.html | Página principal da interface                 |
| style.css  | Estilos visuais da aplicação                  |
| app.js     | Lógica de busca via AJAX                      |
| search.php | Endpoint que conecta a interface à API Python |

---

# Página Principal

Arquivo:

```
index.html
```

Responsável por:

* renderizar a interface
* receber a pergunta do usuário
* exibir resultados
* carregar CSS e JavaScript

Componentes da interface:

* campo central de pesquisa
* botão de busca
* área de resultados
* área de sugestões (autocomplete)

---

# Estilo Visual

Arquivo:

```
css/style.css
```

Principais características:

* layout minimalista
* campo de busca centralizado
* design responsivo
* cartões de resultados
* animação de carregamento (spinner)

Compatível com:

* desktop
* tablets
* dispositivos móveis

---

# Lógica da Aplicação

Arquivo:

```
js/app.js
```

Responsável por:

* capturar a pergunta
* enviar requisição AJAX
* exibir loading
* renderizar resultados
* destacar termos encontrados

A busca é enviada para:

```
src/search.php
```

---

# Endpoint PHP

Arquivo:

```
src/search.php
```

Função:

* receber a pergunta
* encaminhar para a API Python
* retornar JSON para o navegador

Exemplo de consulta:

```
/src/search.php?q=transistor
```

---

# Inicialização da Interface

A interface não precisa de processo de inicialização.

Ela é servida diretamente pelo **Apache2**.

Certifique-se de que o Apache esteja rodando.

No servidor:

```
sudo systemctl status apache2
```

Se necessário:

```
sudo systemctl start apache2
```

---

# Como Acessar

No navegador, acesse:

```
http://IP_DO_SERVIDOR/docai
```

ou

```
http://localhost/docai
```

A página exibirá o campo de busca.

---

# Funcionamento da Busca

Quando o usuário digita uma pergunta:

1. O JavaScript captura o texto
2. Uma requisição AJAX é enviada para

```
src/search.php
```

3. O PHP consulta a API Python

```
http://127.0.0.1:5005/search
```

4. A API consulta o banco vetorial

```
/opt/doc-ai/vector_db
```

5. Os resultados retornam para a interface.

---

# Exemplo de Consulta

Pergunta do usuário:

```
transistor bipolar
```

Resposta exibida:

```
Arquivo: Eletronica_Basica.pdf
Página: 45

Trecho:
O transistor bipolar é um dispositivo semicondutor utilizado para amplificação...
```

Link gerado:

```
Eletronica_Basica.pdf#page=45
```

O navegador abre diretamente na página correspondente.

---

# Requisitos

Para funcionamento completo:

* Apache2
* PHP 8+
* API DocAI em execução
* banco vetorial ChromaDB indexado

---

# Segurança

A interface web **não acessa diretamente o banco vetorial**.

A comunicação ocorre apenas via:

```
search.php
```

A API Python roda em:

```
127.0.0.1:5005
```

Isso evita exposição externa do motor de IA.

---

# Manutenção

Caso a interface precise ser atualizada:

1. editar arquivos em

```
/var/www/html/docai
```

2. atualizar o navegador

Não é necessário reiniciar o Apache.

---

# Melhorias Futuras

Possíveis evoluções da interface:

* visualização de PDF ao lado dos resultados
* destaque automático do trecho dentro do PDF
* histórico de buscas
* paginação de resultados
* modo chat com documentos
* ranking de relevância
* cache de consultas

---

# Licença

Projeto interno DocAI.

Uso educacional e técnico.

---

Se quiser, também posso gerar um **segundo README para o backend (API Python + ChromaDB)**, explicando:

* indexação
* estrutura `/opt/doc-ai`
* execução do serviço
* manutenção do banco vetorial.
