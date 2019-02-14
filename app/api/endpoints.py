from flask import render_template, request
from app import app
from app.MLUI.main.Algorithms.AlgorithmsEnum import Algorithm


@app.route('/api')
@app.route('/api/help')
def help():
    result = ""
    for a in Algorithm:
        result += str(a.value) + "<br>"
    return render_template('help.txt', algorithms=Algorithm)

@app.route('/api/help/adv')
def help_adv():
    return render_template('help.txt', algorithms=Algorithm, adv=True)

@app.route('/api/model', methods=['POST'])
def model():
    #create a model

    data = request.form
    files = request.files

    return str(data)
