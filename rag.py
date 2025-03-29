import os
import json
import openai
from dotenv import load_dotenv

# IMPORTANT : on utilise ici langchain_openai & langchain_community
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# 1. Configuration de la clé OpenAI
openai.api_key = "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"
os.environ["OPENAI_API_KEY"] = openai.api_key

# 2. Fonction : charger les JSON
def charger_donnees_json(dossier_json):
    documents = []
    for nom_fichier in os.listdir(dossier_json):
        if nom_fichier.endswith(".json"):
            chemin_fichier = os.path.join(dossier_json, nom_fichier)
            try:
                with open(chemin_fichier, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Pour chaque question trouvée
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

# 3. Fonction : indexer les documents
def preparer_et_indexer_documents(documents, chemin_chroma):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs_split = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
    vecteur_store = Chroma(
        collection_name="orientation_chatbot",
        embedding_function=embeddings,
        persist_directory=chemin_chroma
    )
    vecteur_store.add_documents(docs_split)
    vecteur_store.persist()
    return vecteur_store

# 4. Construire la chaîne QA
def construire_chatbot(vectorstore, temperature=0.3):
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        openai_api_key=openai.api_key,
        temperature=temperature
    )
    memoire = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        ),
        memory=memoire,
        verbose=True
    )
    return qa_chain

# 5. Mode terminal
def mode_terminal():
    print("\n🔍 Chargement et indexation des documents...")
    docs = charger_donnees_json("./load_documents")
    vecteurs = preparer_et_indexer_documents(docs, "./embeddings")
    chatbot = construire_chatbot(vecteurs)

    print("\n🤖 Chatbot prêt ! Posez vos questions (ou tapez 'exit'):\n")
    while True:
        question = input("> ")
        if question.lower() in ["exit", "quit"]:
            break
        reponse = chatbot.invoke({"question": question})
        print("\n🧠 Réponse :", reponse["answer"], "\n")

# 6. Point d'entrée
if __name__ == "__main__":
    mode_terminal()
