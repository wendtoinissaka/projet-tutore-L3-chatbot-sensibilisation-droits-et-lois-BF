import fitz  # PyMuPDF
import json
import re


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def parse_text_to_structure(text):
    structure = {
        "Loi": {
            "Nom": "28-2008/AN du 13 mai 2008 portant code du travail au Burkina Faso",
            "Titres": []
        }
    }

    # Define patterns for titles, chapters, sections, and articles
    title_pattern = re.compile(r'(TITRE\s+[IVXLCDM]+\s*[-]?\s*[A-Z\s,\'’]+)(?=\s+TITRE\s+[IVXLCDM]|\s+CHAPITRE|\s+Section|\s+Art\.|\Z)', re.IGNORECASE)
    chapter_pattern = re.compile(r'(CHAPITRE\s+[IVXLCDM]+\s*[-]?\s*[A-Z\s,\'’]+)(?=\s+CHAPITRE|\s+Section|\s+Art\.|\Z)', re.IGNORECASE)
    section_pattern = re.compile(r'(Section\s+\d+\s*[-]?\s*[A-Z\s,\'’]+)(?=\s+Section|\s+Art\.|\Z)', re.IGNORECASE)
    article_pattern = re.compile(r'(Art\.\s*\d+[^\s]*\s*[\.\s]*)\s*(.*?)(?=(?:\s+Art\.|\Z))', re.DOTALL | re.IGNORECASE)

    # Find titles
    titles = title_pattern.findall(text)
    for title in titles:
        title_start = text.find(title)
        title_end = text.find(titles[titles.index(title) + 1]) if (titles.index(title) + 1) < len(titles) else len(text)

        title_text = text[title_start:title_end].strip()

        title_entry = {
            "Titre": title.strip(),
            "Chapitres": []
        }

        # Find chapters within the title
        chapters = chapter_pattern.findall(title_text)
        if not chapters:  # Handle cases where there are no chapters
            articles = article_pattern.findall(title_text)
            if articles:
                title_entry["Chapitres"].append({
                    "Titre": "Articles uniquement",
                    "Sections": [{
                        "Titre": "Articles",
                        "Articles": [
                            {"Article": article_number.strip(), "Texte": article_text.strip()}
                            for article_number, article_text in articles
                        ]
                    }]
                })
        else:
            for chapter in chapters:
                chapter_start = title_text.find(chapter)
                chapter_end = title_text.find(chapters[chapters.index(chapter) + 1]) if (chapters.index(chapter) + 1) < len(chapters) else len(title_text)

                chapter_text = title_text[chapter_start:chapter_end].strip()

                chapter_entry = {
                    "Titre": chapter.strip(),
                    "Sections": []
                }

                # Find sections within the chapter
                sections = section_pattern.findall(chapter_text)
                if not sections:  # Handle cases where there are no sections
                    articles = article_pattern.findall(chapter_text)
                    if articles:
                        chapter_entry["Sections"].append({
                            "Titre": "Articles uniquement",
                            "Articles": [
                                {"Article": article_number.strip(), "Texte": article_text.strip()}
                                for article_number, article_text in articles
                            ]
                        })
                else:
                    for section in sections:
                        section_start = chapter_text.find(section)
                        section_end = chapter_text.find(sections[sections.index(section) + 1]) if (sections.index(section) + 1) < len(sections) else len(chapter_text)

                        section_text = chapter_text[section_start:section_end].strip()

                        section_entry = {
                            "Titre": section.strip(),
                            "Articles": []
                        }

                        # Find articles in this section
                        articles = article_pattern.findall(section_text)
                        for article_number, article_text in articles:
                            section_entry["Articles"].append({
                                "Article": article_number.strip(),
                                "Texte": article_text.strip()
                            })

                        chapter_entry["Sections"].append(section_entry)

                title_entry["Chapitres"].append(chapter_entry)

        structure["Loi"]["Titres"].append(title_entry)

    return structure


def save_structure_to_json(structure, json_path):
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(structure, json_file, ensure_ascii=False, indent=4)


def main():
    pdf_path = 'stockage_nettoyage_donnees/code_du_travail.pdf'  # Path to your PDF file
    json_path = 'stockage_nettoyage_donnees/code_du_travail_apres_traitement.json'  # Path to save the JSON file

    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)

    # Parse text into structured data
    structured_data = parse_text_to_structure(text)

    # Save structured data to JSON file
    save_structure_to_json(structured_data, json_path)

    print(f"Data has been extracted and saved to {json_path}")


if __name__ == "__main__":
    main()
