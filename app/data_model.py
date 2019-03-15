from amlet import amlet_engine
import string
import random
# import database library

class data_model:
    # NOTE: Most of the methods' parameters need to change

    def __init__(self):
        self.engine = amlet_engine.AMLET_Engine(self)
        # set up database
        pass

    def help(self):
        # get dict of algorithms from amlet
        return {}

    def model_create(self, algorithm, data_file, data_id, params):
        # create new random model_id
        model_id = ''.join(
            random.choices(string.ascii_letters + string.digits, k=10))

        # TODO: check for id collision in database

        response = dict(error=False,
                    errmsg="",
                    model_id=model_id)

        # if no data_file, and data_id is given, get data from the database
        if data_file is not None:
            data = data_file
        elif data_id is not None:
            data = data_id #TODO: get data from database
        else:
            response['error'] = True
            response['errmsg'] = "No data provided"
            return response

        # call amlet_engine's createModel()
        self.engine.createModel(algorithm, params, data, model_id)

        #return model_id and any error message
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
        # create new random result_id
        result_id = ''.join(
            random.choices(string.ascii_letters + string.digits, k=10))

        # TODO: check for id collision in database

        response = dict(error=False,
                    errmsg="",
                    result_id=result_id)

        # TODO: get the model from the database
        model = model_id

        # if data_id is given, get data from the database
        if data_file is not None:
            data = data_file
        elif data_id is not None:
            data = data_id #TODO: get data from database
        else:
            response['error'] = True
            response['errmsg'] = "No data provided"
            return response

        # send model and data to amlet
        self.engine.testModel(model, params, data, model_id)

        # return result_id
        return response

    def model_results(self, model_id):
        # check results table, get all rows with model_id
        # return the list of results JSONs
        return []

    def model_remove(self, model_id):
        # delete model with model_id from database
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
