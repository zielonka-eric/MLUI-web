from flask import render_template, request, send_file
from app import app
from app.MLUI.main.Algorithms.AlgorithmsEnum import Algorithm #replace this
import io

@app.route('/')
@app.route('/api')
@app.route('/api/help')
def help():
    #result = ""
    #for a in Algorithm:
    #    result += str(a.value) + "<br>"
    return render_template('help.txt', algorithms=Algorithm)

@app.route('/api/help/adv')
def help_adv():
    return render_template('help.txt', algorithms=Algorithm, adv=True)

@app.route('/api/model', methods=['POST'])
def model_create():
    if request.mimetype == 'multipart/form-data':
        #create a model
        data = request.form
        files = request.files

        return str(data.get("data")) + " " + request.mimetype
    else:
        pass #error

@app.route('/api/model/<int:id>', methods=['GET'])
def model_status(id):
    pass

@app.route('/api/model/<int:id>/download', methods=['GET'])
def model_download(id):
    pickledModel = b'hello world\n'

    return send_file(
        io.BytesIO(pickledModel),
        mimetype='application/octet-stream',
        as_attachment=True,
        attachment_filename='%s.txt' % id)     #change filename

@app.route('/api/model/<int:id>/stats', methods=['GET'])
def model_stats(id):
    pass