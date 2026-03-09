# ##################################################################
# Este codigo deve ser instalado no serv 10.0.0.37/opt/doc-ai/scrips 
# Desenvolvido em 08-03-2026
# ##################################################################

import os
import hashlib
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings

import pytesseract
from pdf2image import convert_from_path


# Diretórios
PDF_DIR = "/opt/doc-ai/pdfs"
DB_DIR = "/opt/doc-ai/vector_db"


print("Carregando modelo de embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")


print("Iniciando banco vetorial...")
client = chromadb.Client(Settings(persist_directory=DB_DIR))
collection = client.get_or_create_collection(name="biblioteca")


splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)


total_chunks = 0
total_pdfs = 0
ocr_used = 0
pdf_errors = 0


for root, dirs, files in os.walk(PDF_DIR):

    for file in files:

        if not file.lower().endswith(".pdf"):
            continue

        path = os.path.join(root, file)

        print("\nIndexando:", path)

        try:

            reader = PdfReader(path)

            # PDFs criptografados
            if reader.is_encrypted:
                try:
                    reader.decrypt("")
                except:
                    print("PDF criptografado ignorado:", path)
                    pdf_errors += 1
                    continue


            for page_number, page in enumerate(reader.pages):

                try:
                    text = page.extract_text()
                except:
                    print("Erro ao ler página", page_number + 1, "de", path)
                    continue


                # OCR automático se não houver texto
                if not text or len(text.strip()) < 20:

                    try:

                        images = convert_from_path(
                            path,
                            first_page=page_number + 1,
                            last_page=page_number + 1
                        )

                        text = pytesseract.image_to_string(
                            images[0],
                            lang="eng+por"
                        )

                        if text:
                            ocr_used += 1

                    except Exception as e:
                        print("Erro OCR:", e)
                        continue


                if not text:
                    continue


                chunks = splitter.split_text(text)

                embeddings = model.encode(chunks)

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


                collection.add(
                    documents=chunks,
                    embeddings=embeddings.tolist(),
                    metadatas=metadatas,
                    ids=ids
                )


                total_chunks += len(chunks)


            total_pdfs += 1


        except Exception as e:

            print("Erro:", path, e)
            pdf_errors += 1


client.persist()


print("\n===============================")
print("Indexação concluída")
print("===============================")

print("PDFs indexados:", total_pdfs)
print("Trechos criados:", total_chunks)
print("Páginas processadas com OCR:", ocr_used)
print("PDFs com erro:", pdf_errors)
