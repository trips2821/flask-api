import json
import pprint

import requests
from termcolor import colored


pp = pprint.PrettyPrinter(indent=4).pprint

username = "user1234"
password = "pass1"
host = "0.0.0.0"
port = str(8000)

host_port = host + ":" + port
base_addr = 'http://' + host_port + '/api'

def print_body(text):
    print(colored('|  ', 'red', attrs=['bold']), end='')
    print(text)


def test_api(message, req_obj, req_method, req_url, req_json, exp_json, exp_code):
    print('Testing: ' + message + '... ', end='')

    method = getattr(req_obj, req_method)
    response = method(url=req_url, json=req_json)
    if response.status_code != exp_code:
        print('\n')
        print(colored('----------------------FAIL----------------------', 'red', attrs=['reverse', 'bold']))
        print_body('METHOD: {}'.format(req_method))
        print_body('URL: {}'.format(req_url))
        print_body('SENT: {}'.format(req_json))

        print_body(colored(req_url + " returned an invalid code of " + str(response.status_code) + " instead of " + str(exp_code), 'red'))

        print_body('---')
        print_body('RSPC: {}'.format(response.status_code))
        print_body('RESP: {}'.format(response.text).replace('\n',''))

        print_body('---')
        print_body('EXPC: {}'.format(exp_code))
        print_body('EXPR: {}'.format(exp_json))
        print(colored('----------------------END-----------------------', 'red', attrs=['reverse', 'bold']))
        print('\n\n')

    else:
        print(colored('OK', 'green'))


    return response


test_api('health check', requests, 'get', base_addr, {}, {}, 200)

test_api('not logged in', requests, 'get', base_addr + '/test', {}, {}, 401)

test_api('register new user', requests, 'post', base_addr + '/user', {"username":username,"password":password}, {}, 201)

test_api('register an already registered user', requests, 'post', base_addr + '/user', {"username":username,"password":password}, {}, 400)

#get http basic auth session
session = requests.Session()
session.auth = (username, password)

response = test_api('get token', session, 'get', 'http://' + host_port + '/api/login', {}, {}, 200)
response = json.loads(response.text)

session.auth = (response['token'],'')

test_api('logged in', session, 'get', base_addr + '/test', {}, {}, 200)
