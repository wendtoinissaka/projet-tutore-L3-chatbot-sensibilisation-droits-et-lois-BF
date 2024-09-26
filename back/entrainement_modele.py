import spacy
from spacy.training import Example
import json

# Charger les données d'entraînement depuis un fichier JSON
def load_train_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    return train_data["train_data"]

# Charger les données d'entraînement
train_data = load_train_data("donne_entrainement_modele.json")  # Mettez le nom de votre fichier JSON

# Créer un modèle vierge francophone
nlp = spacy.blank("fr")

# Ajouter un composant de reconnaissance d'entités nommées (NER)
ner = nlp.add_pipe("ner")

# Ajouter les labels pour les nouvelles entités (PROCEDURE, LOI, TITRE, ARTICLE, etc.)
ner.add_label("PROCEDURE")
ner.add_label("LOI")
ner.add_label("TITRE")
ner.add_label("CHAPITRE")
ner.add_label("SECTION")
ner.add_label("ARTICLE")

# Préparer les données d'entraînement pour SpaCy
def prepare_training_data(train_data, nlp):
    examples = []
    for item in train_data:
        text = item["text"]
        entities = item["entities"]
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, {"entities": [(ent["start"], ent["end"], ent["label"]) for ent in entities]})
        examples.append(example)
    return examples

# Préparer les exemples d'entraînement
train_examples = prepare_training_data(train_data, nlp)

# Configurer l'entraînement du modèle
optimizer = nlp.initialize()

# Entraîner le modèle
for i in range(10):  # Vous pouvez ajuster le nombre d'itérations
    losses = {}
    nlp.update(train_examples, sgd=optimizer, losses=losses)
    print(f"Iteration {i + 1}, Losses: {losses}")

# Sauvegarder le modèle entraîné
nlp.to_disk("modele_lois_procedures")
print("Modèle sauvegardé avec succès dans le dossier 'modele_lois_procedures'.")








# import spacy
# from spacy.training import Example
# import json

# # Charger les données d'entraînement depuis un fichier JSON
# def load_train_data(file_path):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         train_data = json.load(f)
#     return train_data["train_data"]

# # Charger un modèle vierge francophone
# nlp = spacy.blank("fr")

# # Ajouter un composant de reconnaissance d'entités nommées (NER)
# ner = nlp.add_pipe("ner")

# # Ajouter les labels existants
# ner.add_label("PROCEDURE_ADMIN")
# ner.add_label("DROIT_TRAVAIL")  # Vous pouvez ajouter d'autres entités au besoin

# # Charger les données d'entraînement depuis le fichier JSON
# train_data = load_train_data("donnees_entrainement.json")  # Le fichier JSON contenant vos exemples

# # Préparer les données pour l'entraînement
# examples = []
# for item in train_data:
#     text = item["text"]
#     entities = item["entities"]
#     doc = nlp.make_doc(text)
#     example = Example.from_dict(doc, {"entities": [(ent["start"], ent["end"], ent["label"]) for ent in entities]})
#     examples.append(example)

# # Configurer l'entraînement
# optimizer = nlp.initialize()

# # Entraîner le modèle
# for i in range(100):  # Nombre d'itérations d'entraînement (vous pouvez ajuster)
#     nlp.update(examples, sgd=optimizer)

# # Sauvegarder le modèle entraîné
# nlp.to_disk("modele_procedures")
