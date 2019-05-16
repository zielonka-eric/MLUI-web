from app import app, data_model
from amlet.utils import parseDir
from flask import render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import io
import json
import os

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
    if request.is_json:
        all_params = request.get_json()
        app.logger.debug('all_params : %s', all_params)

        alg = all_params.pop('alg', None)
        if alg:
            alg = alg.replace("_", " ")
        else:
            return jsonify({"error": True,
                        "errmsg":
                            "No algorithm was defined (parameter 'alg')."})

        is_img = False
        data_path = all_params.pop('data', '')
        img_dir_path = all_params.pop('img-dir', '')

        if os.path.isfile(data_path):
            # form a list of the data csv files
            data = [ open(data_path, mode='r') ]
        elif os.path.isdir(img_dir_path):
            data = parseDir(img_dir_path)
            is_img = True
        else:
            return jsonify({"error": True,
                        "errmsg":
                            "No data was defined or invalid data filepath. "
                            "(parameter 'data')"})

        #create the model
        response = dm.model_create(alg, data, all_params, is_img)

        return jsonify(response)
    else:
        return jsonify({"error": True,
                        "errmsg":
                            "Incorrect mimetype. Use 'application/json'"})

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
    if request.is_json:
        all_params = request.get_json()
        app.logger.debug('all_params : %s', all_params)

        data_path = all_params.pop('data', '')
        img_dir_path = all_params.pop('img-dir', '')

        if os.path.isfile(data_path):
            # form a list of the data csv files
            data = [ open(data_path, mode='r') ]
        elif os.path.isdir(img_dir_path):
            data = parseDir(img_dir_path)
        else:
            return jsonify({"error": True,
                        "errmsg":
                            "No data was defined or invalid data filepath. "
                            "(parameter 'data')"})

        tests = all_params.pop('tests', None)
        if not tests:
            return jsonify({"error": True,
                        "errmsg":
                            "No tests were defined. (parameter 'tests')"})

        #create the model
        response = dm.model_test(model_id, data, tests)

        return jsonify(response)
    else:
        return jsonify({"error": True,
                        "errmsg":
                            "Incorrect mimetype. Use 'application/json'"})

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
