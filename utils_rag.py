# utils_rag.py

import os
import json
import openai
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Charger la clé .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# Si vous voulez vérifier la clé :
# if not openai.api_key:
#     raise ValueError("Clé OPENAI_API_KEY non trouvée.")

def charger_donnees_json(dossier_json: str):
    documents = []
    for nom_fichier in os.listdir(dossier_json):
        if nom_fichier.endswith(".json"):
            chemin_fichier = os.path.join(dossier_json, nom_fichier)
            try:
                with open(chemin_fichier, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for question in data.get("questions", []):
                        contenu = f"Question: {question['question']}\nRéponse: {question['reponse']}"
                        documents.append(
                            Document(
                                page_content=contenu,
                                metadata={"source": nom_fichier}
                            )
                        )
            except json.JSONDecodeError as e:
                print(f"❌ Erreur JSON dans {nom_fichier} : {e}")
    return documents

def preparer_et_indexer_documents(documents, chemin_chroma="embeddings", collection_name="orientation_chatbot"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    splitted_docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)

    vecteur_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=chemin_chroma
    )

    vecteur_store.add_documents(splitted_docs)
    vecteur_store.persist()
    return vecteur_store

def construire_chatbot(vectorstore, temperature=0.0, model_name="gpt-3.5-turbo", k=2, verbose=False):
    llm = ChatOpenAI(
        model_name=model_name,
        openai_api_key=openai.api_key,
        temperature=temperature
    )

    # Mémoire conversationnelle
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k}),
        memory=memory,
        verbose=verbose
    )
    return qa_chain
