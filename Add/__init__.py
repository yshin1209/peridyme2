# Add (two numbers)
# 2021 Yong-Jun Shin

# Ctrl-Shift-P --> Terminal: Create New Integrated Terminal
# gremlinpython==3.5.0 --> requirments.txt 
# gremelinpython supports python 3.4 or higher
# pip install --target ".\.venv\Lib\site-packages" -r requirements.txt --upgrade

import logging
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_data = req.get_json()
        if req_data is not None:
            input_value = req_data.get('value') #requesting vertex value
            output = input_value + 10    
            response = {"output": output}
            response_json = json.dumps(response)
            logging.info (response_json)
            return response_json
        else: return "req_data is None!"
    except Exception as e:
            logging.info ('There was an exception with Add: {0}'.format(e))
