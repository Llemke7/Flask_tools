from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__,)
app.config['SECRET_KEY']= 'super_secret_key'

responses = ['Yes', 'No', 'Less than $10,000', 'Yes']

@app.route('/')
def home():
    return render_template('base.html', survey= satisfaction_survey)

@app.route('/questions/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    try:
        if question_id >= len(satisfaction_survey.questions):
            return "Survey or question not found!"
        question = satisfaction_survey.questions[question_id]
        if request.method == 'POST':
            answer = request.form.get('choice')
            responses.append({question_id: answer})
            
            if question_id + 1 < len(satisfaction_survey.questions):
                return redirect(f'/questions/{question_id + 1}')
            else:
                return render_template('thank_you.html')
        return render_template('question.html', survey=satisfaction_survey, question=question, question_id=question_id)
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Error ocurred"

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

