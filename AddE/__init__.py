  # AddE
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
    edgeLabel = req_body.get('edgeLabel') # edge label
    inV = req_body.get('inV') # edge label

    dbclient = client.Client('wss://peridymegraph.gremlin.cosmos.azure.com:443/','g', 
    message_serializer=serializer.GraphSONSerializersV2d0(),
    username="/dbs/db/colls/Graph1", 
    password="47ONfPHcunYSxeR8elFB4JpKED2Rei1mFANxpMyfPDOU8tX2ZIE1gNYJ9Pl7NY2DRZ0IouKwuxyy8nqPOqXrQg==")
    query = f"g.V('{outV}').addE('{edgeLabel}').to(g.V('{inV}'))"
    callback = dbclient.submitAsync(query)
    callback_result = json.dumps(callback.result().all().result())
    dbclient.close()

    if callback.result() is not None:
            logging.info(f"\tQuery result:\n\t{callback_result}")
    else:
            logging.info(f"Something went wrong with this query: {query}")

    return func.HttpResponse(body = callback_result)
