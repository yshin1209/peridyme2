import logging
import azure.functions as func
from azure.core.credentials import AzureKeyCredential
from azure.eventgrid import EventGridPublisherClient, EventGridEvent

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    endpoint = "https://eventtopic.westus-1.eventgrid.azure.net/api/events"
    credential = AzureKeyCredential("")
    client = EventGridPublisherClient(endpoint, credential)
    
    event = EventGridEvent(
        data={"name": "Yong Jun Shin"},
        subject="Student List",
        event_type="Azure.Sdk.Demo",
        data_version="2.0"
        )
    client.send(event)

    return func.HttpResponse("OK")

