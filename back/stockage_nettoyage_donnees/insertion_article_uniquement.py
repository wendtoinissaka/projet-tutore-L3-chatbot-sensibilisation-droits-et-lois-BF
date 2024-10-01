import psycopg2

# Connexion à la base de données
def create_table():
    conn = psycopg2.connect(
        dbname='projet_chatbot',
        user='issaka',
        password='issaka',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()

    # Création de la table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS code_civil (
        id SERIAL PRIMARY KEY,    -- Identifiant auto-incrémenté
        article_num INT UNIQUE,   -- Numéro de l'article, unique
        texte TEXT                -- Texte de l'article
    );
    '''
    cur.execute(create_table_query)
    conn.commit()

    cur.close()
    conn.close()
    print("Table créée ou existante vérifiée.")

# Insertion des articles dans la base de données
def insert_articles_to_db(articles):
    conn = psycopg2.connect(
        dbname='projet_chatbot',
        user='issaka',
        password='issaka',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()

    # Insertion des articles
    for article in articles:
        article_num = article["Article"]
        texte = article["Texte"]

        # Préparer la requête d'insertion
        insert_query = '''
        INSERT INTO code_civil (article_num, texte)
        VALUES (%s, %s)
        ON CONFLICT (article_num) DO NOTHING;
        '''
        cur.execute(insert_query, (article_num, texte))

    conn.commit()
    cur.close()
    conn.close()
    print("Les articles ont été insérés dans la base de données.")

# Articles de 1 à 6 avec leur texte spécifique
articles_1_to_6 = [
    {"Article": 1, "Texte": "Les lois sont exécutoires dans tout le territoire [burkinabè] en vertu de la promulgation qui en est faite par [le Président du Faso]. Elles seront exécutées dans chaque partie du [Faso] du moment où la promulgation en pourra être connue."},
    {"Article": 2, "Texte": "La loi ne dispose que pour l'avenir, elle n'a point d'effet rétroactif."},
    {"Article": 3, "Texte": "Les lois de police et de sûreté obligent tous ceux qui habitent le territoire. Les immeubles, même ceux possédés par des étrangers, sont régis par la loi [burkinabè]."},
    {"Article": 4, "Texte": "Le juge qui refusera de juger, sous prétexte du silence, de l'obscurité ou de l'insuffisance de la loi, pourra être poursuivi comme coupable de déni de justice."},
    {"Article": 5, "Texte": "Il est défendu aux juges de se prononcer par voie de disposition générale et réglementaire sur les causes qui leur sont soumises."},
    {"Article": 6, "Texte": "On ne peut déroger, par des conventions particulières, aux lois qui intéressent l'ordre public et les bonnes mœurs."}
]

# Articles de 7 à 515 avec le texte générique
def generate_articles_7_to_515():
    articles = []
    texte_abroge = "Abrogés par l’art. 1067 de la zatu an VII 13 du 16 novembre 1989 portant institution et application d’un code des personnes et de la famille."
    
    for i in range(7, 516):
        articles.append({
            "Article": i,
            "Texte": texte_abroge
        })
    
    return articles

# Fonction principale
def main():
    # Créer la table si nécessaire
    create_table()

    # Générer et insérer les articles de 1 à 6
    insert_articles_to_db(articles_1_to_6)

    # Générer et insérer les articles de 7 à 515
    articles_7_to_515 = generate_articles_7_to_515()
    insert_articles_to_db(articles_7_to_515)

if __name__ == "__main__":
    main()
