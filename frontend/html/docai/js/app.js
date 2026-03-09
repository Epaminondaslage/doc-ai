/* ##########################################################
   DocAI - Interface de Busca
   Desenvolvido para consulta de documentos técnicos
   roda em 10.0.0.37/var/www/html/docai/js
   ########################################################## */

const input = document.getElementById("query");
const resultsDiv = document.getElementById("results");
const autocompleteDiv = document.getElementById("autocomplete");

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

    data.results.forEach(item => {

        const div = document.createElement("div");
        div.className = "result";

        const pdfLink =
            item.caminho +
            "#page=" +
            item.pagina;

        div.innerHTML = `
            <div class="fonte">
                📄 ${item.arquivo} — página ${item.pagina}
            </div>

            <div class="trecho">
                ${highlight(item.trecho, query)}
            </div>

            <div style="margin-top:10px">
                <a href="${pdfLink}" target="_blank">
                    Abrir PDF na página ${item.pagina}
                </a>
            </div>
        `;

        resultsDiv.appendChild(div);

    });

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