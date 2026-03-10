#!/bin/bash

PDF_DIR="/opt/doc-ai/pdfs"
CHECKPOINT="/opt/doc-ai/index_checkpoint.txt"
LOG="/opt/doc-ai/index_status.log"

TOTAL_PDFS=$(find "$PDF_DIR" -iname "*.pdf" | wc -l)
INDEXADOS=$(wc -l < "$CHECKPOINT")

RESTANTES=$((TOTAL_PDFS - INDEXADOS))

DATA_ATUAL=$(date +%s)
DATA_HUMANA=$(date "+%Y-%m-%d %H:%M:%S")

echo
echo "========================================"
echo "        Status da Indexação DocAI"
echo "========================================"
echo

echo "Data atual        : $DATA_HUMANA"
echo "PDFs biblioteca   : $TOTAL_PDFS"
echo "PDFs indexados    : $INDEXADOS"
echo "PDFs restantes    : $RESTANTES"

if [ "$TOTAL_PDFS" -gt 0 ]; then
    PERC=$((INDEXADOS * 100 / TOTAL_PDFS))
    echo "Progresso         : $PERC %"
fi

echo

# calcular velocidade usando último log

if [ -f "$LOG" ]; then

    LAST_LINE=$(tail -n 1 "$LOG")

    LAST_TIME=$(echo $LAST_LINE | awk '{print $1}')
    LAST_INDEXED=$(echo $LAST_LINE | awk '{print $2}')

    DELTA_TIME=$((DATA_ATUAL - LAST_TIME))
    DELTA_DOCS=$((INDEXADOS - LAST_INDEXED))

    if [ "$DELTA_TIME" -gt 0 ]; then

        DOCS_HORA=$(echo "$DELTA_DOCS*3600/$DELTA_TIME" | bc)

        echo "Novos PDFs        : $DELTA_DOCS"
        echo "Tempo decorrido   : $((DELTA_TIME/60)) min"
        echo "Velocidade        : $DOCS_HORA PDFs/hora"

    fi

fi

echo

echo "$DATA_ATUAL $INDEXADOS" >> "$LOG"

echo "Histórico salvo em:"
echo "$LOG"

echo
echo "========================================"