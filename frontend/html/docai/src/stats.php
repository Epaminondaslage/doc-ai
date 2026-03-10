<?php

header('Content-Type: application/json');

$pdfDir = "/opt/doc-ai/pdfs";

$pdfs = 0;
$pages = 0;

/* percorrer PDFs recursivamente */

$iterator = new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator($pdfDir)
);

foreach ($iterator as $file) {

    if ($file->isFile() && strtolower($file->getExtension()) === "pdf") {

        $pdfs++;

        $path = escapeshellarg($file->getPathname());

        $info = shell_exec("pdfinfo $path 2>/dev/null | grep Pages");

        if(preg_match('/Pages:\s+(\d+)/', $info, $m)) {
            $pages += intval($m[1]);
        }
    }
}

/* chunks atuais */
$chunks = 57740;

echo json_encode([
    "pdfs" => $pdfs,
    "pages" => $pages,
    "chunks" => $chunks
]);