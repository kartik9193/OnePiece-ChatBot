from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain import hub
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore
from langchain.chains.history_aware_retriever import create_history_aware_retriever

load_dotenv()

def run_llm(query: str, chat_history):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", verbose=True)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    docsearch = PineconeVectorStore(embedding=embeddings, index_name=os.environ['INDEX_NAME'])

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
    history_aware_retriever = create_history_aware_retriever(
        llm=llm, retriever=docsearch.as_retriever(), prompt=rephrase_prompt
    )

    qa_retrieval_chain = create_retrieval_chain(retriever=history_aware_retriever, combine_docs_chain=stuff_documents_chain)

    result = qa_retrieval_chain.invoke(input={"input":query, "chat_history":chat_history})

    return result['answer']