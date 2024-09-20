import spacy

# Charger le modèle SpaCy (assure-toi d'avoir installé le modèle en exécutant : `python -m spacy download fr_core_news_sm`)
nlp = spacy.load("fr_core_news_sm")


def process_question(question):
    doc = nlp(question)

    # Pour l'instant, on ne fait que retourner les entités reconnues
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    if not entities:
        return "Je n'ai pas pu comprendre votre question. Pouvez-vous reformuler ?"

    # Logique pour correspondre à des lois ou informations légales (à ajouter)
    return f"Entités détectées : {entities}"
