"""
Credit Risk Analysis using machine learning and deep learning models
Ten Feature Analysis: lightgbm
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn import metrics
from sklearn.metrics import roc_auc_score,roc_curve,auc
import category_encoders as ce
import matplotlib.pyplot as plt
from lightgbm import LGBMClassifier

#------------------Data Cleaning-----------------#
all_data=pd.read_csv("new_data_preprocessed.csv")
# Special for lightGBM (it does not support special JSON characters)
import re
all_data = all_data.rename(columns = lambda x:re.sub('[^A-Za-z0-9_]+', '', x))

X = all_data.drop(columns=['TARGET'])
y = all_data['TARGET']

#------------------Ten Feature-------------------#
X_m1 = X.iloc[:,[34,11,8,10,5,4,9,172,57,64]]
X_m2 = X.iloc[:,[28,29,30,79,26,60,20,2,36,16]]
X_m3 = X.iloc[:,[29,28,79,16,18,83,2,56,55,64]]
X_m31 = X.iloc[:,[80,81,56,79,27,36,82,2,18,16]]
X_m32 = X.iloc[:,[29,18,26,79,16,28,82,60,2,30]]
X_m33 = X.iloc[:,[28,29,8,34,10,11,0,5,9,7]]

X_train,X_test,y_train,y_test = train_test_split(X_m33,y,test_size=0.2,random_state=999)
X_train,X_valid,y_train,y_valid = train_test_split(X_train,y_train,test_size=0.25,random_state=999)

#------------------Data Preprosessing --------------------#
# SMOTE Algorithm to get balanced set
from collections import Counter
from imblearn.over_sampling import SMOTE
smo = SMOTE(random_state=99)
X_trains, y_trains = smo.fit_sample(X_train, y_train)
print(Counter(y_trains))

lgbm = LGBMClassifier(n_estimators=250,learning_rate=0.65,
                          num_leaves=41,max_depth=28,
                          subsample=0.5,random_state=100)
lgbm.fit(X_trains,y_trains)


# Validation Set
y_hat1 = lgbm.predict(X_valid)  
print("M3.3(valid) RMSE:", np.sqrt(metrics.mean_squared_error(y_valid, y_hat1))) 
print("M3.3(valid) AUC:",roc_auc_score(y_valid, y_hat1))
# Testing Set
y_hat2 = lgbm.predict(X_test)  
print("M3.3(test) RMSE:", np.sqrt(metrics.mean_squared_error(y_test, y_hat2))) 
print("M3.3(test) AUC:",roc_auc_score(y_test, y_hat2))

