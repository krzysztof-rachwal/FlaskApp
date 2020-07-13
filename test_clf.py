import json
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer, TfidfTransformer
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import fetch_20newsgroups
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
import numpy as np
from joblib import dump, load
import pickle


# categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
twenty_train = fetch_20newsgroups(subset='train', shuffle=True, random_state=42)

vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(twenty_train.data)

tf_transformer = TfidfTransformer()
X_train_tfidf = tf_transformer.fit_transform(X_train_counts)


# vectorizer = TfidfVectorizer()
# vectorizer.fit(twenty_train.data)
# X = vectorizer.transform(twenty_train.data)
# clf = LogisticRegression()
# clf.fit(X, twenty_train.target)


tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
X_new_tfidf = tf_transformer.transform(X_train_tf)
#print(X_train_tf.shape)

clf = MultinomialNB().fit(X_train_counts, twenty_train.target)

#using pipeline and SGDClassifier, slow but one of the best.     
clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None)),
])

clf.fit(twenty_train.data, twenty_train.target)


# twenty_test = fetch_20newsgroups(subset='test', categories=categories, shuffle=True, random_state=42)
# docs_test = twenty_test.data
# predicted = clf.predict(docs_test)


# test_list = ["Everybody should have access to guns and automatic rifles. This is the second amendmend right."]
# #docs_list = test_list.data
# pred = clf.predict(test_list)

# print(pred)

dump(clf, 'models/model.joblib')
dump(vectorizer, 'models/vectorizer.joblib')

# print(np.mean(predicted == twenty_test.target))
# print(metrics.classification_report(twenty_test.target, predicted, target_names=twenty_test.target_names))
# print(twenty_train.target_names)
# print(len(twenty_train.data))
# print(len(twenty_train.filenames))