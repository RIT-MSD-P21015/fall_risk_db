#!/usr/bin/env python3


from TestUser import TestUser
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--use-server', action='store_true')
args = parser.parse_args()


if args.use_server:
    base_url = 'http://fallriskdb-vm.main.ad.rit.edu:5000'
else:
    base_url = 'http://0.0.0.0:5000'


def main():
    user = TestUser(base_url, 'Matt', 'Krol', 'mkrolbass@gmail.com', 'secret')
    user.create_profile()
    user.reset_password_request()


if __name__ == '__main__':
    main()
