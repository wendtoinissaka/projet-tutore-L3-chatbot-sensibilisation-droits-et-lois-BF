# import spacy
# from spacy.training import Example

# # Charger un modèle vide francophone
# nlp = spacy.blank("fr")

# # Ajouter un composant de reconnaissance d'entités nommées (NER)
# ner = nlp.add_pipe("ner")

# # Ajouter les labels pour les entités existantes et la nouvelle entité
# ner.add_label("DROIT_TRAVAIL")
# ner.add_label("DROIT_CIVIL")
# ner.add_label("CONTRAVENTION")
# ner.add_label("PROCEDURE")
# ner.add_label("CHATBOT_INFO")  # Nouvelle entité pour les informations sur le chatbot

# # Ensemble de données d'entraînement incluant la nouvelle entité
# TRAIN_DATA = [
#     ("Quels sont mes droits en cas de licenciement abusif ?", {"entities": [(19, 38, "DROIT_TRAVAIL")]}),
#     ("Comment obtenir une carte d'identité ?", {"entities": [(15, 38, "PROCEDURE_ADMIN")]}),
#     ("Que fait ce chatbot ?", {"entities": [(9, 17, "CHATBOT_INFO")]}),
#     ("Quel est le domaine de ce chatbot ?", {"entities": [(16, 24, "CHATBOT_INFO")]}),
#     # Ajoutez d'autres exemples
# ]

# # Préparer les données pour l'entraînement
# examples = []
# for text, annotations in TRAIN_DATA:
#     doc = nlp.make_doc(text)
#     example = Example.from_dict(doc, annotations)
#     examples.append(example)

# # Configurer l'entraînement
# optimizer = nlp.initialize()

# # Entraîner le modèle
# for i in range(100):
#     nlp.update(examples, sgd=optimizer)

# # Sauvegarder le modèle entraîné
# nlp.to_disk("modele_juridique_chatbot_info")
