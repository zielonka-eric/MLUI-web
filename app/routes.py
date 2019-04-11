from app import app, data_model
from flask import render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import MultiDict
import io
import json

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
        all_params = request.form.copy()

        app.logger.debug('all_params : %s', all_params)
        app.logger.debug('files : %s', files)
        # check if theres the JSON argument 'params'
        params = all_params.pop('params', None)
        if params:
            all_params = MultiDict(json.loads(params)) # change to multidict

        alg = all_params.pop('alg', None).replace("_", " ")
        data_ids = all_params.poplist('data')
        data_files = files.getlist('data')

        #create the model
        response = dm.model_create(alg, data_files, data_ids, all_params)
        
        return jsonify(response)
    else:
        return jsonify({"error": True,
                        "errmsg":
                            "Incorrect mimetype. Use 'multipart/form-data'"})

@app.route('/api/model/<string:model_id>', methods=['GET'])
def model_status(model_id):
    # returns the creation status
    return jsonify(dm.model_status(model_id))

@app.route('/api/model/<string:model_id>/download', methods=['GET'])
def model_download(model_id):
    # returns the pickled model
    pickled_model, response = dm.model_download(model_id)

    if response['error'] == True:
        return jsonify(response), 409
    else:
        return send_file(
            io.BytesIO(pickled_model),
            mimetype='application/octet-stream',
            as_attachment=True,
            attachment_filename='%s.pickle' % model_id)

@app.route('/api/model/<string:model_id>/test', methods=['POST'])
def model_test(model_id):
    # returns the new result_id
    if request.mimetype == 'multipart/form-data':
        files = request.files
        all_params = request.form.copy()

        app.logger.debug('all_params : %s', all_params)
        # check if theres the JSON argument 'params'
        params = all_params.pop('params', None)
        if params:
            all_params = MultiDict(json.loads(params)) # change to multidict

        data_ids = all_params.poplist('data', None)
        data_files = files.getlist('data')
        
        #create the model
        response = dm.model_test(model_id, data_files, data_ids, all_params)
        
        return jsonify(response)
    else:
        return jsonify({"error": True,
                        "errmsg":
                            "Incorrect mimetype. Use 'multipart/form-data'"})

@app.route('/api/model/<string:model_id>/results', methods=['GET'])
def model_results(model_id):
    # returns all of model's testing results
    return jsonify(dm.model_results(model_id))

@app.route('/api/model/<string:model_id>/remove', methods=['POST'])
def model_remove(model_id):
    # returns a confirmation that the model was removed
    return jsonify(dm.model_remove(model_id))

@app.route('/api/results/<string:result_id>', methods=['GET'])
def get_results(result_id):
    # returns one set of results
    return jsonify(dm.get_results(result_id))

@app.route('/api/data', methods=['POST'])
def upload_data():
    # returns new data_id
    if request.mimetype == 'multipart/form-data':
        #create a model
        if "data" not in request.files:
            return jsonify({"error": True, "errmsg": "No data file uploaded.'"})

        data_file = request.files.get("data")
        filename = secure_filename(data_file.filename)
        response = dm.upload_data(data_file, filename)

        return jsonify(response)
    else:
        return jsonify({"error": True,
                        "errmsg":
                            "Incorrect mimetype. Use 'multipart/form-data'"})

@app.route('/api/data/<string:data_id>', methods=['GET'])
def data_get(data_id):
    # returns the data file
    data_file, filename, response = dm.data_get(data_id)

    if response['error'] == True:
        return jsonify(response), 404
    else:
        return send_file(
            io.BytesIO(data_file),
            mimetype='application/octet-stream',
            as_attachment=True,
            attachment_filename=filename)

@app.route('/api/data/<string:data_id>/remove', methods=['POST'])
def data_remove(data_id):
    # returns a confirmation that the data was removed
    return jsonify(dm.data_remove(data_id))