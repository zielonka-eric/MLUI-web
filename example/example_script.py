import requests
import time
import datetime
import json

output_filename = 'model_output_file.pickle'

data = {
    #'alg' : 'support_vector_classifier',
    'alg' : 'perceptron',
    'train' : ['Route', 'Heading', 'TimeInFlight', 'Speed',
               'Altitude', 'Lat', 'Long'],
    'target' : 'Anom'
}
files = {'data': open('testdata.csv', 'rb')}
#files = {'data': [open('testdata.csv', 'rb'), open('testdata2.csv', 'rb')]}


# send the POST request to create the model
url = 'http://127.0.0.1:5000/api/model'
# non-JSON formatted : 
r = requests.post(url, data=data, files=files)
# JSON formatted :
#r = requests.post(url, data={'params': json.dumps(data)}, files=files)

response = r.json()
if response['error'] == False:
    model_id = response['model_id']
    print('model_id : {}'.format(model_id))
else:
    print(response['errmsg'])
    exit()

done = False

while not done:
    # send the GET request to get the status of the model
    url = 'http://127.0.0.1:5000/api/model/' + model_id
    r = requests.get(url)
    
    response = r.json()
    if response['error'] == True:
        print(response['errmsg'])
        exit()

    print('[  {}  ] status: {}'.format(
        datetime.datetime.now(), response['status']))
    if response['status'] != 'done':
        time.sleep(60 * 5) # wait for 5 minutes before trying again
    else:
        done = True

# send the POST request to download the model
url = 'http://127.0.0.1:5000/api/model/' + model_id + '/download'
r = requests.get(url)

# write the model to an output file
with open(output_filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size=128):
        f.write(chunk)

print('[  {}  ] model downloaded and saved in {}'.format(
        datetime.datetime.now(), output_filename))