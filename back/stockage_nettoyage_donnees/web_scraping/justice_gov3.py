import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time

# URL de base pour la pagination
base_url = 'http://www.justice.gov.bf/index.php/category/info-pratique/'
page_number = 1
data = []

while True:
    # Construire l'URL de la page
    url = f"{base_url}page/{page_number}/" if page_number > 1 else base_url
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie les erreurs de réponse

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

            if title_tag and date_tag and category_tag:
                title = title_tag.get_text(strip=True)
                href = title_tag.find('a')['href']
                date = date_tag.get_text(strip=True)
                category = category_tag.get_text(strip=True)

                # Récupérer la description complète depuis la page de l'article
                try:
                    article_response = requests.get(href)
                    article_response.raise_for_status()  # Vérifie les erreurs de réponse
                    article_html = article_response.text
                    article_soup = BeautifulSoup(article_html, 'html.parser')
                    content_div = article_soup.find('div', class_='content')
                    description = content_div.find('article').get_text(strip=True) if content_div else 'Description non trouvée'
                except requests.exceptions.RequestException as e:
                    description = f'Erreur lors de la récupération de la description: {str(e)}'

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
            time.sleep(2)  # Délai de 2 secondes entre les requêtes
        else:
            break

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération du site: {str(e)}")
        break

# Enregistrer les données dans un fichier JSON
with open('articles_info_pratiques33.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

# Afficher le nombre d'articles récupérés
print(f"Nombre d'articles récupérés : {len(data)}")
