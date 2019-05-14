import nltk
import spacy
from spacy.lang.en import English
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import random
import gensim
from gensim import corpora
import pickle
# import pyLDAvis.gensim
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
    # text_data = []
    # with open("test.csv") as f:
    # for l in text:
    tokens = prepare_text_for_lda(text)
            # if random.random() > .99:
        # text_data.append(tokens)
    return tokens

def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def get_topics(tweet, train_data):
    dictionary = corpora.Dictionary(train_data)
    tokens = prepare_tweet(tweet)
    corpus = [dictionary.doc2bow(tokens)]
    pickle.dump(corpus, open('corpus.pkl', 'wb'))
    dictionary.save('dictionary.gensim')

    NUM_TOPICS = 3
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=0)
    ldamodel.save('model5.gensim')

    prob_topics = ldamodel.print_topics(num_words=4)
    topics = []
    for i in prob_topics:
        split = i[1].split("\"")
        topics.append(split[1])
        # topics.append(split[3])
        # topics.append(split[5])
        # print(split[1])
    return unique(topics)

def train_model(text):
    train_data = []
    with open(text) as f:
        for line in f:
            tokens = prepare_text_for_lda(line)
            if random.random() > .99:
                # print(tokens)
                train_data.append(tokens)
    return train_data


# USE pyLDAvis
# topics = get_topics("test", train_model("test"))

# ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 3, id2word=dictionary, passes=15)
# ldamodel.save('model3.gensim')
# topics = ldamodel.print_topics(num_words=4)
# for topic in topics:
#     print(topic)

# ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 10, id2word=dictionary, passes=15)
# ldamodel.save('model10.gensim')
# topics = ldamodel.print_topics(num_words=4)
# for topic in topics:
#     print(topic)
