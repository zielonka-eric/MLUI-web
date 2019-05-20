# MLUI-web

## Required Python Libraries
- flask
- sqlite3
- amlet
- requests ( not necessary for the server, it's used for the example script )

## Setup and Process
 1. If this is the first time running the script, run `create_db.py`. This will create the sqlite3 database to hold the models and test results.
 2. Run `ml-web.py` to start the server.
 3. With the server running, make a request to `/api/help` to see a list of endpoints and parameters. Alternatively, see the included `help.txt` file for the same list of endpoints.
 4. The server is ready to receive requests. See `example/example_script.py` for an example of how send API requests to the server, using the Python Requests library. Of course, you can use any library or tool that can send HTTP requests to use this API.