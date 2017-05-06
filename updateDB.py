import couchdb
import getopt
import sys
import NBTraining
import time

server = couchdb.Server('http://ccc:cloud@localhost:5984/')
classifier, vectorizer = NBTraining.generate_classifier()

try:
    opts, args = getopt.getopt(sys.argv[1:], 'c:m:', ['city=', 'model='])
except getopt.GetoptError:
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-c', '--city'):
        city = arg

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
    if label == 0:
        count += 1
    else:
        pos += 1

    if index%100 == 0:
        print "processing doc{}".format(index)
    doc['lable_ccc'] = label
    db.update([doc])

end = time.time()
print "time:", end-start
