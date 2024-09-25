import pdfplumber
import json


# Fonction pour extraire les enregistrements
def extract_data_from_pdf(pdf_path):
    data = {
        "personnes_physiques": {
            "avocats_inscrits": [],
            "avocats_honoraires": []
        },
        "personnes_morales": {
            "societes_civiles": [],
            "liste_de_stage": []
        }
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            print(f"Tables extraites de la page : {tables}")  # Affiche les tables extraites
            for table in tables:
                # SECTION I – PERSONNES PHYSIQUES
                # A – Avocats inscrits : 6 colonnes
                if "Noms et Prénom(s)" in table[0] and "Date de début d’honorariat" in table[0]:
                    for row in table[1:3]:  # Garder seulement 2 enregistrements
                        data["personnes_physiques"]["avocats_inscrits"].append({
                            "N°": row[0],
                            "Date de début d’honorariat": row[1],
                            "Noms et Prénom(s)": row[2],
                            "Adresse": row[3],
                            "Téléphone": row[4],
                            "Email": row[5]
                        })

                # B – Avocats Honoraires : 6 colonnes
                elif "Date d'inscription" in table[0]:
                    for row in table[1:3]:  # Garder seulement 2 enregistrements
                        data["personnes_physiques"]["avocats_honoraires"].append({
                            "N°": row[0],
                            "Date d'inscription": row[1],
                            "Noms et Prénom(s)": row[2],
                            "Adresse": row[3],
                            "Téléphone": row[4],
                            "Email": row[5]
                        })

                # SECTION II : PERSONNES MORALES
                # Sociétés Civiles Professionnelles, Sociétés Civiles de Moyens, Associations : 6 colonnes
                elif "Dénomination" in table[0] and "Date de Création" in table[0]:
                    for row in table[1:3]:  # Garder seulement 2 enregistrements
                        data["personnes_morales"]["societes_civiles"].append({
                            "N°": row[0],
                            "Date de Création": row[1],
                            "Dénomination": row[2],
                            "Adresse": row[3],
                            "Téléphone": row[4],
                            "Fax": row[5],
                            "E-mail": row[6]
                        })

                # LISTE DE STAGE : 6 colonnes
                elif "Liste de stage" in table[0]:
                    for row in table[1:3]:  # Garder seulement 2 enregistrements
                        data["personnes_morales"]["liste_de_stage"].append({
                            "N°": row[0],
                            "Date de Création": row[1],
                            "Dénomination": row[2],
                            "Adresse": row[3],
                            "Téléphone": row[4],
                            "Fax": row[5],
                            "E-mail": row[6]
                        })

    return data


# Sauvegarde dans un fichier JSON
def save_to_json(data, json_path):
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


# Chemins de fichier
pdf_path = 'contact_avocat_Barreau_Burkina.pdf'
json_path = 'mon_fichier.json'

# Extraction et sauvegarde
extracted_data = extract_data_from_pdf(pdf_path)
save_to_json(extracted_data, json_path)

print("Extraction terminée et sauvegardée dans", json_path)
