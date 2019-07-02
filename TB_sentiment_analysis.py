import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from textblob import TextBlob

def polarity(text_clean):
    line = TextBlob(text_clean)
    return line.sentiment.polarity

def subjectivity(text_clean):
    line = TextBlob(text_clean)
    return line.sentiment.subjectivity

def sentiment_number(sentiment):
    if sentiment == 'negative':
        return -1
    elif sentiment == 'positive':
        return 1
    else:
        return 0

df = pd.read_csv('data/clean_dataset.csv', sep = ';', encoding='latin-1')

df['polarity'] = df['clean_text'].apply(polarity)
df['subjectivity'] = df['clean_text'].apply(subjectivity)
df['sentiment'] = df['sentiment'].apply(sentiment_number)

score_counter = Counter((df['score']-3)/2)
sentiment_counter = Counter(df['sentiment'])
polarity_counter = Counter(df['polarity'].round(1))

legend = []
labels = []
colors = ['#ff0000', '#00ff00']

legend.append(plt.bar(list(score_counter.keys()), list(score_counter.values()), \
                      width = 0.1, color = colors[0], alpha = 0.5)[0])
labels.append('score_counter')

legend.append(plt.bar(list(polarity_counter.keys()), list(polarity_counter.values()), \
                      width = 0.1, color = colors[1], alpha = 0.5)[0])
labels.append('polarity')

plt.grid(True)
plt.legend(legend, labels)
plt.savefig('tb_polarity-score.png', dpi = 180)
plt.show()