//     # ##################################################################
//     # Este codigo deve ser instalado no serv 10.0.0.37
//     #   /var/www/html/docai/app.js
//     # Desenvolvido em 08-03-2026
//     # ##################################################################


async function search(){

let q = document.getElementById("query").value;

if(!q) return;

let resultsDiv = document.getElementById("results");

resultsDiv.innerHTML = "Pesquisando...";

let res = await fetch("src/search.php?q=" + encodeURIComponent(q));

let data = await res.json();

let html = "";

html += "<h2>Resposta da IA</h2>";

html += "<div class='answer'>";

html += data.answer;

html += "</div>";

html += "<h2>Documentos encontrados</h2>";

data.results.forEach(r=>{

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

resultsDiv.innerHTML = html;

}