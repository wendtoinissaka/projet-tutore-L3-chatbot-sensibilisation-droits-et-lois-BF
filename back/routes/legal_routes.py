from flask import Flask, jsonify, request
from app import app, db
from database.models import Law, Lawyer, Question


# from app.models import Law, Lawyer, Question

@app.route('/laws', methods=['GET'])
def get_laws():
    laws = Law.query.all()
    return jsonify([law.to_dict() for law in laws])

@app.route('/lawyers', methods=['GET'])
def get_lawyers():
    lawyers = Lawyer.query.all()
    return jsonify([lawyer.to_dict() for lawyer in lawyers])

@app.route('/questions', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    return jsonify([question.to_dict() for question in questions])

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json['question']
    # Simulation de réponse basique
    answer = 'Réponse à votre question : '+ question
    new_question = Question(question, answer)
    db.session.add(new_question)
    db.session.commit()
    return jsonify({'response': answer})