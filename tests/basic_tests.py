#!/usr/bin/env python3


import requests
import json
import pickle
import random
import argparse
from TestUser import TestUser
from TestAdmin import TestAdmin


parser = argparse.ArgumentParser()
parser.add_argument('--number-of-users', type=int, default=8)
parser.add_argument('--number-of-user-tests', type=int, default=4)
parser.add_argument('--use-server', action='store_true')
parser.add_argument('--seed-only', action='store_true')
args = parser.parse_args()


if args.use_server:
    base_url = 'http://fallriskdb-vm.main.ad.rit.edu:5000'
else:
    base_url = 'http://0.0.0.0:5000'


def main():
    # Number of users to be created.
    n = args.number_of_users
    # Number of users who take the tests and survey.
    k = args.number_of_user_tests

    # Access admin account.
    if not args.seed_only:
        admin = TestAdmin(base_url)
        admin.get_token()

    # Create user profiles.
    users = [ TestUser(base_url) for i in range(n) ]
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

    if not args.seed_only:
        print('Press any key to continue ...', end='')
        input()

        data = admin.get_data()

        if data is not None:
            print('Found {} users who need to be evaluated.'.format(len(data)))

            cmt = admin.post_results(data)

            print('Was able to update {} out of {} users fall risk.'.format(cmt['results_updated'], len(data)))

            user = users[idxs[random.randint(0, k - 1)]]

            sent = user.tests

            test_passed = False
            for i in range(len(data)):
                if data[i]['email'] == user.email:
                    received = pickle.loads(base64.b64decode(data[i]['tests'].encode('utf-8')))

                    print('Sent tests are equal to the received tests? {}'.format('PASS' if sent == received else 'FAIL'))

                    print('Printing the rest of the data ...')
                    print()

                    data[0].pop('tests')

                    print(json.dumps(data[0], indent=2))

                    test_passed = True
                    break
            
            if not test_passed:
                print('User was not found in the data.')


if __name__ == '__main__':
    main()
