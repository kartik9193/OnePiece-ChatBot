import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_pinecone import PineconeVectorStore

load_dotenv()

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"), model='text-embedding-3-small')

def ingest_docs(file_path):
    print("Ingestion Started...")
    loader = TextLoader(file_path=file_path)
    raw_documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100
    )

    documents = text_splitter.split_documents(raw_documents)

    print(f"Loaded {len(documents)} documents")

    PineconeVectorStore.from_documents(embedding=embeddings, index_name=os.environ['INDEX_NAME'], documents=documents)

    print("Ingestion complete")

if __name__ == "__main__":
    ingest_docs(os.environ['TXTFILE_PATH'])