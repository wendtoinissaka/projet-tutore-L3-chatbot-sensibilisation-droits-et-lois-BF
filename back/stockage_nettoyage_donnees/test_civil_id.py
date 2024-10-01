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
    article_pattern = re.compile(
        r'(Art\.\s*(\d+)[^\s]*\s*[\.\s]*)\s*(.*?)(?=(?:\s*Art\.\s*\d+|\Z))',
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


# import fitz  # PyMuPDF
# import json
# import re


# def extract_text_from_pdf(pdf_path):
#     doc = fitz.open(pdf_path)
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     return text


# def parse_text_to_structure(text):
#     structure = {
#         "Loi": {
#             "Nom": "CODE CIVIL DE 1804 du Burkina Faso",
#             "Articles": []
#         }
#     }

#     # Define pattern for articles (extracting numeric article numbers only)
#     article_pattern = re.compile(r'(Art\.\s*(\d+)[^\s]*\s*[\.\s]*)\s*(.*?)(?=(?:\s+Art\.|\Z))', re.DOTALL | re.IGNORECASE)

#     # Find all articles
#     articles = article_pattern.findall(text)

#     # Process each article and add it to the structure
#     for _, article_number, article_text in articles:
#         structure["Loi"]["Articles"].append({
#             "Article": int(article_number),  # Store the article number as an integer
#             "Texte": article_text.strip()
#         })

#     return structure


# def save_structure_to_json(structure, json_path):
#     with open(json_path, 'w', encoding='utf-8') as json_file:
#         json.dump(structure, json_file, ensure_ascii=False, indent=4)


# def main():
#     # Path to your PDF file
#     pdf_path = "code_civil_1.pdf"
#     # Path to save the JSON file
#     json_path = "extracted_articles_numeric.json"

#     # Extract text from PDF
#     text = extract_text_from_pdf(pdf_path)

#     # Parse text into structured data (only articles)
#     structured_data = parse_text_to_structure(text)

#     # Save structured data to JSON file
#     save_structure_to_json(structured_data, json_path)

#     print(f"Articles have been extracted and saved to {json_path}")


# if __name__ == "__main__":
#     main()
