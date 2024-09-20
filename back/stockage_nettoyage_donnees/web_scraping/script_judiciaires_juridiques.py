import requests
from bs4 import BeautifulSoup
import json
import time

# En-têtes pour imiter un navigateur
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Fonction pour récupérer les articles d'une catégorie
def get_articles_from_category(category_name, category_url):
    page_number = 1
    articles_data = []

    while True:
        url = f"{category_url}page/{page_number}/" if page_number > 1 else category_url

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Vérifie si la requête a échoué
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération du site: {str(e)}. Passer à la page suivante.")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
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

                # Récupérer la description avec une gestion simple d'erreurs
                try:
                    article_response = requests.get(href, headers=headers)
                    article_response.raise_for_status()
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    content_div = article_soup.find('div', class_='content')

                    if content_div:
                        description = content_div.get_text(strip=True)
                        # Retirer les "mots clés" de la description
                        keywords_index = description.lower().find("mots clés")
                        if keywords_index != -1:
                            description = description[:keywords_index].strip()
                    else:
                        description = 'Description non trouvée'
                except requests.exceptions.RequestException as e:
                    # En cas d'erreur, on note une description partielle ou un message d'erreur
                    print(f"Erreur lors de la récupération de la description: {str(e)}. Utilisation de la description partielle.")
                    description = 'Description partielle en raison d’une erreur serveur.'

                articles_data.append({
                    'Title': title,
                    'Link': href,
                    'Date': date,
                    'Category': category,
                    'Description': description
                })

        next_page = soup.find('a', class_='next page-numbers')
        if next_page:
            page_number += 1
            time.sleep(10)  # Pause de 10 secondes entre les pages
        else:
            break

    return articles_data

# Organiser les données pour une seule catégorie
def scrape_single_category(category_name, category_url):
    output_data = {
        "justice.gov.bf": {
            category_name: get_articles_from_category(category_name, category_url)
        }
    }

    # Enregistrer les données dans un fichier JSON
    file_name = f'articles_{category_name}_new.json'
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=4)

    print(f"Récupération des articles pour {category_name} terminée. Fichier enregistré sous {file_name}")

# Exemple d'exécution pour une seule catégorie
if __name__ == "__main__":
    # Remplace avec le nom et l'URL de la catégorie que tu souhaites scraper
    category_name = "Judiciaires & Juridiques"
    category_url = "http://www.justice.gov.bf/index.php/category/judiciaires/"

    scrape_single_category(category_name, category_url)
