import json
import psycopg2

from database import connect_db

# Connexion à la base de données
conn = connect_db()

cursor = conn.cursor()

# Création de la table si elle n'existe pas
create_table_query = '''
CREATE TABLE IF NOT EXISTS procedures (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50),
    titre VARCHAR(255),
    description_texte TEXT,
    description_pieces_a_fournir TEXT,
    description_cout TEXT,
    description_conditions_acces TEXT,
    source VARCHAR(255)
);
'''
cursor.execute(create_table_query)
conn.commit()

# Chargement des données JSON depuis un fichier
with open('procedures_juridiques_administratives.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Insertion des données dans la base
for type_procedure, categories in data["procedures_juridiques_et_administratives"].items():
    for procedure_key, procedure in categories.items():
        if "description" in procedure:
            description = procedure["description"]
            cursor.execute(
                "INSERT INTO procedures (type, titre, description_texte, description_pieces_a_fournir, description_cout, description_conditions_acces, source) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    type_procedure,
                    procedure["titre"],
                    description.get("texte", ""),
                    ', '.join(description.get("pieces_a_fournir", [])),
                    description.get("cout", ""),
                    ', '.join(description.get("conditions_acces", [])),
                    procedure["source"]
                )
            )
        else:
            print(f"Procedure '{procedure['titre']}' sans description, sautée.")

# Validation et fermeture de la connexion
conn.commit()
cursor.close()
conn.close()
