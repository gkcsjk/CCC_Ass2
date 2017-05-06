import nltk
import re


lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
w = frozenset(nltk.corpus.words.words())


def pre_process(tweet):
    tweet = remove_username(tweet)
    tweet = remove_url(tweet)
    tweet = lowercase_words(tweet)
    tweet = remove_hashtags(tweet)
    tweet = tokenize_words(tweet)
    return tweet


def lemmatize(word):
    lemma = lemmatizer.lemmatize(word, 'v')
    if lemma == word:
        lemma = lemmatizer.lemmatize(word, 'n')
    return lemma


def remove_username(tweet):
    tweet = re.sub("@[^\s^\r^\n]*", "", tweet).strip()
    return tweet


def remove_url(tweet):
    tweet = re.sub("https?:\/\/[^\s^\r^\n]*", "", tweet).strip()
    return tweet


def lowercase_words(tweet):
    tweet = tweet.lower()
    return tweet


def remove_hashtags(tweet):
    # tweet = re.sub("#[^\s^\r^\n]*", "", tweet).strip()
    # return tweet

    hashtags = re.findall("#[^\s^\r^\n]*", tweet)
    hashtags_ans = ""
    if len(hashtags) == 0:
        return tweet

    else:
        tweet = re.sub("#[^\s^\r^\n]*", "", tweet).strip()
        for hashtag in hashtags[:]:
            hashtags_ans = hashtags_ans + " " + maxmatch(hashtag)
        return tweet + hashtags_ans


def maxmatch(hashtag):
    if len(hashtag) == 0:
        return ""
    hashtag = re.sub("#", "", hashtag).strip()
    l = len(hashtag)
    for i in range(l, 0, -1):
        firstword = hashtag[0:i]
        remainder = hashtag[i:l]
        if lemmatize(firstword) in w:
            return firstword + " " + maxmatch(remainder)

    firstword = hashtag[0:1]
    remainder = hashtag[1:l]
    return firstword + " " + maxmatch(remainder)


def tokenize_words(tweet):
    word_tokenizer = nltk.tokenize.regexp.WordPunctTokenizer()
    word_tokenizer = word_tokenizer.tokenize(tweet)
    for i, word in enumerate(word_tokenizer):
        word_tokenizer[i] = lemmatize(word)
    return word_tokenizer




