# ##################################################################
# DocAI Indexador v4
# alta performance para bibliotecas grandes
# ##################################################################

# ##################################################################
# Este codigo deve ser instalado no serv 10.0.0.37/opt/doc-ai/scrips 
# Desenvolvido em 09-03-2026
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

LOG_DIR = "/opt/doc-ai/logs"
ERROR_LOG = os.path.join(LOG_DIR, "errors.log")
OCR_LOG = os.path.join(LOG_DIR, "ocr.log")


os.makedirs(LOG_DIR, exist_ok=True)


print("\nDocAI Indexador v4\n")

print("Carregando modelo de embeddings...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Abrindo banco vetorial...")

client = chromadb.PersistentClient(path=DB_DIR)

collection = client.get_or_create_collection(name="biblioteca")


splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=120
)


# carregar checkpoint

indexed_files = set()

if os.path.exists(CHECKPOINT_FILE):

    with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:

        indexed_files = set(line.strip() for line in f)


print("PDFs já indexados:", len(indexed_files))


# lista PDFs restantes

pdf_list = []

for root, dirs, files in os.walk(PDF_DIR):

    for file in files:

        if file.lower().endswith(".pdf"):

            path = os.path.join(root, file)

            if path not in indexed_files:

                pdf_list.append(path)


print("PDFs restantes:", len(pdf_list))


total_chunks = 0
ocr_pages = 0


for path in tqdm(pdf_list):

    file = os.path.basename(path)

    try:

        reader = PdfReader(path)

        if reader.is_encrypted:

            try:
                reader.decrypt("")
            except:
                with open(ERROR_LOG, "a") as f:
                    f.write(path + " encrypted\n")
                continue


        for page_number, page in enumerate(reader.pages):

            try:
                text = page.extract_text()
            except:
                text = None


            # detectar se precisa OCR

            if not text or len(text.strip()) < 80:

                try:

                    images = convert_from_path(
                        path,
                        first_page=page_number + 1,
                        last_page=page_number + 1
                    )

                    text = pytesseract.image_to_string(
                        images[0],
                        lang="por+eng"
                    )

                    if text:

                        with open(OCR_LOG, "a") as f:
                            f.write(f"{path} page {page_number+1}\n")

                        ocr_pages += 1

                except Exception as e:

                    with open(ERROR_LOG, "a") as f:
                        f.write(path + " OCR error\n")

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


            for i, chunk in enumerate(chunks):

                hash_id = hashlib.md5(
                    f"{path}_{page_number}_{i}".encode()
                ).hexdigest()

                ids.append(hash_id)

                metadatas.append({

                    "arquivo": file,
                    "pagina": page_number + 1,
                    "caminho": path

                })


            collection.upsert(

                documents=chunks,
                embeddings=embeddings.tolist(),
                metadatas=metadatas,
                ids=ids

            )


            total_chunks += len(chunks)


        # salvar checkpoint

        with open(CHECKPOINT_FILE, "a") as f:
            f.write(path + "\n")


    except Exception as e:

        with open(ERROR_LOG, "a") as f:
            f.write(path + " " + str(e) + "\n")


print("\n==============================")
print("Indexação finalizada")
print("==============================")

print("Chunks gerados:", total_chunks)
print("Paginas OCR:", ocr_pages)