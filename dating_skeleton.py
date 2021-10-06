import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

#Create your df here:
df = pd.read_csv('profiles.csv')
# print(df.job.value_counts())

#visualizing
# plt.hist(df.age, bins = 20)
# plt.xlabel('Age')
# plt.ylabel('Frequency')
# plt.xlim(16,80)
# plt.show()

#zodiac signs
# print(df.sign.value_counts())

#drink mapping
# print(df.smokes.value_counts())
# print(df.drugs.value_counts())
drink_mapping = {"not at all": 0, "rarely": 1, "socially": 2, "often": 3,
"very often": 4, "desperately": 5}
df['drink_map'] = df.drinks.map(drink_mapping)
# print(df.drink_map.value_counts())

#smoke mapping
smoke_mapping = {"no":0, "trying to quit":1, "sometimes":2, "when drinking":3, "yes":4}
df['smoke_map'] = df.smokes.map(smoke_mapping)
# print(df.smoke_map.value_counts())

# drug mapping
drug_mapping = {'never':0, 'sometimes':1, 'often':2}
df['drug_map'] = df.drugs.map(drug_mapping)
# print(df.drug_map.value_counts())

#essay analysis
essay_cols = ['essay0', 'essay1', 'essay2', 'essay3', 'essay4', 'essay5', 'essay6', 'essay7', 'essay8', 'essay9']
all_essays = df[essay_cols].replace(np.nan, '', regex = True)
all_essays = all_essays[essay_cols].apply(lambda x: ' '.join(x), axis = 1)
df['essay_len'] = all_essays.apply(lambda x:len(x))
list_of_words = all_essays.apply(lambda x: x.split())
# print((type(list_of_words[0][0])))
# print(list_of_words)
def avg_len(lst):
    for i in range(len(lst)):
        lst[i] = len(lst[i])
    return np.mean(lst)
df['avg_word_len'] = list_of_words.apply(lambda x: avg_len(x))
import re
list_of_words = all_essays.apply(lambda x: x.split())
def i_me(lst):
    counter = 0
    for i in range(len(lst)):
        if (re.match("^[Mm][Ee]$|^[Ii]$|^[Ii]'[m]$", lst[i])):
            # print(lst[i])
            counter += 1
    return counter
df['i_me_count'] = list_of_words.apply(lambda x: i_me(x))

#normalize your data
feature_data = df[['smoke_map', 'drink_map', 'drug_map', 'essay_len', 'avg_word_len']]
label_data = df[['i_me_count']]
# print(feature_data.head())
# print(label_data.head())
x = feature_data.values
y = label_data.values
from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()
# imputer = preprocessing.Imputer()
x_scaled = min_max_scaler.fit_transform(x)
y_scaled = min_max_scaler.fit_transform(y)
feature_data = pd.DataFrame(x_scaled, columns = feature_data.columns)
label_data = pd.DataFrame(y_scaled, columns = label_data.columns)
from sklearn.impute import SimpleImputer
imputer = SimpleImputer()
feature_imputed = imputer.fit_transform(feature_data)
label_imputed = imputer.fit_transform(label_data)
# feature_data = feature_data.fillna(feature_data.mean())
# label_data = label_data.fillna(label_data.mean())
# print(feature_data.head())
# print(label_data.head())

#make a model to see if you can use first 5 features to predict last
#don't use normalized?
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
x_train, x_test, y_train, y_test = train_test_split(feature_imputed
, label_imputed, train_size=0.8, test_size=0.2, random_state = 42)
mlr = LinearRegression()
mlr.fit(x_train, y_train)
y_predicted = mlr.predict(x_test)
#creating scatter plot to show how close y_predicted is to y_test
# plt.colorbar()
print('y_test')
print(y_test)
print('y_predicted')
print(y_predicted)
plt.xlabel('actual i_me_count')
plt.ylabel('predicted i_me_count')
plt.title('actual vs predicted')
# plt.scatter([1,2,3,4], [5,6,7,8])
plt.scatter(y_test, y_predicted, alpha = .25)
plt.show()

#showing accuracy, recall, precision
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
print('printing scores')
print(accuracy_score(y_test, y_predicted))
print(recall_score(y_test, y_predicted))
print(precision_score(y_test, y_predicted))
print(f1_score(y_test, y_predicted))
