import json
import psycopg2

# Connexion à la base de données projet_chatbot
conn = psycopg2.connect(
    dbname='projet_chatbot',  # Connexion à la base de données projet_chatbot
    user='issaka',
    password='issaka',
    host='localhost',
    port='5432'
)

cur = conn.cursor()

# Création de la table code_famille si elle n'existe pas encore
create_table_query = '''
CREATE TABLE IF NOT EXISTS code_penale (
    id SERIAL PRIMARY KEY,
    article_num INT UNIQUE,
    texte TEXT
);
'''
cur.execute(create_table_query)
conn.commit()

# Fonction pour insérer les articles dans la table code_famille
def insert_article(article_num, texte):
    try:
        cur.execute("""
            INSERT INTO code_penale (article_num, texte)
            VALUES (%s, %s)
            ON CONFLICT (article_num) DO NOTHING;  -- Ignore si l'article existe déjà
        """, (article_num, texte))
    except Exception as e:
        print(f"Erreur lors de l'insertion de l'article {article_num}: {e}")

# Chargement des données JSON depuis le fichier extrait
with open('./articles_code_penale.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Parcourir les articles et insérer dans la base de données
for article_data in data:
    article_num = article_data["Article"]
    texte = article_data["Texte"]
    
    # Insertion de l'article dans la base de données
    insert_article(article_num, texte)

# Commit des transactions
conn.commit()

# Fermeture de la connexion
cur.close()
conn.close()
