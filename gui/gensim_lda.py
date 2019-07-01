# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import pyLDAvis.gensim  # don't skip this

import pandas as pd
import webbrowser
import os
import platform

def compute_coherence_values(id2word, corpus, texts, limit, start, step):
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

    return model_list, coherence_values

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations


def gensim_lda_product(product_id, start = 1, limit = 10, step = 1):
    df = pd.read_csv('../clean_dataset.csv', sep = ';', encoding='latin-1')

    product_df = df[df['productid'] == product_id].clean_text.values.tolist()
    data_words = list(sent_to_words(product_df))
    id2word = corpora.Dictionary(data_words)
    texts = data_words
    corpus = [id2word.doc2bow(text) for text in texts]
    model_list, coherence_values = compute_coherence_values(id2word=id2word, corpus=corpus, texts=data_words, start=start, limit=limit, step=step)
    
    # selezioniamo il modello migliore
    best_index = coherence_values.index(max(coherence_values))
    best_model = model_list[best_index]
    
    LDAvis_prepared = pyLDAvis.gensim.prepare(best_model, corpus, id2word)
    pyLDAvis.save_html(LDAvis_prepared,'lda.html')
    #pyLDAvis.show(LDAvis_prepared)
    url = 'lda.html'
    if platform.system() == 'Darwin': #Mac
        url = 'file:///' + os.path.dirname(os.path.abspath('gensim_lda.py')) + '/' + url
    webbrowser.open_new_tab(url)
