# ##################################################################
# DocAI Indexador v5.1
# UI melhorada + progresso real
# ##################################################################
# ##################################################################
# Este codigo deve ser instalado no serv 10.0.0.37/opt/doc-ai/scrips 
# Desenvolvido em 09-03-2026
# ##################################################################

import os
import time
import hashlib
from tqdm import tqdm
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
import pytesseract
from pdf2image import convert_from_path


PDF_DIR = "/opt/doc-ai/pdfs"
DB_DIR = "/opt/doc-ai/vector_db"
CHECKPOINT_FILE = "/opt/doc-ai/index_checkpoint.txt"

print("\nDocAI Indexador v5.1\n")


print("Carregando modelo embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Abrindo banco vetorial...")
client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection(name="biblioteca")


splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=120
)


# carregar checkpoint

indexed = set()

if os.path.exists(CHECKPOINT_FILE):

    with open(CHECKPOINT_FILE) as f:
        indexed = set(line.strip() for line in f)


# listar PDFs

pdfs = []

for root, dirs, files in os.walk(PDF_DIR):

    for file in files:

        if file.lower().endswith(".pdf"):

            path = os.path.join(root, file)

            if path not in indexed:

                pdfs.append(path)


total = len(pdfs)

print("PDFs restantes:", total)
print()


start = time.time()

total_chunks = 0
ocr_pages = 0


bar = tqdm(total=total, ncols=80)


for i, path in enumerate(pdfs):

    file = os.path.basename(path)

    bar.set_description(f"PDF: {file[:40]}")


    try:

        reader = PdfReader(path)


        for page_number, page in enumerate(reader.pages):

            try:
                text = page.extract_text()
            except:
                text = None


            if not text or len(text.strip()) < 80:

                try:

                    images = convert_from_path(
                        path,
                        first_page=page_number + 1,
                        last_page=page_number + 1,
                        dpi=200
                    )

                    text = pytesseract.image_to_string(
                        images[0],
                        lang="por+eng"
                    )

                    if text:
                        ocr_pages += 1

                except:
                    continue


            if not text:
                continue


            chunks = splitter.split_text(text)


            embeddings = model.encode(
                chunks,
                batch_size=32,
                show_progress_bar=False
            )


            ids = []
            metas = []


            for c, chunk in enumerate(chunks):

                hid = hashlib.md5(
                    f"{path}_{page_number}_{c}".encode()
                ).hexdigest()

                ids.append(hid)

                metas.append({
                    "arquivo": file,
                    "pagina": page_number + 1,
                    "caminho": path
                })


            collection.upsert(
                documents=chunks,
                embeddings=embeddings.tolist(),
                metadatas=metas,
                ids=ids
            )


            total_chunks += len(chunks)


        with open(CHECKPOINT_FILE, "a") as f:
            f.write(path + "\n")


    except Exception as e:

        print("Erro:", path)


    elapsed = time.time() - start
    speed = (i + 1) / elapsed if elapsed else 0

    remaining = (total - (i + 1)) / speed if speed else 0

    bar.set_postfix(
        chunks=total_chunks,
        ocr=ocr_pages,
        eta=f"{remaining/60:.1f}m"
    )

    bar.update(1)


bar.close()

client.persist()


print("\n==============================")
print("Indexação concluída")
print("==============================")

print("Chunks gerados:", total_chunks)
print("Paginas OCR:", ocr_pages)