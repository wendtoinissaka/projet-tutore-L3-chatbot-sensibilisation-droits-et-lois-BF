import fitz  # PyMuPDF
import json
import re

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def convert_article_number(article_num):
    # Convertir "1er" en "1", ou conserver le numéro tel quel s'il est déjà un nombre
    if article_num.lower() == "1er":
        return 1
    try:
        return int(article_num)  # Conversion en entier si possible
    except ValueError:
        return article_num  # Retourner tel quel si ce n'est pas un nombre valide

def parse_text_to_articles(text):
    # Structure pour contenir les articles
    articles = []

    # Expression régulière pour capturer les articles et leur texte
    # On capture maintenant "1er" en plus des chiffres ordinaires
    article_pattern = re.compile(
        r'(?<=\n)(Art\.\s*((\d+|1er))\s*\.\s*)(.*?)(?=\nArt\.\s*\d+|1er\s*\.\s*|\Z)', 
        re.DOTALL | re.IGNORECASE
    )

    # Extraction des articles
    matches = article_pattern.findall(text)

    for match in matches:
        article_num = match[1]  # Numéro de l'article ("1er" ou un chiffre)
        article_text = match[3]  # Texte de l'article

        # Conversion du numéro d'article (ex. "1er" -> 1)
        converted_article_num = convert_article_number(article_num)

        articles.append({
            "Article": converted_article_num,  # Utiliser le numéro converti
            "Texte": article_text.strip()  # Suppression des espaces superflus
        })

    return articles

def save_articles_to_json(articles, json_path):
    # Sauvegarde des articles sous format JSON
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(articles, json_file, ensure_ascii=False, indent=4)

def main():
    # Chemin vers le fichier PDF du Code des personnes et de la famille
    pdf_path = "./code_famille.pdf"
    
    # Chemin pour sauvegarder le fichier JSON
    json_path = "articles_code_personnes_et_famille1.json"

    # Extraire le texte du PDF
    text = extract_text_from_pdf(pdf_path)

    # Extraire les articles et leurs textes
    articles = parse_text_to_articles(text)

    # Sauvegarder les articles dans un fichier JSON
    save_articles_to_json(articles, json_path)

    print(f"Extraction terminée et sauvegardée dans {json_path}")

if __name__ == "__main__":
    main()
