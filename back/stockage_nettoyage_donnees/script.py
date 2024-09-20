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
    title_pattern = re.compile(r'(TITRE\s+[IVXLCDM]+[\s-]+[A-Z\s]+)')
    chapter_pattern = re.compile(r'(CHAPITRE\s+[IVXLCDM]+[\s-]+[A-Z\s]+)')
    section_pattern = re.compile(r'(Section\s+\d+[\s-]+[A-Z\s]+)')
    article_pattern = re.compile(r'(Art\.\s*\d+)\.\s*(.*)')

    # Find titles, chapters, sections, and articles
    titles = title_pattern.findall(text)
    chapters = chapter_pattern.findall(text)
    sections = section_pattern.findall(text)

    # Process each title separately
    for title in titles:
        title_start = text.find(title)
        title_end = text.find(titles[titles.index(title) + 1]) if (titles.index(title) + 1) < len(titles) else len(text)

        chapter_text = text[title_start:title_end].strip()

        title_entry = {
            "Titre": title.strip(),
            "Chapitres": []
        }

        # Process chapters within the title
        for chapter in chapters:
            chapter_start = chapter_text.find(chapter)
            chapter_end = chapter_text.find(chapters[chapters.index(chapter) + 1]) if (chapters.index(
                chapter) + 1) < len(chapters) else len(chapter_text)

            chapter_text_content = chapter_text[chapter_start:chapter_end].strip()

            chapter_entry = {
                "Titre": chapter.strip(),
                "Sections": []
            }

            # Find sections within the chapter
            for section in sections:
                section_start = chapter_text_content.find(section)
                section_end = chapter_text_content.find(sections[sections.index(section) + 1]) if (sections.index(
                    section) + 1) < len(sections) else len(chapter_text_content)

                section_text = chapter_text_content[section_start:section_end].strip()

                section_entry = {
                    "Titre": section.strip(),
                    "Articles": []
                }

                # Find articles in this section
                articles = article_pattern.findall(section_text)
                for article in articles:
                    article_number, article_text = article
                    section_entry["Articles"].append({
                        "Article": article_number,
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
    json_path = 'stockage_nettoyage_donnees/code_du_travail.json'  # Path to save the JSON file

    # Extract text a PDF
    text = extract_text_from_pdf(pdf_path)

    # Parse text into structured data
    structured_data = parse_text_to_structure(text)

    # Save structured data to JSON file
    save_structure_to_json(structured_data, json_path)

    print(f"Data has been extracted and saved to {json_path}")


if __name__ == "__main__":
    main()
