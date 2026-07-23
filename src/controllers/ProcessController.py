from .BaseController import BaseController
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

class ProcessController(BaseController):

    def __init__(self, project_id: str = None):
        super().__init__()
        self.project_id = project_id

    def get_file_content(self, file_id: str):
        file_path = os.path.join(
            self.files_dir,
            self.project_id,
            file_id
        )

        if not os.path.exists(file_path):
            return None

        return self.load_pdf(file_path)

    def load_pdf(self, path):
        pdf_loader = PyPDFLoader(path)

        return pdf_loader.load() 

    def process_file_content(self, file_content: list, file_id: str,
                              chunk_size: int, overlap_size: int):
        return self.split_text_into_chunks(
            document=file_content,
            chunk_size=chunk_size,
            chunk_overlap=overlap_size
        )

    def split_text_into_chunks(self, document: list, chunk_size: int, chunk_overlap: int):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        doc_content_list = [doc.page_content for doc in document]
        doc_metadata_list = [doc.metadata for doc in document]

        chunks = text_splitter.create_documents(doc_content_list, metadatas=doc_metadata_list) 

        print(f"Number of chunks: {len(chunks)}")
        return chunks