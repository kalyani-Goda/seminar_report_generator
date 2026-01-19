from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

def setup_retriever(folder_path: str):
    loader = PyPDFDirectoryLoader(folder_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200
    )

    splits = splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(
        splits,
        embedding=OllamaEmbeddings(model="nomic-embed-text"),
        collection_name="seminar_papers"
    )

    return vectorstore.as_retriever(search_kwargs={"k": 3})
