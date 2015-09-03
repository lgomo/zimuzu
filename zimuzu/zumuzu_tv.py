#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
import os
from os import path
import sys

import click
import requests


class Zimuzu(object):
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; \
             Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0'})

    @staticmethod
    def get_config():
        conf_path = path.join(sys.path[0], 'zimuzu_config.json')
        if not os.path.exists(conf_path):
            sys.exit('Please check you config at: {0}.'.format(conf_path))

        with open(conf_path) as f:
            config = json.load(f)

        if config.keys() != ['account', 'password', 'log_directory']:
            sys.exit("The config file should contain 'account', 'password' "
                     "and 'log_directory' settings.")
        return config['account'], config['password'], config['log_directory']

    def login(self):
        account, password, log_directory = self.get_config()
        post_data = {
            'account': account,
            'password': password,
            'remember': 0,
            'url_back': 'http://www.zimuzu.tv/user/sign'
        }
        login = self.session.post('http://www.zimuzu.tv/User/Login/ajaxLogin',
                                  data=post_data)
        try:
            if login.json()['status'] == 1:
                click.echo('Login success!')
            else:
                click.echo(login.json()['info'])
        except ValueError:
            sys.exit("Login failed.")

    def do_sign(self):
        # We need to visit the sign page first, or you'll get 4002 status.
        self.session.get('http://www.zimuzu.tv/user/sign')

        do_sign = self.session.get('http://www.zimuzu.tv/user/sign/dosign')
        try:
            if do_sign.json()['status'] == 1:
                click.echo("Success! You've keep signing in {0} days".format(
                    do_sign.json()['data']))
            # Check whether we've signed before.
            elif do_sign.json()['status'] == 4001:
                click.echo("You've signed today.")
            else:
                click.echo(do_sign.json()['info'])
        except ValueError:
            sys.exit("Do sign failed.")