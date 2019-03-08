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
    # returns the model_id
    if request.mimetype == 'multipart/form-data':
        #create a model
        data = request.form
        files = request.files

        return str(data) + " " + request.mimetype
    else:
        pass #error

@app.route('/api/model/<int:model_id>', methods=['GET'])
def model_status(model_id):
    # returns the creation status
    pass

@app.route('/api/model/<int:model_id>/download', methods=['GET'])
def model_download(model_id):
    # returns the pickled model
    pickled_model = b'hello world\n'

    return send_file(
        io.BytesIO(pickled_model),
        mimetype='application/octet-stream',
        as_attachment=True,
        attachment_filename='%s.txt' % id)     #change filename

@app.route('/api/model/<int:model_id>/test', methods=['POST'])
def model_test(model_id):
    # returns the new result_id
    pass

@app.route('/api/model/<int:model_id>/results', methods=['GET'])
def model_results(model_id):
    # returns all of model's testing results
    pass

@app.route('/api/model/<int:model_id>/remove', methods=['POST'])
def model_remove(model_id):
    # returns a confirmation that the model was removed
    pass

@app.route('/api/results/<int:result_id>', methods=['GET'])
def get_results(result_id):
    # returns one set of results
    pass

@app.route('/api/data', methods=['POST'])
def upload_data():
    # returns new data_id
    pass

@app.route('/api/data/<int:data_id>', methods=['GET'])
def data_get(data_id):
    # returns the data file
    pass

@app.route('/api/data/<int:data_id>/remove', methods=['POST'])
def data_remove(data_id):
    # returns a confirmation that the data was removed
    pass