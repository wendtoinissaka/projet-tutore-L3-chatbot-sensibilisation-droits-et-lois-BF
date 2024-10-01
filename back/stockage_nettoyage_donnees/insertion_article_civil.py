import json
import psycopg2

# Connexion à la base de données
conn = psycopg2.connect(
    dbname='projet_chatbot',
    user='issaka',
    password='issaka',
    host='localhost',
    port='5432'
)

cur = conn.cursor()

# Création de la table si elle n'existe pas encore
create_table_query = '''
CREATE TABLE IF NOT EXISTS code_civil (
    id SERIAL PRIMARY KEY,   -- L'identifiant auto-incrémenté
    article_num INT UNIQUE,  -- Le numéro de l'article, doit être unique
    texte TEXT               -- Le texte de l'article
);
'''
cur.execute(create_table_query)
conn.commit()

# Fonction pour insérer un article
def insert_article(article_num, texte):
    try:
        cur.execute("INSERT INTO code_civil (article_num, texte) VALUES (%s, %s) RETURNING id;", (article_num, texte))
        return cur.fetchone()[0]  # Retourne l'id de l'article inséré
    except psycopg2.IntegrityError:
        conn.rollback()  # Annule la transaction en cas de doublon
        print(f"Article num {article_num} déjà existant, ignoré.")
        return None  # Retourne None si l'insertion échoue

# Chargement des données
with open('test_code_civil_apres_traitement2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Insertion des articles 1 à 6
for titre_data in data["CODE_CIVIL"]["Titres"]:
    for chapitre_data in titre_data["Chapitres"]:
        for section_data in chapitre_data["Sections"]:
            for article_data in section_data["Articles"]:
                try:
                    article_num = int(article_data["Article"])  # Essayer de convertir en entier
                    if article_num <= 6:
                        article_id = insert_article(article_num, article_data["Texte"])
                except ValueError:
                    print(f"Article ignoré : {article_data['Article']} (non numérique)")
                    continue  # Ignorer les articles avec des numéros non numériques

# 2. Insertion des articles de 7 à 515 avec le texte abrogé
texte_abroge = "Abrogés par l’art. 1067 de la zatu an VII 13 du 16 novembre 1989 portant institution et application d’un code des personnes et de la famille."
for article_num in range(7, 516):
    insert_article(article_num, texte_abroge)  # Insère l'article avec le texte abrogé

# 3. Insertion des articles après 515
for titre_data in data["CODE_CIVIL"]["Titres"]:
    for chapitre_data in titre_data["Chapitres"]:
        for section_data in chapitre_data["Sections"]:
            for article_data in section_data["Articles"]:
                try:
                    article_num = int(article_data["Article"])  # Essayer de convertir en entier
                    if article_num > 515:
                        insert_article(article_num, article_data["Texte"])
                except ValueError:
                    print(f"Article ignoré : {article_data['Article']} (non numérique)")
                    continue  # Ignorer les articles avec des numéros non numériques

# Commit des transactions
conn.commit()

# Fermeture de la connexion
cur.close()
conn.close()

print("Articles insérés avec succès.")
