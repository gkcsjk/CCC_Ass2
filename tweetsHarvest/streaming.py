import getopt
import json
import sys

import couchdb
import tweepy

import keys

USERNAME = 'ccc'
PASSWORD = 'cloud'

locations = {
    "melbourne": [144.5436, -38.4287, 145.4239, -37.5401],
    "sydney": [150.5598, -34.0974, 151.3563, -33.5601],
    "brisbane": [152.7879, -27.7495, 153.3482, -27.1450],
    "adelaide": [138.4422, -35.1555, 138.7883, -34.6419],
    "perth": [115.6965, -32.3350, 116.0906, -31.6922],
    "canberra": [148.9917, -35.4675, 149.2773, -35.1436]
}

server = couchdb.Server('http://ccc:cloud@localhost:5984/')


class MyStreamListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        data = json.loads(raw_data)
        print data['id']
        doc = [data]
        db.update(doc)



try:
    opts, args = getopt.getopt(sys.argv[1:], 'c:nok:',['city=', 'key='])
except getopt.GetoptError:
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-c', '--city'):
        city = arg
    elif opt == '-n':
        create_new = True
    elif opt == '-o':
        create_new = False
    elif opt in ('-k', '--key'):
        key_owner = arg
        

if key_owner == 'karl':
    consumer_token = keys.karl.consumer_token
    consumer_secret = keys.karl.consumer_secret
    access_token = keys.karl.access_token
    access_token_secret = keys.karl.access_token_secret
elif key_owner == 'tina':
    consumer_token = keys.tina.consumer_token
    consumer_secret = keys.tina.consumer_secret
    access_token = keys.tina.access_token
    access_token_secret = keys.tina.access_token_secret
elif key_owner == 'hu':
    consumer_token = keys.hu.consumer_token
    consumer_secret = keys.hu.consumer_secret
    access_token = keys.hu.access_token
    access_token_secret = keys.hu.access_token_secret
elif key_owner == 'karl2':
    consumer_token = keys.karl2.consumer_token
    consumer_secret = keys.karl2.consumer_secret
    access_token = keys.karl2.access_token
    access_token_secret = keys.karl2.access_token_secret
elif key_owner == 'karl3':
    consumer_token = keys.karl3.consumer_token
    consumer_secret = keys.karl3.consumer_secret
    access_token = keys.karl3.access_token
    access_token_secret = keys.karl3.access_token_secret
elif key_owner == 'gloria':
    consumer_token = keys.gloria.consumer_token
    consumer_secret = keys.gloria.consumer_secret
    access_token = keys.gloria.access_token
    access_token_secret = keys.gloria.access_token_secret
elif key_owner == 'gloria2':
    consumer_token = keys.gloria2.consumer_token
    consumer_secret = keys.gloria2.consumer_secret
    access_token = keys.gloria2.access_token
    access_token_secret = keys.gloria2.access_token_secret    
        

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

mystreamListener = MyStreamListener()
mystream = tweepy.Stream(auth, mystreamListener)   

if create_new:
    db = server.create(city)
else:
    db = server[city]
    
mystream.filter(locations=locations[city], async=True)


