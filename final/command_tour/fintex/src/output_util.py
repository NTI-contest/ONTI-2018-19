from json import dumps

def print_error(message):
    print(message)
    quit(0)

def print_json(obj):
    print(dumps(obj, indent=4))

def handle_error(response):
    if type(response) == dict and response.get('error'):
        print_error(response['error'])
    return response
