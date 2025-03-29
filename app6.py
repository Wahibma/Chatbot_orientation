import streamlit as st
import os
from utils_rag import (
    charger_donnees_json,
    preparer_et_indexer_documents,
    construire_chatbot
)

def main():
    st.set_page_config(page_title="Chatbot d'Orientation", layout="centered")
    st.title("Chatbot d'Orientation Étudiant")

    st.markdown("""
    Bienvenue sur votre Chatbot d'Orientation Étudiant. 
    Posez vos questions ci-dessous, et le chatbot vous répondra 
    en se basant sur les documents chargés.
    """)

    dossier_json = "load_documents"
    chemin_chroma = "embeddings"

    # 1) Charger et indexer (si pas déjà fait)
    if "vecteur_store" not in st.session_state or st.session_state.vecteur_store is None:
        st.write("**Chargement et indexation des documents...**")
        docs = charger_donnees_json(dossier_json)
        st.session_state.docs = docs

        vecteur_store = preparer_et_indexer_documents(docs, chemin_chroma)
        st.session_state.vecteur_store = vecteur_store
        st.success("Données indexées avec succès !")

    # 2) Paramètres internes (non visibles)
    temperature = 0.3
    k = 4
    model_name = "gpt-3.5-turbo"

    # 3) Construire / mettre à jour le chatbot
    st.session_state.chatbot = construire_chatbot(
        st.session_state.vecteur_store,
        temperature=temperature,
        model_name=model_name,
        k=k
    )

    # 4) Historique
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Afficher l'historique
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            # Bulle pour l’utilisateur
            with st.chat_message("user"):
                st.write(f"**Question :** {msg['content']}")
        else:
            # Bulle pour l’assistant
            with st.chat_message("assistant"):
                st.write(f"**Réponse :** {msg['content']}")

    # 5) Zone de saisie
    user_input = st.chat_input("Posez votre question ici...")

    # 6) Gestion de la nouvelle question
    if user_input:
        # (Optionnel) Vérifier si la question est la même que la dernière question
        if len(st.session_state.messages) > 0:
            last_msg = st.session_state.messages[-1]
            if last_msg["role"] == "user" and last_msg["content"] == user_input.strip():
                st.warning("Vous venez de poser la même question. Veuillez en poser une autre.")
                return

        # Ajouter la question à l’historique
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Appel du chatbot
        reponse = st.session_state.chatbot.invoke({"question": user_input})
        bot_answer = reponse["answer"]

        # Ajouter la réponse
        st.session_state.messages.append({"role": "assistant", "content": bot_answer})

        # Afficher immédiatement la réponse
        with st.chat_message("assistant"):
            st.write(f"**Réponse :** {bot_answer}")

if __name__ == "__main__":
    # Initialisations
    if "docs" not in st.session_state:
        st.session_state.docs = None
    if "vecteur_store" not in st.session_state:
        st.session_state.vecteur_store = None
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = None
    if "messages" not in st.session_state:
        st.session_state.messages = []

    main()
