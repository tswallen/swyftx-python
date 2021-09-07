import logging
import json
import requests

logger = logging.getLogger(__name__)

postman_collection_file = open('Swyftx.postman_collection.json')
postman_collection = json.load(postman_collection_file)

class Swyftx:
    def __init__(self, config):
        self.config = config

def function_builder(request):
    def call_api(self, **kwargs):
        url = request['url']['raw'].replace('{{base_route}}', self.config['base_route'])
        for key, value in { key : value for key, value in kwargs.items() }.items():
            if key in url:
                url = url.replace(f':{key}', str(value))
                del kwargs[key]
        request_function = getattr(requests, request['method'].lower())
        try:
            response = request_function(url, **kwargs)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            logger.error(error)
        return response
    return call_api

def process_item(item):
    if 'request' in item:
        function_name = item['name'].replace(' ', '_').lower()
        new_function = function_builder(item['request'])
        setattr(Swyftx, function_name, new_function)
    if 'item' in item:
        for item in item['item']:
            process_item(item)

for item in postman_collection['item']:
    process_item(item)