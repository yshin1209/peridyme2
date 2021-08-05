  
# RemoveVProperty
# 2021 Yong-Jun Shin

# Ctrl-Shift-P --> Terminal: Create New Integrated Terminal
# gremlinpython==3.5.0 --> requirments.txt 
# gremelinpython supports python 3.4 or higher
# pip install --target ".\.venv\Lib\site-packages" -r requirements.txt --upgrade

import logging
from gremlin_python.driver import client, serializer
import azure.functions as func
import json 

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_body = req.get_json()
    id = req_body.get('id') # vertex id
    key = req_body.get('key') # vertex key
    dbclient = client.Client('wss://peridymegraph.gremlin.cosmos.azure.com:443/','g', 
    message_serializer=serializer.GraphSONSerializersV2d0(),
    username="/dbs/db/colls/Graph1", 
    password="")
    query = f"g.V('{id}').properties('{key}').drop()"
    callback = dbclient.submitAsync(query)
    callback_result = json.dumps(callback.result().all().result())
    dbclient.close()
    return func.HttpResponse(body = callback_result)
