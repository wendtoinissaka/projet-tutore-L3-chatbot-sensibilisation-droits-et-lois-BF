import spacy
from spacy.training import Example
import json

# Charger les données d'entraînement depuis un fichier JSON
def load_train_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    return train_data["train_data"]

# Charger un modèle vierge francophone
nlp = spacy.blank("fr")

# Ajouter un composant de reconnaissance d'entités nommées (NER)
ner = nlp.add_pipe("ner")

# Ajouter les labels existants
ner.add_label("PROCEDURE_ADMIN")
ner.add_label("DROIT_TRAVAIL")  # Vous pouvez ajouter d'autres entités au besoin

# Charger les données d'entraînement depuis le fichier JSON
train_data = load_train_data("donnees_entrainement.json")  # Le fichier JSON contenant vos exemples

# Préparer les données pour l'entraînement
examples = []
for item in train_data:
    text = item["text"]
    entities = item["entities"]
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, {"entities": [(ent["start"], ent["end"], ent["label"]) for ent in entities]})
    examples.append(example)

# Configurer l'entraînement
optimizer = nlp.initialize()

# Entraîner le modèle
for i in range(100):  # Nombre d'itérations d'entraînement (vous pouvez ajuster)
    nlp.update(examples, sgd=optimizer)

# Sauvegarder le modèle entraîné
nlp.to_disk("modele_procedures")
