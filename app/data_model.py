from app import query_db, app
from amlet import amlet_engine
from amlet.library.algorithms import AlgorithmsEnum
import string
import random
import io
import json
import sqlite3
import pickle

class data_model:
    def __init__(self):
        self.engine = amlet_engine.AMLET_Engine(self)

    def help(self):
        # get dict of algorithms from amlet
        return AlgorithmsEnum.Algorithm

    def model_create(self, algorithm, data_files, params, is_img):
        # set up return value
        response = dict(error=False, errmsg="")

        while True:
            # create new random model_id
            model_id = ''.join(
                random.choices(string.ascii_letters + string.digits, k=10))

            # check for id collision in database
            c_res = query_db("SELECT COUNT() FROM Models WHERE model_id = ?;",
                             [model_id], one=True)

            if c_res[0] == 0:
                break

        # create the params dict for amlet's createModel()
        if is_img:
            params_dict = {
                "DataParams" : {
                    "Scheme": "Images",
                    "Scheme Specific": {
                        #"Color Space": "RGB"  # L is black and white, if you get memory errors using RGB(A) try using L (for now)
                        #"Dimensions": (int, int) # resizes all images in a dataset to this size
                    }
                },
                "AlgParams" : params
            }
        else:
            params_dict = {
                "DataParams" : {
                    "Scheme" : "Row Based Examples CSV",
                    "Scheme Specific" : {
                        "Training Cols" : params.pop('train'),
                        "Target Col" : [ params.pop('target') ]  # change with amlet update
                    }
                },
                "AlgParams" : params
            }

        app.logger.info('creating model %s', model_id)
        app.logger.debug('algorithm : %s', algorithm)
        app.logger.debug('params_dict : %s', params_dict)
        app.logger.debug('data_files : %s', data_files)

        # call amlet_engine's createModel()
        success = self.engine.createModel(algorithm, params_dict,
                                          data_files, model_id)

        if not success:
            response['error'] = True
            response['errmsg'] = "There was an error creating the model."
            return response

        # insert row into database for the new model
        query_db("INSERT INTO Models (model_id, is_finished) VALUES (?, ?);",
                 [model_id, 0])

        #return model_id or any error message
        response['model_id'] = model_id
        return response

    def model_status(self, model_id):
        # set up return value
        response = dict(error=False, errmsg="")

        # check model table in database for status of model_id
        s_res = query_db("SELECT is_finished FROM Models WHERE model_id = ?;",
                         [model_id], one=True)
        # check if there is no model with that id
        if s_res is None:
            response['error'] = True
            response['errmsg'] = "No model with that id."
            return response
        status = s_res[0]

        # if status is not finished, check amlet
        if status == 0:
            response['status'] = self.engine.getStatus(model_id)
            #response['status'] = "not done"
        elif status == 1:
            response['status'] = "done"
        elif status == 2:
            response['status'] = "error creating model"

        # return status
        return response

    def model_download(self, model_id):
        # set up return value
        model = None
        response = dict(error=False, errmsg="")

        # check model table in database for status of model_id
        s_res = query_db("SELECT is_finished FROM Models WHERE model_id = ?;",
                         [model_id], one=True)
        # check if there is no model with that id
        if s_res is None:
            response['error'] = True
            response['errmsg'] = "No model with that id."
            return model, response
        status = s_res[0]

        # if status is not finished, error
        if status == 0: # not finished
            response['error'] = True
            response['errmsg'] = "Model is not finished being trained."
        elif status == 1: # finished
            m_res = query_db("SELECT model FROM Models WHERE model_id = ?;",
                             [model_id], one=True)
            model = m_res[0]
        elif status == 2: # error creating model
            response['error'] = True
            response['errmsg'] = "There was an error training the model."

        # return the model bytestream from the database
        return model, response

    def model_test(self, model_id, data_files, tests):
        # set up return value
        response = dict(error=False, errmsg="")

        while True:
            # create new random result_id
            result_id = ''.join(
                random.choices(string.ascii_letters + string.digits, k=10))

            # check for id collision in database
            c_res = query_db("SELECT COUNT() FROM Results WHERE result_id = ?;",
                             [result_id], one=True)

            if c_res[0] == 0:
                break

        # get the model from the database
        m_res = query_db("SELECT model FROM Models WHERE model_id = ?;",
                         [model_id], one=True)
        if m_res:
            model = pickle.loads(m_res[0])
        else:
            response['error'] = True
            response['errmsg'] = "No model provided or invalid model_id"
            return response

        app.logger.info('testing model %s\n'
                        '\tresult_id %s', model_id, result_id)
        app.logger.debug('tests : %s', tests)
        app.logger.debug('data_files : %s', data_files)

        # send model and data to amlet
        success = self.engine.testModel(model, tests, data_files, result_id)

        if not success:
            response['error'] = True
            response['errmsg'] = "There was an error creating the model."
            return response

        # insert row into database for the new testing result
        query_db("INSERT INTO Results (result_id, model_id, is_finished) "
                 "VALUES (?, ?, ?);",
                 [result_id, model_id, 0])

        #return result_id or any error message
        if response['error'] == False:
            response['result_id'] = result_id
        return response

    def model_results(self, model_id):
        # set up return value
        response = dict(error=False, errmsg="")

        # check results table, get all rows with model_id
        r_res = query_db("SELECT result_id, results FROM Results "
                           "WHERE model_id = ?;",
                         [model_id])
        # check if there are no sets of results with that id
        if not r_res:
            response['error'] = True
            response['errmsg'] = "No results with that model_id."
            return response

        # return the list of results JSONs
        response['results'] = [ { 'result_id' : r['result_id'],
                                  'results' : json.loads(r['results'])
                                    if r['results'] else 'no results yet' }
                                for r in r_res ]
        return response

    def model_remove(self, model_id):
        # set up return value
        response = dict(error=False, errmsg="")

        # check that the model_id exists
        s_res = query_db("SELECT COUNT() FROM Models WHERE model_id = ?",
                         [model_id], one=True)
        if s_res[0] == 0:
            response['error'] = True
            response['errmsg'] = ( "There is no model with model_id of %s" %
                (model_id) )
            return response

        # TODO: remove model from amlet if it's being created

        # delete model with model_id from database
        query_db("DELETE FROM Models WHERE model_id = ?;",
                 [model_id])

        # delete results with this model_id from database
        query_db("DELETE FROM Results WHERE model_id = ?;",
                 [model_id])

        # return confirmation
        response['confirmation'] = ( 'Model %s and all of its ' +
                                     'results were removed' ) % (model_id)
        return response

    def get_results(self, result_id):
        # set up return value
        response = dict(error=False, errmsg="")

        # get results JSON from database
        r_res = query_db("SELECT results, is_finished FROM Results WHERE "
                           "result_id = ?;",
                         [result_id], one=True)

        if r_res is None:
            response['error'] = True
            response['errmsg'] = "No results with that id."
            return response

        status = r_res['is_finished']
        # if status is not finished
        if status == 0:
            response['status'] = "not done"
        elif status == 1:
            # return the results JSON
            response['results'] = json.loads(r_res['results'])
            response['status'] = "done"
        elif status == 2:
            response['status'] = "error during testing"

        return response

    # methods for interfacing with AMLET
    def receiveModel(self, model, model_id, error=False):
        with app.app_context():
            app.logger.info("Model %s received", model_id)

            # check if error
            if error:
                query_db("UPDATE Models SET "
                         "is_finished = 2 WHERE model_id = ?;",
                        [model_id])

            # pickle the model
            p_model = pickle.dumps(model, pickle.HIGHEST_PROTOCOL)

            # update row with the model_id to add the model, is_finished
            query_db("UPDATE Models SET model = ?, is_finished = 1 "
                    "WHERE model_id = ?;",
                    [sqlite3.Binary(p_model), model_id])

    def receiveTest(self, result, result_id, error=False):
        with app.app_context():
            result = json.dumps(result)
            app.logger.info("Test results %s received", result_id)
            app.logger.debug("Test results %s are: %s", result_id, result)

            # check if error
            if error:
                query_db("UPDATE Results SET "
                         "is_finished = 2 WHERE result_id = ?;",
                        [result_id])

            # update row with the result_id to add the results, is_finished
            query_db("UPDATE Results SET results = ?, is_finished = 1 "
                    "WHERE result_id = ?;",
                    [result, result_id])