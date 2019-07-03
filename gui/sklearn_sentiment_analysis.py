import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
warnings.filterwarnings("ignore",category=FutureWarning)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn import metrics

def weighted_splitting(df):

    df['index']= list(range(df.shape[0]))
    train_df = pd.DataFrame()

    for productid_action in df['productid'].unique():
        productid_df = df.loc[df['productid'] == productid_action]
        n_instance = productid_df.shape[0]
        train_df = train_df.append(productid_df.sample(n = int(0.8 * n_instance), replace = False))

    test_df = pd.concat([df, train_df]).drop_duplicates(keep=False)

    return train_df['clean_text'], test_df['clean_text'], train_df['sentiment'], test_df['sentiment']

def plot_confusion_matrix(cm, analysis_field, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    
    string_normalized = 'not-normalized'
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        string_normalized = 'normalized'

    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.xlabel('True label')
    plt.ylabel('Predicted label')
    plt.savefig(f'graphs/confusion_matrix_{analysis_field}_{string_normalized}.png', dpi = 180)
    plt.show()

def sklearn_sa(analysis_field, normalized, split_type = None):

    df = pd.read_csv('../data/clean_dataset.csv', sep = ';', encoding='latin-1')

    if split_type and split_type == 'weighted':
        X_train, X_test, y_train, y_test = weighted_splitting(df)
    else:
        X_train, X_test, y_train, y_test = train_test_split(df['clean_text'], df[analysis_field], \
                                    random_state=np.random.randint(df.shape[0]), \
                                    shuffle=True, train_size=0.80)
    print(X_train.shape)
    print(X_test.shape)
    print()

    vect = CountVectorizer().fit(X_train)
    X_train_vectorized = vect.transform(X_train)
    X_train_vectorized.toarray()

    #model = LogisticRegression()
    model = RandomForestClassifier(n_estimators = 115, random_state = np.random.randint(df.shape[0]))

    model.fit(X_train_vectorized, y_train)

    predictions = model.predict(vect.transform(X_test))

    classes = sorted(df[analysis_field].unique(), reverse = True)

    confusion_matrix = metrics.confusion_matrix(y_test, predictions, labels = classes).T
    metrics_matrix = metrics.classification_report(y_test, predictions)    
    accuracy = metrics.accuracy_score(y_test, predictions, normalize=True, sample_weight=None)

    print(confusion_matrix)
    print(metrics_matrix)
    print(accuracy)

    plot_confusion_matrix(
            confusion_matrix,
            analysis_field,
            classes,
            normalize=normalized
        )