import fitz  # PyMuPDF
import json
import re

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_text_to_articles(text):
    # Structure pour contenir les articles
    articles = []

    # Expression régulière pour capturer les articles et leur texte
    # On cherche des articles qui commencent par un retour à la ligne suivi de "Art." et d'un numéro
    article_pattern = re.compile(
        r'(?<=\n)(Art\.\s*(\d+)\s*\.\s*)(.*?)(?=\nArt\.\s*\d+\s*\.\s*|\Z)', 
        re.DOTALL | re.IGNORECASE
    )

    # Extraction des articles
    matches = article_pattern.findall(text)

    for match in matches:
        article_num = match[1]  # Numéro de l'article
        article_text = match[2]  # Texte de l'article

        articles.append({
            "Article": int(article_num),  # Conversion du numéro en entier
            "Texte": article_text.strip()  # Suppression des espaces superflus
        })

    return articles

def save_articles_to_json(articles, json_path):
    # Sauvegarde des articles sous format JSON
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(articles, json_file, ensure_ascii=False, indent=4)

def main():
    # Chemin vers le fichier PDF
    pdf_path = "code_civil_1.pdf"
    
    # Chemin pour sauvegarder le fichier JSON
    json_path = "extracted_articles.json"

    # Extraire le texte du PDF
    text = extract_text_from_pdf(pdf_path)

    # Extraire les articles et leurs textes
    articles = parse_text_to_articles(text)

    # Sauvegarder les articles dans un fichier JSON
    save_articles_to_json(articles, json_path)

    print(f"Extraction terminée et sauvegardée dans {json_path}")

if __name__ == "__main__":
    main()
