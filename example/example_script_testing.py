# run with `python -u` for unbuffered output, to print the
# status messages immediately

import requests
import time
import datetime
import json



##### change these variables

model_id = 'abcde12345'             # replace with actual model id
output_filename = 'results.json'

arguments = {
    'tests' : ['f1', 'accuracy'],
    'data' : 'example/testdata.csv' # should use absolute path for consistency
}

time_interval = 60 * 5 # wait for 5 minutes before checking status again

##### ####



# send the POST request to test the model
url = 'http://127.0.0.1:5000/api/model/{}/test'.format(model_id)
r = requests.post(url, json=arguments)

response = r.json()
if response['error'] == False:
    result_id = response['result_id']
    print('result_id : {}'.format(result_id))
else:
    print(response['errmsg'])
    exit()

done = False
while not done:
    # send the GET request to get the status and results
    url = 'http://127.0.0.1:5000/api/results/{}'.format(result_id)
    r = requests.get(url)
    
    response = r.json()
    if response['error'] == True:
        print(response['errmsg'])
        exit()

    print('[  {}  ] status: {}'.format(
        datetime.datetime.now(), response['status']))
    if response['status'] != 'done':
        time.sleep(time_interval)
    else:
        done = True
        results = json.dumps(response['results'])
        print('Test results for model {} :'.format(model_id))
        print(results)

# write the results to an output file
with open(output_filename, 'w') as f:
        f.write(results)

print('[  {}  ] results downloaded and saved in {}'.format(
        datetime.datetime.now(), output_filename))