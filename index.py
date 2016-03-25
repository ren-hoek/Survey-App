from flask import Flask, render_template, request
from forms import SurveyForm
import json
import os

app = Flask(__name__)

#Needs setting as CSRF_ENABLED=True for flask-wtf. Keep secret_key, secret
app.secret_key = ''

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    form = SurveyForm()

    if request.method == 'POST':
        with open ('results.json','a') as json_file:
            result = '{"time":'+ form.time_drop.data +', "score":'+ form.swb_radio.data + '},'
            json_file.write(result)

    form.swb_radio.choices = (
        [(1, "Option 1")
        ,(2, "Option 2")
        ,(3, "Option 3")
        ,(4, "Option 4")
        ,(5, "Option 5")]
    )

    form.time_drop.choices = [(0, "Before presentation"), (1, "After presentation")]

    opts = list(form.swb_radio)

    return render_template('survey.html', form=form, opts=opts)

@app.route('/result')
def result():
    with open ('results.json','r') as text_file:
        survey_data = text_file.readlines()

    survey_data= "[" + survey_data[0][:-1] + "]"

    survey = json.loads(survey_data)

    time = []
    est = []
    cil = []
    ciu = []

    for i in xrange(2):
        scores = []
        scores2 = []
        for result in survey:
            if result["time"] == i :
                scores.append(result["score"])
                scores2.append(result["score"]**2)

        time.append(i)
        mn = float(sum(scores))/len(scores)
        se = ((float(sum(scores2))-float(sum(scores)**2)/len(scores))**(1/2))/(len(scores))**(1/2)
        est.append(mn)
        cil.append(mn-1.96*se)
        ciu.append(mn+1.96*se)


    survey_results = zip(time, est, cil, ciu)
    return render_template('result.html', data=survey_results)

@app.route('/reset')
def reset():
    with open ('results.json','w') as text_file:
        text_file.write('')

    return render_template('reset.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
