import json
import logging
from gremlin_python.driver import client, serializer
import azure.functions as func
import datetime
import requests_async as requests



async def main(event: func.EventGridEvent):
    result_json = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    })

    logging.info(event.get_json())
    data = event.get_json()
    input_id = data.get('input_id')
    value = data.get('value')

    dbclient = client.Client('wss://peridymegraph.gremlin.cosmos.azure.com:443/','g', 
    message_serializer=serializer.GraphSONSerializersV2d0(),
    username="/dbs/db/colls/Graph1", 
    password="")
    
    query = f"g.V('{input_id}').out('function').values('value')"
    callback = dbclient.submitAsync(query)
    function_url = callback.result().all().result()[0]
    logging.info(function_url)
    data = {"value": value}
    logging.info (data)
    '''with requests.Session() as s:
        response = s.post(function_url, timeout=5, json = data)
        logging.info(response.text)
        response_json = response.json()
        output = response_json["output"]
        logging.info(output)
        s.close()
    '''
    
    async with requests.Session() as session:
        response = await session.post(function_url, timeout=5, json = data)
        logging.info(response.text)
        response_json = response.json()
        output = response_json["output"]
        logging.info(output)
        session.close()
    
    query2 = f"g.V('{input_id}').out('function').out('output').property('value', {output})"
    logging.info (query2)
    dbclient.submitAsync(query2)
    dbclient.close()


    '''
    try:
        callback = dbclient.submitAsync(query)
        if callback.result() is not None:
            function_url = callback.result().all().result()[0]
            logging.info(function_url)
        else: logging.info ("callback.result() is None!")
    except Exception as e:
            logging.info ('There was an exception with query1: {0}'.format(e))
    
    try:
        if function_url is not None:
            req_data = {"value": value}
            logging.info (data)
            with requests.Session() as s:
                response = s.post(function_url, timeout=1, json = req_data)
                logging.info(response.text)
                response_json = response.json()
                output = response_json["output"]
                logging.info(output)
                s.close()
        else: logging.info ("function_url is None!")
    except Exception as e:
            logging.info  ('There was an exception with requests.post: {0}'.format(e))

    try:
        if (function_url is not None) and (output is not None):
            query2 = f"g.V('{input_id}').out('function').out('output').property('value', {output})"
            logging.info (query2)
            dbclient.submitAsync(query2)
        else: logging.info ("function_url or output is missing!")
    except Exception as e:
            logging.info ('There was an exception with query2: {0}'.format(e))
    
    dbclient.close()


    '''


