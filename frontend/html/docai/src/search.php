<?php
/* #########################################################
   DocAI - Motor de busca de documentos 10.0.0.37
   Local: /var/www/html/docai/src/search.php
   ######################################################### */

header("Content-Type: application/json");

$q = $_GET["q"] ?? "";

if(!$q){

    echo json_encode([
        "error" => "query vazia"
    ]);

    exit;
}

$url = "http://127.0.0.1:5005/search?q=" . urlencode($q);

$response = file_get_contents($url);

echo $response;