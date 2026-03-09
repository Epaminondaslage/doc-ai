# ##################################################################
# DocAI Indexador PRO v3
# corrigido para performance
# ##################################################################


# ##################################################################
# Este codigo deve ser instalado no serv 10.0.0.37/opt/doc-ai/scrips 
# Desenvolvido em 08-03-2026
# ##################################################################



import os
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
ERROR_FILE = "/opt/doc-ai/index_errors.txt"


print("Carregando modelo embeddings...")

model = SentenceTransformer("all-MiniLM-L6-v2")


print("Abrindo banco vetorial...")

client = chromadb.PersistentClient(path=DB_DIR)

collection = client.get_or_create_collection(name="biblioteca")


splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=120
)


indexed_files = set()

if os.path.exists(CHECKPOINT_FILE):

    with open(CHECKPOINT_FILE,"r",encoding="utf-8") as f:

        indexed_files = set(line.strip() for line in f)


print("PDFs já indexados:",len(indexed_files))


pdf_list = []

for root,dirs,files in os.walk(PDF_DIR):

    for file in files:

        if file.lower().endswith(".pdf"):

            path = os.path.join(root,file)

            if path not in indexed_files:

                pdf_list.append(path)


print("PDFs restantes:",len(pdf_list))


error_files = []

ocr_pages = 0
total_chunks = 0


for path in tqdm(pdf_list):

    file = os.path.basename(path)

    try:

        reader = PdfReader(path)

        if reader.is_encrypted:

            try:
                reader.decrypt("")
            except:
                print("PDF criptografado:",path)
                continue


        for page_number,page in enumerate(reader.pages):

            try:

                text = page.extract_text()

            except:

                continue


            if not text or len(text.strip()) < 80:

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


            ids = []
            metadatas = []


            for i,chunk in enumerate(chunks):

                hash_id = hashlib.md5(
                    f"{path}_{page_number}_{i}".encode()
                ).hexdigest()


                ids.append(hash_id)

                metadatas.append({

                    "arquivo":file,
                    "pagina":page_number+1,
                    "caminho":path

                })


            collection.upsert(

                documents=chunks,
                embeddings=embeddings.tolist(),
                metadatas=metadatas,
                ids=ids

            )


            total_chunks += len(chunks)


        with open(CHECKPOINT_FILE,"a",encoding="utf-8") as f:

            f.write(path+"\n")


    except Exception as e:

        print("Erro:",path,e)

        error_files.append(path)



if error_files:

    with open(ERROR_FILE,"w",encoding="utf-8") as f:

        for e in error_files:

            f.write(e+"\n")


print("\n========================")
print("Indexação concluída")
print("========================")

print("Chunks criados:",total_chunks)
print("Paginas OCR:",ocr_pages)
print("PDFs com erro:",len(error_files))