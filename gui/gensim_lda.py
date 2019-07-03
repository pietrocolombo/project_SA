import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
import os
import re
import pandas as pd
import webbrowser
import platform
from textblob import TextBlob



# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import pyLDAvis.gensim  # don't skip this

def compute_coherence_values(id2word, corpus, texts, start, limit, step, on_update):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    
    value_progress_bar = 5
    n_models = len(range(start, limit, step))
    increment_progress_bar = int(55/n_models)

    for num_topics in range(start, limit, step):
        model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                   id2word=id2word,
                                                   num_topics=num_topics, 
                                                   random_state=100,
                                                   update_every=1,
                                                   chunksize=100,
                                                   passes=10,
                                                   alpha='auto',
                                                   per_word_topics=True)
        
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=id2word, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
        value_progress_bar += increment_progress_bar
        on_update(value_progress_bar)

    return model_list, coherence_values

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations


def gensim_lda_product(product_id, n_execution, start = 2, limit = 10, step = 1, on_update=None):
    df = pd.read_csv('../data/clean_dataset.csv', sep = ';', encoding='latin-1')

    product_df = df[df['productid'] == product_id].clean_text.values.tolist()
    data_words = list(sent_to_words(product_df))
    id2word = corpora.Dictionary(data_words)
    texts = data_words
    corpus = [id2word.doc2bow(text) for text in texts]
    on_update(5)
    model_list, coherence_values = compute_coherence_values(id2word=id2word, corpus=corpus, texts=data_words, start=start, limit=limit, step=step, on_update=on_update)
    
    # selezioniamo il modello migliore
    best_index = coherence_values.index(max(coherence_values))
    best_model = model_list[best_index]
    
    LDAvis_prepared = pyLDAvis.gensim.prepare(best_model, corpus, id2word)
    on_update(90)
    pyLDAvis.save_html(LDAvis_prepared,f'lda_model/lda_{n_execution}.html')
    on_update(95)

    polarity_df = sentiment_topic(best_model)

    #pyLDAvis.show(LDAvis_prepared)
    url = f'lda_model/lda_{n_execution}.html'
    if platform.system() == 'Darwin': #Mac
        url = 'file:///' + os.path.dirname(os.path.abspath('gensim_lda.py')) + '/' + url
    webbrowser.open_new_tab(url)
    on_update(100)

def sentiment_topic(lda_model):

    topic_words = lda_model.print_topics(num_words=100)
    polarity_df = pd.DataFrame(columns=['topic', 'polarity'])
    for topic in topic_words:
        weighted_words = topic[1]
        weighted_words = weighted_words.split(' + ')
        weighted_words = [pair.split('*') for pair in weighted_words]

        sentiment_words = []
        sentiment_weights = []
        for pair in weighted_words:
            word = pair[1].lstrip('"').rstrip('"')
            weight = float(pair[0])
            if not TextBlob(word).sentiment.polarity == 0:
                sentiment_words.append(word)
                sentiment_weights.append(weight)

        total_weight = sum(sentiment_weights)
        sentiment_weights = [weight/total_weight for weight in sentiment_weights]

        topic_polarity = 0
        for word, weight in zip(sentiment_words, sentiment_weights):
            topic_polarity += TextBlob(word).sentiment.polarity*weight
        
        data = [[topic[0], topic_polarity]]
        row = pd.DataFrame(data, columns=['topic', 'polarity'])
        polarity_df = polarity_df.append(row)
    
    return polarity_df
