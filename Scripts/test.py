from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.base import TransformerMixin
import numpy as np
from sklearn.pipeline import Pipeline, FeatureUnion
training_set = [
  {'p1':'A', 'p2':'T', 'p3':'G', 'p4':'C', 'p5':'T',
   'p6':'A', 'p7':'C', 'p8':'T', 'p9':'G', 'p10':'A',
   'mass':370.2, 'temp':70.0},
  {'p1':'A', 'p2':'C', 'p3':'G', 'p4':'T', 'p5':'A',
   'p6':'C', 'p7':'T', 'p8':'G', 'p9':'A', 'p10':'T',
   'mass':400.3, 'temp':67.2}
]

target = [1,0]

vec = DictVectorizer()
train = vec.fit_transform(training_set).toarray()



# The following part fails.
test_set =   {
  'p1':'A', 'p2':'T', 'p3':'G', 'p4':'C', 'p5':'T',
  'p6':'A', 'p7':'C', 'p8':'T', 'p9':'G', 'p10':'A',
  'mass':370.2, 'temp':70.0}

class testtran(TransformerMixin):

    def transform(self, X, **transform_params):
        vec = DictVectorizer()
        return vec.fit_transform(X).toarray()

    def fit(self, X, y=None, **fit_params):
        return self


class newtransform(TransformerMixin):
    def transform(self, X, **transform_params):
        vec=DictVectorizer()
        print vec.fit_transform(X).toarray()
        return  ([["A","A"],["B","C"]])#vec.fit_transform(X).toarray()

    def fit(self, X, y=None, **fit_params):
        return self


combined_features = FeatureUnion([("pca", newtransform()), ("univ_select", testtran())])

# Use combined features to transform dataset:
X_features = combined_features.fit(training_set).transform(training_set)
print (X_features)

