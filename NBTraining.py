import preprocess
import json
from nltk.corpus import stopwords
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import MultinomialNB
stop = stopwords.words('english')


def read_training_set(filename):
    tweets = []
    labels = []
    f = open(filename)
    for line in f:
        tweet_dict = json.loads(line)
        tweets.append(preprocess.pre_process(tweet_dict['text']))
        labels.append(int(tweet_dict["label"]))
    return tweets, labels


def build_countdict(tweets):
    count_dict = {}
    for tweet in tweets:
        for word in tweet:
            if word in count_dict:
                count_dict[word] += 1
            else:
                count_dict[word] = 1
    return count_dict


def remove_lessn(tweets, n):
    count_dict = build_countdict(tweets)
    for tweet in tweets:
            for word in tweet:
                if count_dict[word] < n:
                    del word
    return tweets


def build_dict(tweet):
    # get the feature of each word in one tweet
    feature_dict = {}
    for word in tweet:
        if word in feature_dict:
            # if the words is already in dict, increase the value by 1
            feature_dict[word] += 1
        else:
            # else add it into the dict, set the value to 1
            feature_dict[word] = 1
    return feature_dict


def remove_stopwords(tweets):
    for tweet in tweets:
        for word in tweet:
            if word in stop:
                del word
    return tweets


def convert_to_feature_dicts(tweets, removeStopWords, n):
    feature_dicts = []
    if removeStopWords:
        tweets = remove_stopwords(tweets)
    tweets = remove_lessn(tweets, n)
    for tweet in tweets:
        feature_dict = build_dict(tweet)
        feature_dicts.append(feature_dict)
    return feature_dicts


def generate_classifier():
    train_tweets, train_lables = read_training_set("train.json")
    train_dict = convert_to_feature_dicts(train_tweets, True, 1)
    vectorizer = DictVectorizer()
    train_data = vectorizer.fit_transform(train_dict)
    print "start training..."
    mnb = MultinomialNB()
    mnb = mnb.fit(train_data, train_lables)
    print "training finished"
    return mnb, vectorizer


def classify_tweet(tweet, vectorizer, classifier):
    tweets = []
    tweet = preprocess.pre_process(tweet)
    tweets.append(tweet)
    tweets = convert_to_feature_dicts(tweets, False, 0)
    data = vectorizer.transform(tweets)
    result = classifier.predict(data)
    return result[0]
