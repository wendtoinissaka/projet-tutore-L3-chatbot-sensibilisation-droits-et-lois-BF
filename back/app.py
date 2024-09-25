from flask import Flask
from routes.chatbot import chatbot_blueprint

app = Flask(__name__)

# Enregistrement des routes
app.register_blueprint(chatbot_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
