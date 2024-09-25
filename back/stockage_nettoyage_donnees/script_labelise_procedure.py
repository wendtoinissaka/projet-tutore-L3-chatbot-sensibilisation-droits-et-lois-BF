# import json

# # Charger le fichier JSON
# def charger_fichier_json(chemin_fichier):
#     with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
#         data = json.load(fichier)
#     return data

# # Générer les données formatées
# def generer_donnees_formattees(data):
#     titles = []

#     # Accéder aux données dans la section 'juridiques'
#     procedures_juridiques = data["procedures_juridiques_et_administratives"]["juridiques"]
    
#     for key, procedure in procedures_juridiques.items():
#         titre = procedure['titre']
#         titles.append(titre)

#     # Accéder aux données dans la section 'administratives'
#     procedures_administratives = data["procedures_juridiques_et_administratives"]["administratives"]
    
#     for key, procedure in procedures_administratives.items():
#         titre = procedure['titre']
#         titles.append(titre)

#     return {"titles": titles}

# # Sauvegarder les titres dans un fichier
# def sauvegarder_donnees(chemin_sortie, donnees):
#     with open(chemin_sortie, 'w', encoding='utf-8') as fichier:
#         json.dump(donnees, fichier, ensure_ascii=False, indent=2)

# # Main - Exécuter le script
# if __name__ == "__main__":
#     chemin_fichier = 'procedures_juridiques_administratives.json'  # Remplace avec le chemin de ton fichier
#     chemin_sortie = 'etiquetage_titres_procedures.json'  # Remplace avec le chemin de ton fichier de sortie
    
#     data = charger_fichier_json(chemin_fichier)
#     donnees_formattees = generer_donnees_formattees(data)
#     sauvegarder_donnees(chemin_sortie, donnees_formattees)

#     print(f"Titres sauvegardés dans {chemin_sortie}")

import json

# Charger le fichier JSON
def charger_fichier_json(chemin_fichier):
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        data = json.load(fichier)
    return data

# Générer les données formatées
def generer_donnees_formattees(data):
    train_data = []

    # Accéder aux données dans la section 'juridiques'
    procedures_juridiques = data["procedures_juridiques_et_administratives"]["juridiques"]
    
    for key, procedure in procedures_juridiques.items():
        texte = procedure['titre']
        entities = [
            {
                "start": 7,  # Ajuste cela selon ton besoin
                "end": 15,   # Ajuste cela selon ton besoin
                "label": "PROCEDURE"
            }
        ]
        train_data.append({"text": texte, "entities": entities})

    # Accéder aux données dans la section 'administratives'
    procedures_administratives = data["procedures_juridiques_et_administratives"]["administratives"]
    
    for key, procedure in procedures_administratives.items():
        texte = procedure['titre']
        entities = [
            {
                "start": 0,  # Ajuste cela selon ton besoin
                "end": len(texte),  # Prendre la longueur du texte
                "label": "PROCEDURE"
            }
        ]
        train_data.append({"text": texte, "entities": entities})

    return {"train_data": train_data}

# Sauvegarder les données formatées dans un fichier
def sauvegarder_donnees(chemin_sortie, donnees):
    with open(chemin_sortie, 'w', encoding='utf-8') as fichier:
        json.dump(donnees, fichier, ensure_ascii=False, indent=2)

# Main - Exécuter le script
if __name__ == "__main__":
    chemin_fichier = 'procedures_juridiques_administratives.json'  # Remplace avec le chemin de ton fichier
    chemin_sortie = 'procedures_annotees.json'  # Remplace avec le chemin de ton fichier de sortie
    
    data = charger_fichier_json(chemin_fichier)
    donnees_formattees = generer_donnees_formattees(data)
    sauvegarder_donnees(chemin_sortie, donnees_formattees)

    print(f"Données sauvegardées dans {chemin_sortie}")
