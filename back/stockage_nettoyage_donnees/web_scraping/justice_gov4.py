import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time

# URL de base pour la pagination
base_url = 'http://www.justice.gov.bf/index.php/category/info-pratique/'
page_number = 1
data = []

# En-têtes pour imiter un navigateur
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

while True:
    url = f"{base_url}page/{page_number}/" if page_number > 1 else base_url
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Vérifie les erreurs de réponse

        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        articles = soup.find_all('article')

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

                # Récupérer la description complète
                try:
                    article_response = requests.get(href, headers=headers)
                    article_response.raise_for_status()  # Vérifie les erreurs de réponse
                    article_html = article_response.text
                    article_soup = BeautifulSoup(article_html, 'html.parser')
                    content_div = article_soup.find('div', class_='content')

                    if content_div:
                        description = content_div.get_text(strip=True)
                        keywords_index = description.lower().find("mots clés")
                        if keywords_index != -1:
                            description = description[:keywords_index].strip()
                    else:
                        description = 'Description non trouvée'
                except requests.exceptions.RequestException as e:
                    print(f"Erreur lors de la récupération de la description: {str(e)}")
                    description = article.get_text(strip=True)  # Utiliser uniquement la description partielle

                data.append({
                    'Title': title,
                    'Link': href,
                    'Date': date,
                    'Category': category,
                    'Description': description
                })

        next_page = soup.find('a', class_='next page-numbers')
        if next_page:
            page_number += 1
            time.sleep(5)  # Augmenter le délai à 5 secondes
        else:
            break

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération du site: {str(e)}")
        break

# Organiser les données avec les deux en-têtes
output_data = {
    "justice.gov.bf": {
        "Info-Pratique": data
    }
}

# Enregistrer les données dans un fichier JSON
with open('articles_info_pratiques45.json', 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=4)

print(f"Nombre d'articles récupérés : {len(data)}")
