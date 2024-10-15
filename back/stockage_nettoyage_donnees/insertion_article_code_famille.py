import json
from models.models import db, CodeFamille1  # Assurez-vous d'importer le modèle

# Fonction pour insérer un article
def insert_article(article_num, texte):
    try:
        article = CodeFamille1(article_num=article_num, texte=texte)
        db.session.add(article)
        db.session.commit()
        print(f"Article {article_num} inséré.")
    except Exception as e:
        db.session.rollback()  # Annule la transaction en cas d'erreur
        print(f"Erreur lors de l'insertion de l'article {article_num}: {e}")

# Fonction pour charger et insérer les articles
def load_and_insert_articles_famille(filename, app_context):
    with app_context:  # Utiliser le contexte d'application passé
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Parcourir les articles et insérer dans la base de données
        for article_data in data:
            article_num = article_data["Article"]
            texte = article_data["Texte"]
            insert_article(article_num, texte)

# Si vous souhaitez exécuter ce script directement, décommentez ce qui suit
# if __name__ == "__main__":
#     load_and_insert_articles_famille('articles_code_personnes_et_famille1.json')




# import json
# import psycopg2

# from database import connect_db

# # Connexion à la base de données projet_chatbot
# conn = connect_db()


# cur = conn.cursor()

# # Création de la table code_famille si elle n'existe pas encore
# create_table_query = '''
# CREATE TABLE IF NOT EXISTS code_famille (
#     id SERIAL PRIMARY KEY,
#     article_num INT UNIQUE,
#     texte TEXT
# );
# '''
# cur.execute(create_table_query)
# conn.commit()

# # Fonction pour insérer les articles dans la table code_famille
# def insert_article(article_num, texte):
#     try:
#         cur.execute("""
#             INSERT INTO code_famille (article_num, texte)
#             VALUES (%s, %s)
#             ON CONFLICT (article_num) DO NOTHING;  -- Ignore si l'article existe déjà
#         """, (article_num, texte))
#     except Exception as e:
#         print(f"Erreur lors de l'insertion de l'article {article_num}: {e}")

# # Chargement des données JSON depuis le fichier extrait
# with open('articles_code_personnes_et_famille1.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

# # Parcourir les articles et insérer dans la base de données
# for article_data in data:
#     article_num = article_data["Article"]
#     texte = article_data["Texte"]
    
#     # Insertion de l'article dans la base de données
#     insert_article(article_num, texte)

# # Commit des transactions
# conn.commit()

# # Fermeture de la connexion
# cur.close()
# conn.close()
