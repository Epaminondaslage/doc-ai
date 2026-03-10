/* ##########################################################
   DocAI - Interface de Busca
   Desenvolvido para consulta de documentos técnicos
   roda em 10.0.0.37/var/www/html/docai/js
   ########################################################## */

const input = document.getElementById("query");
const resultsDiv = document.getElementById("results");
const autocompleteDiv = document.getElementById("autocomplete");

/* =========================
   CONTROLE DE PAGINAÇÃO
   ========================= */

let allResults = [];
let currentPage = 1;
let resultsPerPage = 5;


/* =========================
   Buscar ao pressionar ENTER
   ========================= */

input.addEventListener("keypress", function(e){

    if(e.key === "Enter"){
        search();
    }

});


/* =========================
   Função principal de busca
   ========================= */

function search(){

    const q = input.value.trim();

    if(!q){
        return;
    }

    resultsDiv.innerHTML = loadingHTML();
    autocompleteDiv.innerHTML = "";

    fetch("src/search.php?q=" + encodeURIComponent(q))
        .then(response => response.json())
        .then(data => renderResults(data, q))
        .catch(err => {

            resultsDiv.innerHTML =
                "<div class='result'>Erro ao consultar servidor.</div>";

            console.error(err);

        });

}


/* =========================
   Loading
   ========================= */

function loadingHTML(){

    return `
        <div class="loading">
            <div class="spinner"></div>
            Buscando nos documentos...
        </div>
    `;

}


/* =========================
   Renderização de resultados
   ========================= */

function renderResults(data, query){

    resultsDiv.innerHTML = "";

    /* ---------- resposta da IA ---------- */

    if(data.answer){

        const answerBox = document.createElement("div");
        answerBox.className = "answer";
        answerBox.innerHTML = highlight(data.answer, query);

        resultsDiv.appendChild(answerBox);

    }

    /* ---------- documentos encontrados ---------- */

    if(!data.results || data.results.length === 0){

        resultsDiv.innerHTML +=
            "<div class='result'>Nenhum documento encontrado.</div>";

        return;

    }

    /* salvar resultados para paginação */

    allResults = data.results;

    showPage(1, query);

}


/* =========================
   Mostrar página específica
   ========================= */

function showPage(page, query){

    resultsDiv.innerHTML = "";

    currentPage = page;

    const start = (page-1) * resultsPerPage;
    const end = start + resultsPerPage;

    const pageResults = allResults.slice(start, end);

    pageResults.forEach(item => {

        const div = document.createElement("div");
        div.className = "result";

        /* link para abrir PDF */

        const pdfLink =
            "/docai/pdfs" +
            item.caminho.replace("/opt/doc-ai/pdfs","") +
            "#page=" +
            item.pagina +
            "&search=" +
            encodeURIComponent(query);

         div.innerHTML = `

            <div class="result-title">

            <span class="pdf-icon">📄</span>

            <a href="${pdfLink}" target="_blank" class="doc-link">
            ${item.arquivo}
            </a>

            <span class="page">— página ${item.pagina}</span>

            </div>

            <div class="trecho">
            ${highlight(item.trecho, query)}
            </div>

            `;

        resultsDiv.appendChild(div);

    });

    renderPagination(query);

}


/* =========================
   Renderizar botões de página
   ========================= */

function renderPagination(query){

    const totalPages = Math.ceil(allResults.length / resultsPerPage);

    if(totalPages <= 1){
        return;
    }

    const nav = document.createElement("div");
    nav.className = "pagination";

    for(let i=1;i<=totalPages;i++){

        const btn = document.createElement("button");

        btn.innerText = i;

        if(i === currentPage){
            btn.style.background="#4285f4";
            btn.style.color="#fff";
        }

        btn.onclick = () => showPage(i, query);

        nav.appendChild(btn);

    }

    resultsDiv.appendChild(nav);

}


/* =========================
   Destaque da palavra buscada
   ========================= */

function highlight(text, query){

    if(!text){
        return "";
    }

    const words = query.split(" ");

    words.forEach(word => {

        const regex = new RegExp("(" + word + ")", "gi");

        text = text.replace(
            regex,
            "<mark>$1</mark>"
        );

    });

    return text;

}


/* =========================
   Autocomplete (básico)
   ========================= */

input.addEventListener("input", function(){

    const q = input.value;

    if(q.length < 3){
        autocompleteDiv.innerHTML = "";
        return;
    }

    fetch("src/search.php?q=" + encodeURIComponent(q))
        .then(r => r.json())
        .then(data => {

            autocompleteDiv.innerHTML = "";

            if(!data.results){
                return;
            }

            data.results.slice(0,5).forEach(item => {

                const div = document.createElement("div");
                div.className = "auto-item";

                div.innerText =
                    item.arquivo +
                    " (página " +
                    item.pagina +
                    ")";

                div.onclick = () => {

                    input.value = item.arquivo;
                    autocompleteDiv.innerHTML = "";
                    search();

                };

                autocompleteDiv.appendChild(div);

            });

        });

});


/* =========================
   Carregar estatísticas
   ========================= */

function loadStats(){

fetch("src/stats.php")
.then(r => r.json())
.then(data => {

const footer = document.getElementById("stats");
if(!footer) return;

footer.innerHTML =
`
${data.pdfs} PDFs • 
${data.pages.toLocaleString('pt-BR')} páginas • 
${Math.round(data.chunks/1000)}k trechos indexados
`;

});

}

document.addEventListener("DOMContentLoaded", loadStats);