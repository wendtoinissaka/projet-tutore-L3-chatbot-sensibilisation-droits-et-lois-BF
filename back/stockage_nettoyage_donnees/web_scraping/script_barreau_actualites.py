import requests
from bs4 import BeautifulSoup
import json

# URL de la page des actualités
url = "https://www.barreau.bf/actualites/"

# En-têtes pour simuler un navigateur
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
}

# Requête pour obtenir la page
response = requests.get(url, headers=headers)
response.raise_for_status()

# Parser la page HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Dictionnaire pour stocker les données
data = {
    "Ordre des Avocats du Burkina Faso": {
        "Actualités": []
    }
}

# Cibler les articles
articles = soup.select("div.btContent article.btPostSingleItemStandard")

# Pour chaque article, extraire le lien et les autres informations
for article in articles:
    link_element = article.find("h2").find_all("a")[1]
    article_link = link_element['href']

    # Accéder à la page de l'article
    article_response = requests.get(article_link, headers=headers)
    article_response.raise_for_status()
    article_soup = BeautifulSoup(article_response.text, 'html.parser')

    # Extraire les informations requises
    category = article_soup.find("span", class_="btArticleCategories").get_text(strip=True)
    title = article_soup.find("span", class_="bt_bb_headline_content").get_text(strip=True)
    date = article_soup.find("span", class_="btArticleDate").get_text(strip=True)
    description = article_soup.find("div", class_="btArticleContent").get_text(strip=True)

    # Ajouter les données à la liste
    data["Ordre des Avocats du Burkina Faso"]["Actualités"].append({
        "Category": category,
        "Title": title,
        "Date": date,
        "Description": description,
        "Link": article_link
    })

# Enregistrer les données dans un fichier JSON
with open('actualites_du_barreau_bf.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("Données scrappées et enregistrées avec succès.")
