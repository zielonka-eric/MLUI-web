from amlet import amlet_engine
import string
import random
import io
from app import query_db

class data_model:
    # NOTE: Most of the methods' parameters need to change

    def __init__(self):
        self.engine = amlet_engine.AMLET_Engine(self)

    def help(self):
        # get dict of algorithms from amlet
        return {}

    def model_create(self, algorithm, data_file, data_id, params):
        while True:
            # create new random model_id
            model_id = ''.join(
                random.choices(string.ascii_letters + string.digits, k=10))

            # check for id collision in database
            c_res = query_db("SELECT COUNT() FROM Models WHERE model_id = ?;",
                             [model_id], one=True)

            if c_res[0] == 0:
                break

        # set up return value
        response = dict(error=False, errmsg="")

        # if no data_file, and data_id is given, get data from the database      # TODO: change to get multiple data files
        data = None
        if data_file is not None:
            data = data_file
        elif data_id is not None:
            d_res = query_db("SELECT data FROM Data WHERE data_id = ?;",
                           [data_id], one=True)
            data = io.BytesIO(d_res[0]) if d_res else None
        if data is None:
            response['error'] = True
            response['errmsg'] = "No data provided or invalid data_id"
            return response

        # call amlet_engine's createModel()
        self.engine.createModel(algorithm, params, data, model_id)

        # insert row into database for the new model
        query_db("INSERT INTO Models (model_id, is_finished) VALUES (?, ?);",
                 [model_id, 0])

        #return model_id or any error message
        if response['error'] == False:
            response['model_id'] = model_id
        return response

    def model_status(self, model_id):
        # check model table in database for status of model_id
        # if status is not finished, check amlet
        # return status
        return "not done"

    def model_download(self, model_id):
        # check model table in database for status of model_id
        # if status is not finished, error
        # return the model bytestream from the database
        return b'hello world\n'

    def model_test(self, model_id, data_file, data_id, params):
        while True:
            # create new random result_id
            result_id = ''.join(
                random.choices(string.ascii_letters + string.digits, k=10))

            # check for id collision in database
            c_res = query_db("SELECT COUNT() FROM Results WHERE result_id = ?;",
                             [result_id], one=True)

            if c_res[0] == 0:
                break

        # set up return value
        response = dict(error=False, errmsg="")

        # get the model from the database
        m_res = query_db("SELECT model FROM Models WHERE model_id = ?;",
                         [model_id], one=True)
        model = str(m_res[0]) if m_res else None

        # if no data_file, and data_id is given, get data from the database      # TODO: change to get multiple data files
        data = None
        if data_file is not None:
            data = data_file
        elif data_id is not None:
            d_res = query_db("SELECT data FROM Data WHERE data_id = ?;",
                             [data_id], one=True)
            data = io.BytesIO(d_res[0]) if d_res else None
        if data is None:
            response['error'] = True
            response['errmsg'] = "No data provided or invalid data_id"
            return response

        # send model and data to amlet
        self.engine.testModel(model, params, data, model_id)

        # insert row into database for the new testing result
        query_db("INSERT INTO Results (result_id, model_id, is_finished) "
                 "VALUES (?, ?, ?);",
                 [result_id, model_id, 0])

        #return result_id or any error message
        if response['error'] == False:
            response['result_id'] = result_id
        return response

    def model_results(self, model_id):
        # check results table, get all rows with model_id
        # return the list of results JSONs
        return []

    def model_remove(self, model_id):
        # delete model with model_id from database
        # delete results with this model_id from database
        # return confirmation?
        return True

    def get_results(self, result_id):
        # get results JSON from database and return it
        return {}

    def upload_data(self, data):
        # create new random data_id
        data_id = ''.join(
            random.choices(string.ascii_letters + string.digits, k=10))

        # TODO: check for id collision in database

        response = dict(error=False,
                    errmsg="",
                    data_id=data_id)

        # TODO: put data into database data table

        # return data_id
        return response

    def data_get(self, data_id):
        # get results JSON from database and return it
        return b"data file\n"

    def data_remove(self, data_id):
        # delete model with model_id from database
        # return confirmation?
        return True
