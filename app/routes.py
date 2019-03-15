from flask import render_template, request, send_file, jsonify
import io
from app import app, data_model

dm = data_model.data_model()

@app.route('/')
@app.route('/api')
@app.route('/api/help')
def help():
    algorithms = dm.help()
    return render_template('help.txt', algorithms=algorithms)

@app.route('/api/help/adv')
def help_adv():
    algorithms = dm.help()
    return render_template('help.txt', algorithms=algorithms, adv=True)


@app.route('/api/model', methods=['POST'])
def model_create():
    # returns the model_id
    if request.mimetype == 'multipart/form-data':
        files = request.files
        params = request.form.to_dict()

        alg = params.pop('alg', None)
        data_id = params.pop('data', None)
        data_file = files.get('data')
        
        #create the model
        data = dm.model_create(alg, data_file, data_id, params)
        
        if data['error']:
            return "\nError: " + data.get('errmsg')
        else:
            return "\nModel id: " + data.get('model_id')
    else:
        return "\nIncorrect mimetype. Use 'multipart/form-data'"

@app.route('/api/model/<string:model_id>', methods=['GET'])
def model_status(model_id):
    # returns the creation status
    return dm.model_status(model_id)

@app.route('/api/model/<string:model_id>/download', methods=['GET'])
def model_download(model_id):
    # returns the pickled model
    pickled_model = dm.model_download(model_id)

    return send_file(
        io.BytesIO(pickled_model),
        mimetype='application/octet-stream',
        as_attachment=True,
        attachment_filename='%s.txt' % id)     #change filename

@app.route('/api/model/<string:model_id>/test', methods=['POST'])
def model_test(model_id):
    # returns the new result_id
    if request.mimetype == 'multipart/form-data':
        files = request.files
        params = request.form.to_dict()

        data_id = params.pop('data', None)
        data_file = files.get('data')
        
        #create the model
        data = dm.model_test(model_id, data_file, data_id, params)
        
        if data['error']:
            return "\nError: " + data.get('errmsg')
        else:
            return "\nResult id: " + data.get('result_id')
    else:
        return "\nIncorrect mimetype. Use 'multipart/form-data'"

@app.route('/api/model/<string:model_id>/results', methods=['GET'])
def model_results(model_id):
    # returns all of model's testing results
    return str(dm.model_results(model_id))

@app.route('/api/model/<string:model_id>/remove', methods=['POST'])
def model_remove(model_id):
    # returns a confirmation that the model was removed
    return str(dm.model_remove(model_id))

@app.route('/api/results/<string:result_id>', methods=['GET'])
def get_results(result_id):
    # returns one set of results
    return str(dm.get_results(result_id))

@app.route('/api/data', methods=['POST'])
def upload_data():
    # returns new data_id
    if request.mimetype == 'multipart/form-data':
        #create a model
        data_file = request.files["data"]
        
        data = dm.upload_data(data_file)
        
        if data['error']:
            return "\nError: " + data.get('errmsg')
        else:
            return "\nData id: " + data.get('data_id')
    else:
        return "\nIncorrect mimetype. Use 'multipart/form-data'"

@app.route('/api/data/<string:data_id>', methods=['GET'])
def data_get(data_id):
    # returns the data file
    return dm.data_get(data_id)

@app.route('/api/data/<string:data_id>/remove', methods=['POST'])
def data_remove(data_id):
    # returns a confirmation that the data was removed
    return str(dm.data_remove(data_id))