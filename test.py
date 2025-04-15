import bamt.networks as networks
import bamt.preprocessors as pp

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from pgmpy.estimators import K2


data = pd.read_csv(r'./data/real data/vk_data.csv')
data

cols = ['age', 'sex', 'has_pets', 'is_parent', 'relation', 'is_driver', 'tr_per_month', 'median_tr', 'mean_tr']
data = data[cols]
data[['sex', 'has_pets',  'is_parent', 'relation', 'is_driver']] = data[['sex',     'has_pets',     'is_parent', 'relation', 'is_driver']].astype(str)

encoder = preprocessing.LabelEncoder()
discretizer = preprocessing.KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='quantile')

p = pp.Preprocessor([('encoder', encoder), ('discretizer', discretizer)])
discretized_data, est = p.apply(data)

bn = networks.HybridBN(has_logit=True, use_mixture=True) # init BN
info = p.info
info
bn.add_nodes(info)

bn.add_edges(discretized_data,  scoring_function=('K2',K2))
bn.set_classifiers(classifiers={'age': DecisionTreeClassifier(),
                             'relation': RandomForestClassifier(),
                             'is_driver': KNeighborsClassifier(n_neighbors=2)})
bn.fit_parameters(data)

bn.plot('bn.html')