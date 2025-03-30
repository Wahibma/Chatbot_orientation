# 🏫 Chatbot d’Orientation Étudiante



## Table of Contents

- [Technologies Utilisées](#technologies-utilisées)
- [Description](#description)
- [Objectifs](#objectifs)
- [Démo](#démo)
- [Installation](#installation)
- [Usage](#usage)
- [Structure du Projet](#structure-du-projet)
- [Collaborateurs](#collaborateurs)
- [Licence](#licence)

---

## Technologies Utilisées

![Python](https://img.shields.io/badge/Python-3.10%2B-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-00A3E0?style=for-the-badge&logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Chroma](https://img.shields.io/badge/Chroma-00A3E0?style=for-the-badge&logo=chroma&logoColor=white)

---

## Description

Ce projet propose un **chatbot d’orientation** pour les étudiants, basé sur une approche **RAG** (Retrieval-Augmented Generation). Il :

1. **Indexe** des documents (JSON, brochures, FAQs) contenant des informations sur les filières, les débouchés et les conditions d’accès.
2. **Permet** à l’étudiant de poser des questions en langage naturel.
3. **Recherche** dans la base vectorielle (Chroma) les extraits les plus pertinents.
4. **Génère** une réponse grâce à un modèle de langage (OpenAI GPT-3.5, par exemple), en s’appuyant sur les extraits retrouvés.

---

## Objectifs

1. **Fournir** une expérience interactive de questions/réponses sur les filières étudiantes (Licences, Masters, etc.).
2. **Garantir** la fiabilité des réponses via un pipeline RAG (pas d’hallucination majeure).
3. **Améliorer** la communication et l’information pour les futurs étudiants ou les personnes en réorientation.

---

## Démo

![alt text](<WhatsApp Image 2025-03-29 à 19.00.21_57fafa21.jpg>)

- **Localement**, lancez :
  ```bash
  streamlit run app.py
