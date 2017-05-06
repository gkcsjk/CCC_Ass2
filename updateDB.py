import couchdb
import getopt
import sys
import NBTraining
import time

server = couchdb.Server('http://admin:helloworld@localhost:5984/')
classifier, vectorizer = NBTraining.generate_classifier()

try:
    opts, args = getopt.getopt(sys.argv[1:], 'c:m:',['city=', 'model='])
except getopt.GetoptError:
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-c', '--city'):
        city = arg
    elif opt in ('-c', '--model'):
        filename = arg

db = server[city]

index = 0
count = 0
neutral = 0
pos = 0

start = time.time()
for doc in db:
    index += 1
    doc = db[doc]
    tweet = doc['text']
    label = NBTraining.classify_tweet(tweet, vectorizer, classifier)
    if label == -1:
        count += 1
    elif label == 0:
        neutral += 1
    else:
        pos += 1

    if index%10 == 0:
        print "processing doc{}".format(index)
    doc['lable_ccc'] = label
    db.update([doc])

end = time.time()
print "neg", count
print "neu", neutral
print "pos", pos
print "time:", end-start
