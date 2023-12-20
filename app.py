from flask import Flask, render_template, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__,)
app.config['SECRET_KEY']= 'secretkey'

responses = []

@app.route('/')
def home():
    return render_template('base.html', survey= satisfaction_survey, display=False)

@app.route('/questions/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    try:
        if question_id >= len(satisfaction_survey.questions):
            return "Survey or question not found!"

        question = satisfaction_survey.questions[question_id]
        if request.method == 'POST':
            answer = request.form.get('choice')
            session_responses = session.get('responses', [])
            session_responses.append({question_id: answer})

            session['responses'] = session_responses

            if question_id + 1 < len(satisfaction_survey.questions):
                return redirect(f'/questions/{question_id + 1}')
            else:
                return render_template('thank_you.html')

        return render_template('question.html', survey=satisfaction_survey, question=question, question_id=question_id)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Error occurred"

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')
