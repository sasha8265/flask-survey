from flask import Flask, request, render_template, redirect, flash, jsonify
from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import personality_quiz, satisfaction_survey, surveys


app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSE = []

@app.route('/')
def home_page():
    """Shows the start page"""
    return render_template('start_page.html')

@app.route('/questions/0')
def show_questions():
    """Shows the start page"""
    return render_template('questions.html')

