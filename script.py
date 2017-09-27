#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
import requests
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--tweet', help='Publish a tweet', required=True)
args = parser.parse_args()


class Request:
    @staticmethod
    def post(url, session, data):
        headers = {'content-type': 'application/x-www-form-urlencoded', 'user-agent': 'Mozilla/5.0'}
        return session.post(url, data=data, headers=headers).content

class User:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def auth(self):
        print 'Authenticating...\n'
        with requests.Session() as self.session:
            response = self.session.get('https://mobile.twitter.com/session/new')
            
            html = BeautifulSoup(response.content, "html.parser")
            self.tokenCsrf = html.find('input', {'name': 'authenticity_token'}).get('value')

            content = Request.post(
                'https://mobile.twitter.com/sessions',
                self.session,
                {'authenticity_token': self.tokenCsrf, 'session[username_or_email]':self.username, 'session[password]': self.password}
            )
            
            html = BeautifulSoup(content, "html.parser")
            authenticated = html.find('td',{'class' : 'me'})

            if authenticated == None:
                return False
            
            print '[OK] Succesfully authenticated ! \n'
            return True

    def tweet(self,tweet):
        print 'Publishing Tweet ...\n'

        Request.post(
            'https://mobile.twitter.com/compose/tweet',
            self.session,
            {'authenticity_token': self.tokenCsrf, 'tweet[text]': tweet}
        )

        print '[OK] Tweet Published ! \n'


def main():
    print '[Twitter CLI] : Welcome !'
    user = User('username','password')
    connected = user.auth()

    if connected == False:
        sys.exit('[FAIL] Check your twitter credentials \n')

    user.tweet(args.tweet)

if __name__ == '__main__':
    main()