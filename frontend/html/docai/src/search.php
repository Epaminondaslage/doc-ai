<?php
/* #########################################################
   DocAI - Motor de busca de documentos 10.0.0.37
   Local: /var/www/html/docai/src/search.php
   ######################################################### */

header("Content-Type: application/json; charset=UTF-8");

/* =============================
   Configurações
   ============================= */

$PDF_PATH = "/opt/doc-ai/pdfs/";

/* =============================
   Receber pergunta
   ============================= */

$q = trim($_GET["q"] ?? "");

if (!$q) {
    echo json_encode([
        "error" => "Pergunta vazia"
    ]);
    exit;
}

/* =============================
   Executar motor DocAI
   ============================= */

$cmd = "docai " . escapeshellarg($q) . " 2>&1";
$output = shell_exec($cmd);

if (!$output) {

    echo json_encode([
        "error" => "Erro ao executar motor DocAI"
    ]);

    exit;
}

/* =============================
   Extrair referências de documentos
   Esperado no formato:

   Arquivo: manual.pdf
   Página: 23
   Trecho: texto encontrado
   ============================= */

$results = [];

preg_match_all(
    '/Arquivo:\s*(.*)\nPágina:\s*(\d+)(?:\nTrecho:\s*(.*))?/i',
    $output,
    $matches,
    PREG_SET_ORDER
);

foreach ($matches as $m) {

    $arquivo = trim($m[1]);
    $pagina  = trim($m[2]);
    $trecho  = isset($m[3]) ? trim($m[3]) : "";

    $results[] = [
        "arquivo" => $arquivo,
        "pagina" => $pagina,
        "trecho" => $trecho,
        "caminho" => $PDF_PATH . $arquivo
    ];
}

/* =============================
   Limpar texto da resposta IA
   removendo blocos de referência
   ============================= */

$answer = preg_replace(
    '/Arquivo:.*?Página:\s*\d+/s',
    '',
    $output
);

$answer = trim($answer);

/* =============================
   Retorno final
   ============================= */

echo json_encode([
    "query" => $q,
    "answer" => $answer,
    "results" => $results,
    "count" => count($results)
], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);