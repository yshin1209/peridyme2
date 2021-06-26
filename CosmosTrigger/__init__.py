# Cosmos DB Trigger
# 2021 Yong-Jun Shin

# Ctrl-Shift-P --> Terminal: Create New Integrated Terminal
# gremlinpython==3.5.0 --> requirments.txt 
# gremelinpython supports python 3.4 or higher
# pip install --target ".\.venv\Lib\site-packages" -r requirements.txt --upgrade

import logging
import datetime
import azure.functions as func

def main(documents: func.DocumentList, outputEvent: func.Out[func.EventGridOutputEvent]):
    if documents:
        logging.info('id: %s', documents[0]['id'])
        logging.info('value: %s', documents[0]['value'][0]['_value'])

    input_id = documents[0]['id']
    value = documents[0]['value'][0]['_value']

    outputEvent.set(
        func.EventGridOutputEvent(
            id="test-id",
            data={'input_id': input_id, 'value': value},
            subject="CosmosDB Trigger",
            event_type="test-event-1",
            event_time= datetime.datetime.utcnow(),
            data_version="1.0"))

    logging.info ("event sent")
    