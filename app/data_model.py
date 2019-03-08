from amlet import amlet_engine
# import database library

class data_model:
    # NOTE: Most of the methods' parameters need to change

    def __init__(self):
        engine = amlet_engine.AMLET_Engine(self)
        # set up database
        pass

    def help(self):
        # get dict of algorithms from amlet
        return {}

    def model_create(self, *args):
        # create new random model_id
        # check for id collision in database
        # if data_id is given, get data from the database
        # call amlet_engine's createModel()
        # if no error returned from amlet, return model_id
        return "abc5"

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

    def model_test(self, model_id):
        # create new random result_id
        # check for id collision in database
        # get the model from the database
        # if data_id is given, get data from the database
        # send model and data to amlet
        # return result_id
        return "xyz24"

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
        # check for id collision in database
        # put data into database data table
        # return data_id
        return "98765a"

    def data_get(self, data_id):
        # get results JSON from database and return it
        return b"data file\n"

    def data_remove(self, data_id):
        # delete model with model_id from database
        # return confirmation?
        return True
