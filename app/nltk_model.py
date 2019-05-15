import nltk
import spacy
from spacy.lang.en import English
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import random
import gensim
from gensim import corpora
import pickle
import numpy

spacy.load('en')
nltk.download('wordnet')
nltk.download('stopwords')

parser = English()

def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens


def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

def prepare_text_for_lda(text):
    en_stop = set(nltk.corpus.stopwords.words('english'))
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

def prepare_tweet(text):
    tokens = prepare_text_for_lda(text)
    return tokens

def get_topics(tweet, train_data):
    """
    Uncomment to train new dataset for model
    """
    # dictionary = corpora.Dictionary(train_data)
    # tokens = prepare_tweet(tweet)
    # corpus = [dictionary.doc2bow(tokens)]
    # pickle.dump(corpus, open('corpus.pkl', 'wb'))
    # pickle.dump(dictionary, open('dictionary.pkl', 'wb'))
    
    """
    Loads from file
    """
    corpus = pickle.load(open('corpus.pkl', 'rb'))
    dictionary = pickle.load(open('dictionary.pkl', 'rb'))
    
    NUM_TOPICS = 4

    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=0)
    pickle.dump(ldamodel, open('model5.gensim', 'wb'))

    prob_topics = ldamodel.print_topics(num_words=3)
    topics = []
    for i in prob_topics:
        split = i[1].split("\"")
        topics.append(split[1])
    return topics

def train_model(text):
    train_data = []
    with open(text) as f:
        for line in f:
            tokens = prepare_text_for_lda(line)
            if random.random() > .99:
                train_data.append(tokens)
    return train_data

# topics = get_topics("test tweet about world", "train8.csv")
# for topic in topics:
#     print(topic)

