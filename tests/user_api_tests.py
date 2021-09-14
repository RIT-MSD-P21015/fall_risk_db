#!/usr/bin/env python3

import requests
import json

base_url = 'http://127.0.0.1:5000'

def url_map(target):
    return '{}/{}'.format(base_url, target)

def print_json(text):
    print(json.dumps(json.loads(text), indent=2))

def auth_header(token):
    return {'Authorization' : 'Bearer {}'.format(token)}

def main():
    user = {
        'username' : 'abc1234',
        'password' : 'secret',
        'email' : 'abc1234@rit.edu'
    }

    print('**** Creating a new user profile ****')
    r = requests.post(url_map('api/user'), json=user)
    print_json(r.text)

    print('**** Getting an access token ****')
    r = requests.post(url_map('api/tokens'), auth=(user['username'], user['password']))
    print_json(r.text)
    token = json.loads(r.text)['token']

    print('**** Getting back user data ****')
    r = requests.get(url_map('api/user'), headers=auth_header(token))
    print_json(r.text)

if __name__ == '__main__':
    main()
