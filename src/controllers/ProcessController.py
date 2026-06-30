from .BaseController import BaseController
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ProcessController(BaseController):

    def __init__(self):
        super().__init__()



    def load_pdf(self,path):
        pdf_loader = PyPDFLoader(path)

        return pdf_loader.load() 


    def split_text_into_chunks(self,document:list,chunk_size:int,chunk_overlap:int):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap,
                                                      separators=["\n\n", "\n", " ", ""])
        
        doc_content_list=[doc.page_content for doc in document]
        doc_metadata_list=[doc.metadata for doc in document]

        chunks=text_splitter.create_documents(doc_content_list,metadatas=doc_metadata_list) 
        
    

        print(  f"Number of chunks: {len(chunks)}")
        return chunks


    



    


       



    