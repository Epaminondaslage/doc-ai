<?php
/* #########################################################
   DocAI - Motor de busca de documentos
   Servidor: 10.0.0.37
   Local: /var/www/html/docai/src/search.php
   ######################################################### */

header("Content-Type: application/json; charset=utf-8");

$q = $_GET["q"] ?? "";

if(!$q){
    echo json_encode([
        "query" => "",
        "results" => []
    ]);
    exit;
}

$url = "http://127.0.0.1:5005/search?q=" . urlencode($q);

/* usar cURL é mais seguro que file_get_contents */

$ch = curl_init();

curl_setopt_array($ch, [
    CURLOPT_URL => $url,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 10
]);

$response = curl_exec($ch);

if(curl_errno($ch)){
    echo json_encode([
        "error" => "API indisponível"
    ]);
    curl_close($ch);
    exit;
}

curl_close($ch);

/* garantir que sempre retornamos JSON */

$data = json_decode($response, true);

if(!$data){
    echo json_encode([
        "error" => "Resposta inválida da API"
    ]);
    exit;
}

echo json_encode($data, JSON_UNESCAPED_UNICODE);