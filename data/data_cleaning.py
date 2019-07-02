import string
import re
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
from nltk.tokenize import TweetTokenizer

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize

def counting(reviews):
    tags = []

    for review in reviews:
        tag = re.findall('<[^<>]*>', review)
        if tag:
            tags.append(tag)

    tags = [item for tag in tags for item in tag]
    counter_tags = Counter(tags)
    print(counter_tags.most_common(10))

def stars_to_sentiment(score):
    if score in [1, 2] :
        return 'negative'
    elif score in [4, 5] :
        return 'positive'
    else:
        return 'neutral'

df = pd.read_csv('food.tsv', sep = '\t', encoding='latin-1')

df['text'] = df['text'].str.lower()
df['text'] = [BeautifulSoup(review, 'html.parser').get_text() for review in df['text']]
reviews = df['text']
counting(reviews)

# Processing sentences
tokenizer = TweetTokenizer(reduce_len=True, strip_handles=True)
reviews_tokenized = reviews.apply(tokenizer.tokenize)

stop = stopwords.words('english')
reviews_tokenized = reviews_tokenized.apply(lambda review: [item for item in review if item not in stop])

punctuation = string.punctuation
reviews_tokenized = reviews_tokenized.apply(lambda review: [item for item in review if item not in punctuation])

words_list = [item for review in reviews_tokenized for item in review]
counter_words = Counter(words_list)
print(counter_words.most_common(10))

reviews_clean = [' '.join(review) for review in reviews_tokenized]
df['clean_text'] = reviews_clean

# Define sentiment
df['score'] = pd.to_numeric(df['score'], downcast = 'integer')
df['sentiment'] = df['score'].apply(stars_to_sentiment)

df.to_csv('clean_dataset.csv', sep = ';', index=False)