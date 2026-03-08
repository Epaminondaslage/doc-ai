/*     # ##################################################################
       # Este codigo deve ser instalado no serv 10.0.0.37
       #   /var/www/html/docai/js/app.js
       # Desenvolvido em 08-03-2026
       # ################################################################## */


// ================================
// ELEMENTOS DA INTERFACE
// ================================

const input = document.getElementById("query");
const autocomplete = document.getElementById("autocomplete");
const resultsDiv = document.getElementById("results");


// ================================
// ENTER PARA PESQUISAR
// ================================

input.addEventListener("keypress", function(e){

    if(e.key === "Enter"){
        search();
    }

});


// ================================
// HISTÓRICO LOCAL DE BUSCAS
// ================================

function saveHistory(q){

    let history = JSON.parse(localStorage.getItem("docai_history") || "[]");

    if(!history.includes(q)){
        history.unshift(q);
    }

    history = history.slice(0,10);

    localStorage.setItem("docai_history", JSON.stringify(history));

}


// ================================
// AUTOCOMPLETE
// ================================

function showAutocomplete(){

    let history = JSON.parse(localStorage.getItem("docai_history") || "[]");

    let q = input.value.toLowerCase();

    autocomplete.innerHTML = "";

    if(!q) return;

    history.forEach(h => {

        if(h.toLowerCase().includes(q)){

            let div = document.createElement("div");

            div.className = "auto-item";

            div.innerText = h;

            div.onclick = function(){

                input.value = h;

                search();

            };

            autocomplete.appendChild(div);

        }

    });

}

input.addEventListener("input", showAutocomplete);


// ================================
// FUNÇÃO PRINCIPAL DE BUSCA
// ================================

async function search(){

    let q = input.value.trim();

    if(!q) return;

    saveHistory(q);

    autocomplete.innerHTML = "";


    // ================================
    // ANIMAÇÃO DE CARREGAMENTO
    // ================================

    resultsDiv.innerHTML = `
    <div class="loading">
        <div class="spinner"></div>
        Consultando biblioteca...
    </div>
    `;


    try{

        let response = await fetch("src/search.php?q=" + encodeURIComponent(q));

        let data = await response.json();


        let html = "";


        // ================================
        // RESPOSTA DA IA
        // ================================

        if(data.answer){

            html += "<h2>Resposta da IA</h2>";

            html += "<div class='answer'>";

            html += data.answer;

            html += "</div>";

        }


        // ================================
        // RESULTADOS ENCONTRADOS
        // ================================

        html += "<h2>Documentos encontrados</h2>";


        if(data.results && data.results.length > 0){

            data.results.forEach(r => {

                html += "<div class='result'>";

                html += "<div class='fonte'>";

                html += r.arquivo + " (página " + r.pagina + ")";

                html += "</div>";

                html += "<div class='trecho'>";

                html += r.trecho;

                html += "</div>";

                html += "<br>";

                html += "<a target='_blank' href='file://" + r.caminho + "'>";

                html += "Abrir PDF";

                html += "</a>";

                html += "</div>";

            });

        }else{

            html += "<p>Nenhum documento encontrado.</p>";

        }


        resultsDiv.innerHTML = html;

    }

    catch(error){

        resultsDiv.innerHTML = `
        <div class="answer">
        Erro ao consultar a biblioteca.
        <br><br>
        ${error}
        </div>
        `;

    }

}