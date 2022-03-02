from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# *********************************************
# Ask why we define responses this way?
RESPONSES = "responses"
# *********************************************

@app.route('/')
def home_page():
    """Shows the start page"""
    return render_template('start_page.html', survey=survey)

@app.route('/start', methods=["POST"])
def start_survey():
    """Starts a session when user starts survey and redirects to first question page"""
    session[RESPONSES] = []
    username = request.args["name"]
    return redirect("/questions/0", name=username)


@app.route('/questions/<int:qid>')
def show_questions(qid):
    """Shows the next question and choices in sequence"""
    
    # gets the responses already submitted by the user in current session
    responses = session.get(RESPONSES)

    print('****************************************')
    print(session[RESPONSES])
    print('****************************************')
    
    if (responses == None):
        # redirect user accessing question page without starting session
        return redirect('/')

    if (len(responses) == len(survey.questions)):
        # user completed all questions - show thank you page
        return redirect('/complete')

    if (len(responses) != qid):
        # user is trying to access a question out of order
        # number of responses does not match number in question sequence
        
        flash("Please answer all questions in order")
        
        # returns user to the question matching their number of responses
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template('questions.html', qid=qid, question=question)


@app.route('/answer', methods=['POST'])
def handle_response():
    """Save response to session and redirects to next question"""

    # Get 'answer' from input name defined in questions.html
    choice = request.form['answer']

    # add response to the session
    responses=session[RESPONSES]
    responses.append(choice)
    session[RESPONSES] = responses

    # redirect user to next question using the length of responses and returning the next question of the same key
    return redirect(f"/questions/{len(responses)}")


@app.route('/complete')
def complete():
    """User completed all questions - shows thank you page"""
    return render_template('complete.html')