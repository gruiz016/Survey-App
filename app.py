from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from random import randint
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = '1123106611'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)


@app.route('/')
def home():
    '''Root route, shows the index.html'''
    session['RESPONSES'] = []
    return render_template('index.html', title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)


@app.route('/questions/<int:num>')
def questions(num):
    '''Renders the questions for the survey'''
    answered = len(session['RESPONSES'])
    end = len(satisfaction_survey.questions)
    if num > answered or answered > num:
        flash('You must complete the survey in order', 'alert')
        return redirect(f'/questions/{answered}')
    return render_template('question.html', num=num, title=satisfaction_survey.title, question=satisfaction_survey.questions)


@app.route('/answer', methods=['POST'])
def answer():
    '''Handles the response from the questions and redirects to the next question'''
    answer = request.form['answer']
    RESPONSE = session['RESPONSES']
    RESPONSE.append(answer)
    session['RESPONSES'] = RESPONSE
    num = len(session['RESPONSES'])
    end = len(satisfaction_survey.questions)
    print(num, end)
    if num == end:
        return redirect('/confirmation')
    return redirect(f'/questions/{num}')


@app.route('/confirmation')
def confirmation():
    '''Displays the completion page'''
    id = randint(1, 300000)
    session[str(id)] = session['RESPONSES']
    return render_template('confirmation.html')
