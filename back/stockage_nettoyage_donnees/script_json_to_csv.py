# import secrets

# # Générer une clé secrète de 32 octets
# secret_key = secrets.token_hex(32)
# print(secret_key)


import pandas as pd

# Charger le fichier JSON
json_file_path = 'stockage_nettoyage_donnees/procedures_juridiques_administratives.json'
df = pd.read_json(json_file_path)

# Exporter en CSV
csv_file_path = 'stockage_nettoyage_donnees/procedures_juridiques_administratives.csv'
df.to_csv(csv_file_path, index=False)



import json
import csv

# Charger le fichier JSON
json_file_path = 'stockage_nettoyage_donnees/procedures_juridiques_administratives.json'

with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Exporter en CSV
csv_file_path = 'stockage_nettoyage_donnees/procedures_juridiques_administratives.csv'

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)

    # Écrire les en-têtes
    writer.writerow(['Type', 'Titre', 'Description', 'Pièces à fournir', 'Coût', 'Conditions d\'accès', 'Source'])

    # Extraire les procédures juridiques
    procedures_juridiques = data.get("procedures_juridiques_et_administratives", {}).get("juridiques", {})
    for procedure in procedures_juridiques.values():
        titre = procedure.get("titre")
        description_texte = procedure.get("description", {}).get("texte", "")
        pieces_a_fournir = ', '.join(procedure.get("description", {}).get("pieces_a_fournir", []))
        cout = procedure.get("description", {}).get("cout", "")
        conditions_acces = ', '.join(procedure.get("description", {}).get("conditions_acces", []))
        source = procedure.get("source", "")
        writer.writerow(['juridique', titre, description_texte, pieces_a_fournir, cout, conditions_acces, source])

    # Extraire les procédures administratives
    procedures_administratives = data.get("procedures_juridiques_et_administratives", {}).get("administratives", {})
    for procedure in procedures_administratives.values():
        titre = procedure.get("titre")
        description_texte = procedure.get("description", {}).get("texte", "")
        pieces_a_fournir = ', '.join(procedure.get("description", {}).get("pieces_a_fournir", []))
        cout = procedure.get("description", {}).get("cout", "")
        conditions_acces = ', '.join(procedure.get("description", {}).get("conditions_acces", []))
        source = procedure.get("source", "")
        writer.writerow(['administrative', titre, description_texte, pieces_a_fournir, cout, conditions_acces, source])

print(f"Conversion terminée. Les données ont été exportées vers {csv_file_path}.")
