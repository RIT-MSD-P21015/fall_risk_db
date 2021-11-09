import json
import requests
import pickle
import base64
import uuid
import random


class TestUser():
    def __init__(self, base_url, firstname=None, lastname=None, email=None, password=None):
        self.firstname = uuid.uuid4().hex if firstname is None else firstname
        self.lastname = uuid.uuid4().hex if lastname is None else lastname
        self.email = '{}@rit.edu'.format(uuid.uuid4().hex) if email is None else email
        self.password = uuid.uuid4().hex if password is None else password
        self.survey = None
        self.tests = None
        self.token = None
        self.base_url = base_url


    def __repr__(self):
        return '{}'.format(self.email)


    def get_data(self):
        header = {'Authorization' : 'Bearer {}'.format(self.token)}
        params = {'tests' : 0, 'survey' : 1}
        r = requests.get('{}/{}'.format(self.base_url, 'api/user'), params=params, headers=header)
        print(json.loads(r.text))


    def delete_data(self):
        header = {'Authorization' : 'Bearer {}'.format(self.token)}
        r = requests.delete('{}/{}'.format(self.base_url, 'api/user'), headers=header)


    def new_survey(self):
        self.survey = {
            'age' : random.randint(1, 100),
            'height' : random.randint(48, 84),
            'weight' : random.randint(50, 300),
            'gender' : random.sample(['Male', 'Female', 'Other'], 1)[0]
        }


    def new_tests(self, m=3000, n=324):
        self.tests = [[random.uniform(0, 100) for i in range(n)] for i in range(m)]


    def create_profile(self):
        user = {
            'firstname' : self.firstname,
            'lastname' : self.lastname,
            'password' : self.password,
            'email' : self.email
        }

        r = requests.post('{}/{}'.format(self.base_url, 'api/user'), json=user)

        error = r.status_code != 201

        print('Email {} - Create user profile - {}'.format(self, 'PASS' if not error else 'FAIL'))


    def get_token(self):
        r = requests.post('{}/{}'.format(self.base_url, 'api/tokens'), auth=(self.email, self.password))

        error = r.status_code != 200

        print('Email {} - Get access token - {}'.format(self, 'PASS' if not error else 'FAIL'))

        if not error:
            self.token = json.loads(r.text)['token']


    def update_profile(self, email=None):
        data = {}

        if self.tests is not None:
            data['tests'] = base64.b64encode(pickle.dumps(self.tests)).decode('utf-8')
        if self.survey is not None:
            data['survey'] = json.dumps(self.survey)

        header = {'Authorization' : 'Bearer {}'.format(self.token)}

        r = requests.put('{}/{}'.format(self.base_url, 'api/user'), json=data, headers=header)

        error = r.status_code != 200

        print('Email {} - Update user profile - {}'.format(self, 'PASS' if not error else 'FAIL'))

    def reset_password_request(self):
        r = requests.get('{}/{}/{}'.format(self.base_url, 'api/reset_password_request', self.email))
        print(r.text)
