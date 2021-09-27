#!/usr/bin/env python3

import requests
import json
import pickle
import base64
import uuid
import random


base_url = 'http://0.0.0.0:5000'


class TestUser():
    def __init__(self, email=None, password=None):
        self.email = '{}@rit.edu'.format(uuid.uuid4().hex) if email is None else email
        self.password = uuid.uuid4().hex if password is None else password
        self.survey = None
        self.tests = None
        self.token = None


    def __repr__(self):
        return '{}'.format(self.email)


    def new_survey(self):
        self.survey = {
            'age' : random.randint(1, 100),
            'height' : random.randint(48, 84),
            'weight' : random.randint(50, 300),
            'gender' : random.sample(['Male', 'Female', 'Other'], 1)[0]
        }

    def new_tests(self, m=10000, n=9):
        self.tests = [[random.uniform(0, 100) for i in range(n)] for i in range(m)]


    def create_profile(self):
        user = {
            'password' : self.password,
            'email' : self.email
        }

        r = requests.post('{}/{}'.format(base_url, 'api/user'), json=user)

        error = r.status_code != 201

        print('Email {} - Create user profile - {}'.format(self, 'PASS' if not error else 'FAIL'))


    def get_token(self):
        r = requests.post('{}/{}'.format(base_url, 'api/tokens'), auth=(self.email, self.password))

        error = r.status_code != 200

        print('Email {} - Get access token - {}'.format(self, 'PASS' if not error else 'FAIL'))

        if not error:
            self.token = json.loads(r.text)['token']


    def update_profile(self, email=None):
        data = {}

        if self.tests is not None:
            # obj = pickle.loads(base64.b64decode(d['tests'].encode('utf-8')))
            data['tests'] = base64.b64encode(pickle.dumps(self.tests)).decode('utf-8')
        if self.survey is not None:
            data['survey'] = json.dumps(self.survey)

        header = {'Authorization' : 'Bearer {}'.format(self.token)}

        r = requests.put('{}/{}'.format(base_url, 'api/user'), json=data, headers=header)

        error = r.status_code != 200

        print('Email {} - Update user profile - {}'.format(self, 'PASS' if not error else 'FAIL'))

class TestAdmin(TestUser):
    def __init__(self, email='admin@rit.edu', password='secret'):
        super().__init__(email=email, password=password)


    def get_data(self):
        header = {'Authorization' : 'Bearer {}'.format(self.token)}

        r = requests.get('{}/{}'.format(base_url, 'api/admin/data'), headers=header)

        if r.status_code == 200:
            data = json.loads(r.text)
            return data
        else:
            return None


    def post_results(self, data):
        results = []

        for i in range(len(data)):
            fall_risk = random.uniform(0, 1)

            result = {
                'id' : data[i]['id'],
                'result' : {
                    'fall_risk' : fall_risk,
                    'comments' : 'See your doctor!' if fall_risk > 0.3 else 'Looks good!'
                }
            }

            results.append(result)

        header = {'Authorization' : 'Bearer {}'.format(self.token)}

        r = requests.put('{}/{}'.format(base_url, 'api/admin/results'), json=results, headers=header)

        if r.status_code == 200:
            data = json.loads(r.text)
            return data
        else:
            return None


def main():
    # Number of users to be created.
    n = 10
    # Number of users who take the tests and survey.
    k = 5

    # Access admin account.
    admin = TestAdmin()
    admin.get_token()

    # Create user profiles.
    users = [ TestUser() for i in range(n) ]
    for user in users:
        user.create_profile()

    print('Press any key to continue ...', end='')
    input()

    idxs = random.sample(range(n), k)

    for idx in idxs:
        users[idx].get_token()
        users[idx].new_survey()
        users[idx].new_tests()
        users[idx].update_profile()

    print('Press any key to continue ...', end='')
    input()

    data = admin.get_data()

    print('Found {} users who need to be evaluated.'.format(len(data)))

    cmt = admin.post_results(data)

    print('Was able to update {} out of {} users fall risk.'.format(cmt['results_updated'], len(data)))


if __name__ == '__main__':
    main()
