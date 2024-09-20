import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL du site à scraper
# url = 'http://www.justice.gov.bf/'  # Remplace par l'URL spécifique si nécessaire
url = "http://www.justice.gov.bf/index.php/category/info-pratique/"
# Faire une requête GET pour récupérer le contenu HTML
response = requests.get(url)

# Vérifier que la requête a réussi
if response.status_code == 200:
    html_content = response.text

    # Parser le contenu HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Liste pour stocker les données
    data = []

    # Trouver tous les articles
    articles = soup.find_all('article')

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

    # Créer un DataFrame nommé articles_info_pratiques
    articles_info_pratiques = pd.DataFrame(data)

    # Afficher le DataFrame
    print(articles_info_pratiques)
else:
    print(f"Erreur lors de la récupération du site: {response.status_code}")
articles_info_pratiques.to_csv('./articles_info_pratiques.csv', index=False)
