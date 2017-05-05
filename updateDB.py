import couchdb
import getopt
import sys
import NBTraining

USERNAME = 'ccc'
PASSWORD = 'cloud'
server = couchdb.Server('http://ccc:cloud@localhost:5984/')
classifier = NBTraining.generate_classifier()

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
for doc in db:
    index += 1
    if index%10 == 0:
        print "processing doc{}".format(index)
    doc = db[doc]
    tweet = doc['text']
    label = NBTraining.classify_tweet(tweet, classifier)
    doc['lable_ccc'] = label
    db.update(doc)

