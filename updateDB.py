import couchdb
import getopt
import sys

USERNAME = 'ccc'
PASSWORD = 'cloud'
server = couchdb.Server('http://ccc:cloud@localhost:5984/')

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

for doc in db:
    print doc["text"]
