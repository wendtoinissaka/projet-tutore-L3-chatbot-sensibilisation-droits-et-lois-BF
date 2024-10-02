import json
import psycopg2

from database import connect_db

# Connexion à la base de données
conn = connect_db()


cur = conn.cursor()

# Fonctions pour insérer les données
def insert_loi(nom_loi):
    cur.execute("INSERT INTO Lois (Nom) VALUES (%s) RETURNING ID;", (nom_loi,))
    return cur.fetchone()[0]

def insert_titre(nom_titre, loi_id):
    cur.execute("""
        INSERT INTO Titres (Nom, Lois_ID)
        VALUES (%s, %s)
        ON CONFLICT (Nom, Lois_ID) DO NOTHING
        RETURNING ID;
    """, (nom_titre, loi_id))
    return cur.fetchone()[0] if cur.rowcount > 0 else get_titre_id(nom_titre, loi_id)

def get_titre_id(nom_titre, loi_id):
    cur.execute("SELECT ID FROM Titres WHERE Nom = %s AND Lois_ID = %s;", (nom_titre, loi_id))
    return cur.fetchone()[0]

def insert_chapitre(nom_chapitre, titre_id):
    cur.execute("""
        INSERT INTO Chapitres (Nom, Titres_ID)
        VALUES (%s, %s)
        ON CONFLICT (Nom, Titres_ID) DO NOTHING
        RETURNING ID;
    """, (nom_chapitre, titre_id))
    return cur.fetchone()[0] if cur.rowcount > 0 else get_chapitre_id(nom_chapitre, titre_id)

def get_chapitre_id(nom_chapitre, titre_id):
    cur.execute("SELECT ID FROM Chapitres WHERE Nom = %s AND Titres_ID = %s;", (nom_chapitre, titre_id))
    return cur.fetchone()[0]

def insert_section(titre_section, chapitre_id):
    cur.execute("""
        INSERT INTO Sections (Titre, Chapitres_ID)
        VALUES (%s, %s)
        ON CONFLICT (Titre, Chapitres_ID) DO NOTHING
        RETURNING ID;
    """, (titre_section, chapitre_id))
    return cur.fetchone()[0] if cur.rowcount > 0 else get_section_id(titre_section, chapitre_id)

def get_section_id(titre_section, chapitre_id):
    cur.execute("SELECT ID FROM Sections WHERE Titre = %s AND Chapitres_ID = %s;", (titre_section, chapitre_id))
    return cur.fetchone()[0]

def insert_article(article, texte, section_id):
    cur.execute("INSERT INTO Articles (Article, Texte, Sections_ID) VALUES (%s, %s, %s);", (article, texte, section_id))

# Chargement des données JSON depuis un fichier
with open('test_code_du_travail_apres_traitement.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Insérer la Loi
nom_loi = data["CODE_TRAVAIL"]["Nom"]
loi_id = insert_loi(nom_loi)

# Insérer les Titres, Chapitres, Sections et Articles
for titre_data in data["CODE_TRAVAIL"]["Titres"]:
    titre_nom = titre_data["Titre"]
    titre_id = insert_titre(titre_nom, loi_id)
    
    for chapitre_data in titre_data["Chapitres"]:
        chapitre_nom = chapitre_data["Titre"]
        chapitre_id = insert_chapitre(chapitre_nom, titre_id)
        
        for section_data in chapitre_data["Sections"]:
            section_titre = section_data["Titre"]
            section_id = insert_section(section_titre, chapitre_id)
            
            for article_data in section_data["Articles"]:
                insert_article(article_data["Article"], article_data["Texte"], section_id)

# Commit des transactions
conn.commit()

# Fermeture de la connexion
cur.close()
conn.close()
