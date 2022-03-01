from operator import methodcaller
from flask import Flask, request, render_template, redirect, flash, jsonify, session
from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# Ask why we define responses as a string here
RESPONSES = "responses"

@app.route('/')
def home_page():
    """Shows the start page"""
    return render_template('start_page.html', survey=survey)

@app.route('/start', methods=["POST"])
def start_survey():
    session[RESPONSES] = []
    return redirect("/questions/0")


@app.route('/questions/<int:qid>')
# how am i getting qid?
def show_questions(qid):
    """Shows the next question and choices in sequence"""
    responses = session.get(RESPONSES)

    question = survey.questions[qid]
    return render_template('questions.html', qid=qid, question=question)


@app.route('/answer', methods=['POST'])
def handle_response():
    """Save response to question and redirect to next question"""

    # Get 'answer' from input name defined in questions.html
    choice = request.form['answer']

    # add response to the session
    responses=session[RESPONSES]
    responses.append(choice)
    print(responses)
    session[RESPONSES] = responses

    # redirect user to next question using the length of responses and returning the next question of the same key
    return redirect(f"/questions/{len(responses)}")


