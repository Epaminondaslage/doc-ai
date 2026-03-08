# ##################################################################
# DocAI Indexador PRO
# Servidor: 10.0.0.37
# Biblioteca: 1063 PDFs / ~22GB
# ##################################################################

# ##################################################################
# Este codigo deve ser instalado no serv 10.0.0.37/opt/doc-ai/scrips 
# Desenvolvido em 08-03-2026
# ##################################################################


import os
import hashlib
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

import chromadb

import pytesseract
from pdf2image import convert_from_path


# ================================
# CONFIG
# ================================

PDF_DIR = "/opt/doc-ai/pdfs"
DB_DIR = "/opt/doc-ai/vector_db"

CHECKPOINT_FILE = "/opt/doc-ai/index_checkpoint.txt"
ERROR_FILE = "/opt/doc-ai/index_errors.txt"

WORKERS = min(8, cpu_count())

CHUNK_SIZE = 600
CHUNK_OVERLAP = 120


# ================================
# MODELO EMBEDDINGS
# ================================

print("Carregando modelo embeddings...")

model = SentenceTransformer("all-MiniLM-L6-v2")


# ================================
# CHROMADB
# ================================

client = chromadb.PersistentClient(path=DB_DIR)

collection = client.get_or_create_collection(
    name="biblioteca"
)


# ================================
# SPLITTER
# ================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)


# ================================
# CHECKPOINT
# ================================

indexed_files = set()

if os.path.exists(CHECKPOINT_FILE):

    with open(CHECKPOINT_FILE,"r",encoding="utf-8") as f:

        indexed_files = set(line.strip() for line in f)

print("PDFs já indexados:",len(indexed_files))


# ================================
# LISTAR PDFs
# ================================

pdf_list = []

for root,dirs,files in os.walk(PDF_DIR):

    for file in files:

        if file.lower().endswith(".pdf"):

            path = os.path.join(root,file)

            if path not in indexed_files:

                pdf_list.append(path)


print("PDFs restantes:",len(pdf_list))


# ================================
# PROCESSAMENTO DE PDF
# ================================

def process_pdf(path):

    local_docs = []
    local_meta = []
    local_ids = []

    ocr_pages = 0

    file = os.path.basename(path)

    try:

        reader = PdfReader(path)

        if reader.is_encrypted:

            try:
                reader.decrypt("")
            except:
                return None


        for page_number,page in enumerate(reader.pages):

            try:
                text = page.extract_text()
            except:
                continue


            if not text or len(text.strip()) < 200:

                try:

                    images = convert_from_path(
                        path,
                        first_page=page_number+1,
                        last_page=page_number+1
                    )

                    text = pytesseract.image_to_string(
                        images[0],
                        lang="eng+por"
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


            for i,chunk in enumerate(chunks):

                hash_id = hashlib.md5(
                    f"{path}_{page_number}_{i}".encode()
                ).hexdigest()


                local_docs.append(chunk)

                local_meta.append({

                    "arquivo":file,
                    "pagina":page_number+1,
                    "caminho":path

                })

                local_ids.append(hash_id)


        return (local_docs,local_meta,local_ids,path,ocr_pages)


    except Exception as e:

        print("Erro:",path,e)

        return None


# ================================
# PROCESSAMENTO PARALELO
# ================================

print("Workers:",WORKERS)

pool = Pool(WORKERS)

results = []


for result in tqdm(pool.imap_unordered(process_pdf,pdf_list),total=len(pdf_list)):

    if not result:
        continue


    docs,meta,ids,path,ocr_pages = result


    if docs:

        embeddings = model.encode(
            docs,
            batch_size=32,
            show_progress_bar=False
        )


        collection.upsert(

            documents=docs,
            embeddings=embeddings.tolist(),
            metadatas=meta,
            ids=ids

        )


    with open(CHECKPOINT_FILE,"a",encoding="utf-8") as f:

        f.write(path+"\n")


pool.close()
pool.join()


print("\n===============================")
print("Indexação concluída")
print("===============================")