<!-- # ##################################################################
     # Este codigo deve ser instalado no serv 10.0.0.37
     #   /var/www/html/docai/search.php
     # Desenvolvido em 08-03-2026
     # ################################################################## -->



<?php

header("Content-Type: application/json");

$q = $_GET["q"] ?? "";

if(!$q){

echo json_encode(["error"=>"no query"]);

exit;

}

$cmd = "docai ".escapeshellarg($q);

$output = shell_exec($cmd);

$results = [];

preg_match_all("/Arquivo:\s*(.*)\nPágina:\s*(\d+)/",$output,$matches,PREG_SET_ORDER);

foreach($matches as $m){

$results[] = [

"arquivo"=>$m[1],
"pagina"=>$m[2],
"trecho"=>"Trecho encontrado relacionado à pergunta.",
"caminho"=>"/opt/doc-ai/pdfs/".$m[1]

];

}

echo json_encode([

"answer"=>$output,
"results"=>$results

]);