import json
import psycopg2

from database import connect_db

# Connexion à la base de données
conn = connect_db()


cur = conn.cursor()

# Création des tables si elles n'existent pas
create_table_query = '''
DROP TABLE IF EXISTS Articles CASCADE;
DROP TABLE IF EXISTS Sections CASCADE;
DROP TABLE IF EXISTS Chapitres CASCADE;
DROP TABLE IF EXISTS Titres CASCADE;
DROP TABLE IF EXISTS Lois CASCADE;

CREATE TABLE Lois (
    ID SERIAL PRIMARY KEY,
    Nom VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Titres (
    ID SERIAL PRIMARY KEY,
    Nom VARCHAR(255) NOT NULL,
    Lois_ID INT NOT NULL,
    UNIQUE (Nom, Lois_ID),
    FOREIGN KEY (Lois_ID) REFERENCES Lois(ID) ON DELETE CASCADE
);

CREATE TABLE Chapitres (
    ID SERIAL PRIMARY KEY,
    Nom VARCHAR(255) NOT NULL,
    Titres_ID INT NOT NULL,
    UNIQUE (Nom, Titres_ID),
    FOREIGN KEY (Titres_ID) REFERENCES Titres(ID) ON DELETE CASCADE
);

CREATE TABLE Sections (
    ID SERIAL PRIMARY KEY,
    Titre TEXT NOT NULL,
    Chapitres_ID INT,
    UNIQUE (Titre, Chapitres_ID),
    FOREIGN KEY (Chapitres_ID) REFERENCES Chapitres(ID) ON DELETE CASCADE
);

CREATE TABLE Articles (
    ID SERIAL PRIMARY KEY,
    Article TEXT NOT NULL,
    Texte TEXT NOT NULL,
    Sections_ID INT,
    FOREIGN KEY (Sections_ID) REFERENCES Sections(ID) ON DELETE CASCADE
);
'''
cur.execute(create_table_query)
conn.commit()

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

# Chargement des données JSON
with open('test_code_civil_apres_traitement1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Insérer la Loi
nom_loi = data["CODE_CIVIL"]["Nom"]
loi_id = insert_loi(nom_loi)

# Insérer les Titres, Chapitres, Sections et Articles
for titre_data in data["CODE_CIVIL"]["Titres"]:
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


# import json
# import psycopg2


# # Connexion à la base de données
# conn = psycopg2.connect(
#     dbname='projet_chatbot',
#     user='issaka',
#     password='issaka',
#     host='localhost',
#     port='5432'
# )

# cur = conn.cursor()

# # Création de la table si elle n'existe pas
# create_table_query = '''
# CREATE TABLE Lois (
#     ID SERIAL PRIMARY KEY,
#     Nom VARCHAR(255) NOT NULL,
#     Date_Adoption DATE,
#     Description TEXT
# );

# CREATE TABLE Articles (
#     ID SERIAL PRIMARY KEY,
#     Texte TEXT NOT NULL,
#     Lois_ID INT REFERENCES Lois(ID) ON DELETE CASCADE,
#     Date_Creation DATE DEFAULT CURRENT_DATE,
#     Date_Modification DATE,
#     Statut VARCHAR(20) CHECK (Statut IN ('actif', 'abrogé', 'modifié')) DEFAULT 'actif'
# );

# CREATE TABLE Historique_Articles (
#     ID SERIAL PRIMARY KEY,
#     Article_ID INT REFERENCES Articles(ID) ON DELETE CASCADE,
#     Texte_Avant_Modification TEXT,
#     Date_Modification DATE DEFAULT CURRENT_DATE,
#     Motif TEXT
# );

# CREATE TABLE Titres (
#     ID SERIAL PRIMARY KEY,
#     Nom VARCHAR(255) NOT NULL,
#     Lois_ID INT REFERENCES Lois(ID) ON DELETE CASCADE
# );

# CREATE TABLE Chapitres (
#     ID SERIAL PRIMARY KEY,
#     Nom VARCHAR(255) NOT NULL,
#     Titres_ID INT REFERENCES Titres(ID) ON DELETE CASCADE
# );

# CREATE TABLE Sections (
#     ID SERIAL PRIMARY KEY,
#     Titre VARCHAR(255) NOT NULL,
#     Chapitres_ID INT REFERENCES Chapitres(ID) ON DELETE CASCADE
# );

# '''
# cur.execute(create_table_query)
# conn.commit()

# # Charge le fichier JSON
# with open('test_code_civil_apres_traitement.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Insérer la loi
# nom_loi = data["CODE_CIVIL"]["Nom"]
# cur.execute("INSERT INTO Lois (Nom) VALUES (%s) RETURNING ID;", (nom_loi,))
# loi_id = cur.fetchone()[0]

# # Insérer les titres, chapitres, sections et articles
# for titre in data["CODE_CIVIL"]["Titres"]:
#     cur.execute("INSERT INTO Titres (Nom, Lois_ID) VALUES (%s, %s) RETURNING ID;", (titre["Titre"], loi_id))
#     titre_id = cur.fetchone()[0]

#     for chapitre in titre["Chapitres"]:
#         cur.execute("INSERT INTO Chapitres (Nom, Titres_ID) VALUES (%s, %s) RETURNING ID;", (chapitre["Titre"], titre_id))
#         chapitre_id = cur.fetchone()[0]

#         for section in chapitre["Sections"]:
#             cur.execute("INSERT INTO Sections (Titre, Chapitres_ID) VALUES (%s, %s) RETURNING ID;", (section["Titre"], chapitre_id))
#             section_id = cur.fetchone()[0]

#             for article in section["Articles"]:
#                 cur.execute("INSERT INTO Articles (Texte, Lois_ID) VALUES (%s, %s) RETURNING ID;", (article["Texte"], loi_id))
#                 article_id = cur.fetchone()[0]

# # Valider les modifications
# conn.commit()

# # Fermer le curseur et la connexion
# cur.close()
# conn.close()

# print("Données insérées avec succès.")
