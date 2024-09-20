import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

# URL de base pour la pagination
base_url = 'http://www.justice.gov.bf/index.php/category/info-pratique/'
page_number = 1
data = []

while True:
    # Construire l'URL de la page
    url = f"{base_url}page/{page_number}/" if page_number > 1 else base_url
    response = requests.get(url)

    # Vérifier le statut de la réponse
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Trouver tous les articles sur la page
        articles = soup.find_all('article')

        # Si aucune article trouvé, sortir de la boucle
        if not articles:
            break

        for article in articles:
            title_tag = article.find('h3', class_='post_title entry-title')
            date_tag = article.find('span', class_='post_meta_item post_date')
            category_tag = article.find('span', class_='post_meta_item post_categories')
            description_tag = article.find('div', class_='post_content entry-content')

            if title_tag and date_tag and category_tag and description_tag:
                title = title_tag.get_text(strip=True)
                href = title_tag.find('a')['href']
                date = date_tag.get_text(strip=True)
                category = category_tag.get_text(strip=True)
                description = description_tag.get_text(strip=True)

                # Ajouter les données à la liste
                data.append({
                    'Title': title,
                    'Link': href,
                    'Date': date,
                    'Category': category,
                    'Description': description
                })

        # Vérifier s'il y a un lien vers la page suivante
        next_page = soup.find('a', class_='next page-numbers')
        if next_page:
            page_number += 1
        else:
            break
    else:
        print(f"Erreur lors de la récupération du site: {response.status_code} pour l'URL {url}")
        break

# Enregistrer les données dans un fichier JSON
with open('articles_info_pratiques.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

# Afficher le nombre d'articles récupérés
print(f"Nombre d'articles récupérés : {len(data)}")
