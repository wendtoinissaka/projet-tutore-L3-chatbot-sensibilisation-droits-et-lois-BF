import json
import psycopg2

from database import connect_db

# Connexion à la base de données projet_chatbot
conn = connect_db()


cur = conn.cursor()

# Création de la table si elle n'existe pas encore
create_table_query = '''
CREATE TABLE IF NOT EXISTS code_travail (
    id SERIAL PRIMARY KEY,
    article_num INT UNIQUE,
    texte TEXT
);

'''
cur.execute(create_table_query)
conn.commit()

# Fonction pour insérer les articles dans la table articles
def insert_article(article_num, texte):
    try:
        cur.execute("""
            INSERT INTO code_travail (article_num, texte)
            VALUES (%s, %s)
            ON CONFLICT (article_num) DO NOTHING;  -- Ignore si l'article existe déjà
        """, (article_num, texte))
    except Exception as e:
        print(f"Erreur lors de l'insertion de l'article {article_num}: {e}")

# Chargement des données JSON depuis un fichier
with open('test_code_du_travail_apres_traitement.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Parcourir les titres, chapitres, sections et articles
for titre_data in data["CODE_TRAVAIL"]["Titres"]:
    for chapitre_data in titre_data["Chapitres"]:
        for section_data in chapitre_data["Sections"]:
            for article_data in section_data["Articles"]:
                article_num = article_data["Article"]
                texte = article_data["Texte"]
                
                # Insertion de l'article dans la base de données
                insert_article(article_num, texte)

# Commit des transactions
conn.commit()

# Fermeture de la connexion
cur.close()
conn.close()
