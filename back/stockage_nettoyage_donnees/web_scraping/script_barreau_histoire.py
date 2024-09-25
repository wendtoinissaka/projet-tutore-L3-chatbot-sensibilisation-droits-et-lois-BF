import requests
from bs4 import BeautifulSoup
import json

# URL de la page à scraper
url = "https://www.barreau.bf/a-propos/histoire-de-lordre/"

# En-têtes pour imiter un navigateur
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
}

# Envoi de la requête GET
response = requests.get(url, headers=headers)
response.raise_for_status()  # Vérifie si la requête a réussi

# Analyse du HTML avec BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Trouver la section contenant les articles
section = soup.find('section', id='bt_bb_section66ee823034661')

# Liste pour stocker les données scrappées
scraped_data = []

# Vérifier si la section existe
if section:
    # Récupérer tous les articles (divs avec la classe 'bold_timeline_item_inner')
    timeline_items = section.find_all('div', class_='bold_timeline_item_inner')

    # Parcourir chaque article
    for item in timeline_items:
        # Essayer d'extraire la date
        date_element = item.find('p', class_='bold_timeline_item_header_supertitle')
        date = date_element.get_text(strip=True) if date_element else "Date non trouvée"

        # Essayer d'extraire le titre
        # title_element = item.find('h2', class_='bold_timeline_item_header_title')
        title_element = item.find(class_='bold_timeline_item_header_title')
        title = title_element.get_text(strip=True) if title_element else "Titre non trouvé"

        # Essayer d'extraire la description
        description_element = item.find('div', class_='bold_timeline_item_text_inner')
        description = description_element.get_text(strip=True) if description_element else "Description non trouvée"

        # Essayer d'extraire l'image
        image_element = item.find('img')
        image = image_element['src'] if image_element else "Image non trouvée"

        # Ajouter les données à la liste
        scraped_data.append({
            'Date': date if date != "Date non trouvée" else "Date non trouvée",
            'Title': title if title != "Titre non trouvé" else "Titre non trouvé",
            'Description': description,
            'Image': image,
            'Link': url  # Ajouter le lien source
        })

# Organiser les données sous un format JSON
output_data = {
    "Ordre des Avocats du Burkina Faso": {
        "Histoire du Barreau burkinabè": scraped_data
    }
}

# Enregistrer les données dans un fichier JSON
with open('histoire_du_barreau_bf.json', 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=4)

print("Données scrappées et enregistrées avec succès dans 'histoire_du_barreau_bf.json'.")
