# import spacy
# from database.models import LoiTravail, LoiCivil
#
# nlp = spacy.load('fr_core_news_md')  # Modèle SpaCy en français
#
# def process_question(question):
#     doc = nlp(question)
#     keywords = [token.lemma_ for token in doc if not token.is_stop]
#
#     # Logique pour interroger la base de données selon les mots-clés
#     if "travail" in keywords:
#         lois = LoiTravail.query.all()
#     elif "civil" in keywords:
#         lois = LoiCivil.query.all()
#     else:
#         return "Désolé, je n'ai pas trouvé de réponse."
#
#     result = [{"titre": loi.titre, "article": loi.article} for loi in lois]
#     return result
