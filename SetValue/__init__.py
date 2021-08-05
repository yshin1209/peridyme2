  
# SetValue
# 2021 Yong-Jun Shin

# Ctrl-Shift-P --> Terminal: Create New Integrated Terminal
# .venv\scripts\activate --> activate the virtual environment in the current folder
# gremlinpython==3.5.0 --> requirments.txt 
# gremelinpython supports python 3.4 or higher
# python -m pip install -r requirements.txt

import logging
from gremlin_python.driver import client, serializer
import azure.functions as func
import json 

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_body = req.get_json()
    input_id = req_body.get('id')   # vertex id
    # key = req_body.get('key') # vertex property key
    value = req_body.get('value') # vertex perperty value

    dbclient = client.Client('wss://peridymegraph.gremlin.cosmos.azure.com:443/','g', 
    message_serializer=serializer.GraphSONSerializersV2d0(),
    username="/dbs/db/colls/Graph1", 
    password="")

    if type(value) == str:
        query = f"g.V('{input_id}').property('value', '{value}')"
    elif type(value) == bool:
        if value == True:
            value = 'true'
        elif value == False:
            value = 'false'
        query = f"g.V('{input_id}').property('value', {value})"
    else: query = f"g.V('{input_id}').property('value', {value})"
    
    callback = dbclient.submitAsync(query)
    callback_result = callback.result().all().result()
    response_json = json.dumps(callback_result)
    logging.info(response_json)
    dbclient.close()
    return func.HttpResponse(body = response_json)


