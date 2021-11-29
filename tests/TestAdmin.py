import requests
import json
import random
from TestUser import TestUser


class TestAdmin(TestUser):
    def __init__(self, base_url, firstname='admin', lastname='admin', email='admin@rit.edu', password='secret'):
        super().__init__(base_url, firstname=firstname, lastname=lastname, email=email, password=password)


    def get_data(self):
        header = {'Authorization' : 'Bearer {}'.format(self.token)}

        r = requests.get('{}/{}'.format(self.base_url, 'api/admin/data'), headers=header)

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

        r = requests.put('{}/{}'.format(self.base_url, 'api/admin/results'), json=results, headers=header)

        if r.status_code == 200:
            data = json.loads(r.text)
            return data
        else:
            return None
