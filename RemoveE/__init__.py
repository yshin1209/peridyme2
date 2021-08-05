# RemoveE
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
    outV = req_body.get('outV') # out vertex
    inV = req_body.get('inV') # in vertex

    dbclient = client.Client('wss://peridymegraph.gremlin.cosmos.azure.com:443/','g', 
    message_serializer=serializer.GraphSONSerializersV2d0(),
    username="/dbs/db/colls/Graph1", 
    password="")
    query = f"g.V('{outV}').outE().where(otherV().hasId('{inV}')).drop()"
    callback = dbclient.submitAsync(query)
    callback_result = json.dumps(callback.result().all().result())
    dbclient.close()
    return func.HttpResponse(body = callback_result)
