def get_email_content(notification_message):
    """Retourne le contenu HTML du message."""

    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nouvelle évolution législative</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #1a73e8; /* Couleur principale */
                text-align: center;
            }}
            h2 {{
                color: #333; /* Titre secondaire */
            }}
            p {{
                font-size: 16px;
                line-height: 1.5;
                color: #555;
            }}
            .highlight {{
                background-color: #e8f5e9;
                padding: 10px;
                border-left: 4px solid #4CAF50; /* Bordure verte */
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #888;
                margin-top: 20px;
            }}
            .dark-mode {{
                background-color: #222;
                color: #ddd;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>VEENGE-MAAN-CHATBOT</h1>
            <h2>Nouvelle évolution législative</h2>
            <p>Bonjour,</p>
            <p class="highlight">Nous souhaitons vous informer d'une nouvelle évolution législative importante concernant vos droits :<br/> <strong>{notification_message}</strong></p>
            <p>Merci de votre attention !</p>
            <div class="footer">VEENGE-MAAN VOTRE CHATBOT JURIDIQUE.</div>
            <div class="footer">Ceci est un e-mail automatique, veuillez ne pas répondre.</div>
        </div>
    </body>
    </html>
    """


# # email_template.py

# def get_email_content(notification_message):
#     """Retourne le contenu HTML du message."""
#     return f"""
#     <!DOCTYPE html>
#     <html lang="fr">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Nouvelle Notification</title>
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 background-color: #f4f4f4;
#                 margin: 0;
#                 padding: 20px;
#             }}
#             .container {{
#                 max-width: 600px;
#                 margin: auto;
#                 background: white;
#                 padding: 20px;
#                 border-radius: 5px;
#                 box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
#             }}
#             h1 {{
#                 color: #333;
#                 text-align: center;
#             }}
#             p {{
#                 font-size: 16px;
#                 line-height: 1.5;
#                 color: #555;
#             }}
#             .footer {{
#                 text-align: center;
#                 font-size: 12px;
#                 color: #888;
#                 margin-top: 20px;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>Nouvelle Notification</h1>
#             <p>Bonjour,</p>
#             <p>Une nouvelle notification a été publiée : <strong>{notification_message}</strong></p>
#             <p>Merci de votre attention !</p>
#             <div class="footer">Ceci est un e-mail automatique, veuillez ne pas répondre.</div>
#         </div>
#     </body>
#     </html>
#     """
