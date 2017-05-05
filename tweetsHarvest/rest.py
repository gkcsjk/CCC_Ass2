import getopt
import sys

import couchdb
import tweepy

import keys

locations = {
    "melbourne": "-37.9154,145.0692,50km",
    "sydney": "-33.8274,151.0569,50km",
    "brisbane": "-27.4379,153.0625,50km",
    "adelaide": "-34.9326,138.6001,50km",
    "perth": "-31.9526,115.8633,50km",
    "canberra": "-35.2940,149.1153,50km"
}

tweetsPerQry = 100

USERNAME = 'ccc'
PASSWORD = 'cloud'


server = couchdb.Server('http://ccc:cloud@localhost:5984/')

sinceID = None

max_id = -1L
tweetCount = 0

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

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        
if create_new:
    db = server.create(city)
else:
    db = server[city]

while 1:
    try:
        if max_id < 0:
            if not sinceID:
                new_tweets = api.search(geocode=locations[city], count=tweetsPerQry)
            else:
                new_tweets = api.search(geocode=locations[city], count=tweetsPerQry, since_id = sinceID)
        else:
            if not sinceID:
                new_tweets = api.search(geocode=locations[city], count=tweetsPerQry,
                                    max_id=str(max_id - 1))
            else:
                new_tweets = api.search(geocode=locations[city], count=tweetsPerQry,
                                    max_id=str(max_id - 1),
                                    since_id=sinceID)
        if not new_tweets:
            print("No more tweets found")
            break

        tweetCount += len(new_tweets)
        print("Downloaded {0} tweets".format(tweetCount))
        for tweet in new_tweets:
            data = tweet._json
            doc = [data]
            db.update(doc)
            max_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        print "some error:"+str(e)
        break
