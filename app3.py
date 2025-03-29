import streamlit as st
from utils_rag import (
    charger_donnees_json,
    preparer_et_indexer_documents,
    construire_chatbot
)

def main():
    st.set_page_config(page_title="Chat Multi-Utilisateurs", layout="centered")
    st.title("Chatbot d'Orientation - Multi Utilisateurs")

    # Barre latérale : pseudo
    pseudo = st.sidebar.text_input("Nom d'utilisateur :", value="", placeholder="Entrez votre pseudo")

    # Bouton pour valider son pseudo
    if st.sidebar.button("Valider le pseudo"):
        st.session_state["username"] = pseudo

    # Vérifier que l'utilisateur a un pseudo
    if "username" not in st.session_state or not st.session_state["username"]:
        st.warning("Veuillez saisir un nom d'utilisateur dans la barre latérale.")
        return

    # Charger/indexer (automatique, si pas déjà fait)
    if "vecteur_store" not in st.session_state or st.session_state["vecteur_store"] is None:
        docs = charger_donnees_json("load_documents")
        st.session_state["vecteur_store"] = preparer_et_indexer_documents(docs, "embeddings")

    # Construire le chatbot (paramètres fixes)
    chatbot = construire_chatbot(
        st.session_state["vecteur_store"],
        temperature=0.3,
        model_name="gpt-3.5-turbo",
        k=2
    )

    # Dictionnaire général qui contient les messages de tous
    if "all_messages" not in st.session_state:
        st.session_state["all_messages"] = {}

    username = st.session_state["username"]

    # Créer la liste de messages pour ce pseudo si n’existe pas
    if username not in st.session_state["all_messages"]:
        st.session_state["all_messages"][username] = []

    user_messages = st.session_state["all_messages"][username]

    # Affichage en mode chat
    for msg in user_messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(f"{username} : {msg['content']}")
        else:
            with st.chat_message("assistant"):
                st.write(msg["content"])

    user_input = st.chat_input("Posez votre question ici...")
    if user_input:
        # Ajout de la question
        user_messages.append({"role": "user", "content": user_input})

        # Appel du chatbot
        reponse = chatbot.invoke({"question": user_input})
        bot_answer = reponse["answer"]
        # Ajout de la réponse
        user_messages.append({"role": "assistant", "content": bot_answer})

        # Affichage direct
        with st.chat_message("assistant"):
            st.write(bot_answer)

    # Possibilité d'effacer l'historique pour CE pseudo
    if st.sidebar.button("Effacer l'historique"):
        st.session_state["all_messages"][username] = []
        st.sidebar.success("Historique effacé (pour votre pseudo)")

if __name__ == "__main__":
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "vecteur_store" not in st.session_state:
        st.session_state["vecteur_store"] = None
    if "all_messages" not in st.session_state:
        st.session_state["all_messages"] = {}
    main()
