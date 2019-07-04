import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

def text_blob_sa(self, analysis_field):

    if self.sa_df.empty:
        df = pd.read_csv('../data/clean_dataset.csv', sep = ';', encoding='latin-1')

        df['polarity'] = df['clean_text'].apply(polarity)
        #self.df['subjectivity'] = self.df['clean_text'].apply(subjectivity)
        df['sentiment'] = df['sentiment'].apply(sentiment_number)
    else:
        df = self.sa_df

    plt.figure()
    sns.boxenplot(x=analysis_field, y='polarity', data=df)
    plt.savefig(f'graphs/tb_polarity_each_{analysis_field}.png', dpi = 180)
    plt.show();

    analysis = df[analysis_field]
    if analysis_field == 'score':
        analysis = (analysis-3)/2

    analysis_counter = Counter(analysis)
    polarity_counter = Counter(df['polarity'].round(1))

    plt.figure()

    legend = []
    labels = []
    colors = ['#ff0000', '#00ff00']

    legend.append(plt.bar(list(analysis_counter.keys()), list(analysis_counter.values()), \
                      width = 0.1, color = colors[0], alpha = 0.5)[0])
    labels.append(f'{analysis_field}')
    legend.append(plt.bar(list(polarity_counter.keys()), list(polarity_counter.values()), \
                      width = 0.1, color = colors[1], alpha = 0.5)[0])
    labels.append('polarity')

    plt.grid(True)
    plt.legend(legend, labels)
    plt.savefig(f'graphs/tb_polarity_{analysis_field}.png', dpi = 180)
    plt.show()

    self.sa_df = df