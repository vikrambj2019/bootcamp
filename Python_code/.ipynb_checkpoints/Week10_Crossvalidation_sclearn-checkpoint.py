# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 10:05:18 2018

@author: Vikram Bandugula
"""
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_boston
import numpy as np
boston = load_boston()
data = boston.data
target = boston.target

# train/test split
X_train, X_test, y_train, y_test = train_test_split(data, 
                                                    target, 
                                                    shuffle=True,
                                                    test_size=0.2, 
                                                    random_state=15)

def calc_train_error(X_train, y_train, model):
    '''returns in-sample error for already fit model.'''
    predictions = model.predict(X_train)
    mse = mean_squared_error(y_train, predictions)
    rmse = np.sqrt(mse)
    return mse
    
def calc_validation_error(X_test, y_test, model):
    '''returns out-of-sample error for already fit model.'''
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    return mse
    
def calc_metrics(X_train, y_train, X_test, y_test, model):
    '''fits model and returns the RMSE for in-sample error and out-of-sample error'''
    model.fit(X_train, y_train)
    train_error = calc_train_error(X_train, y_train, model)
    validation_error = calc_validation_error(X_test, y_test, model)
    return train_error, validation_error

import pandas as pd
url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/forest-fires/forestfires.csv'
df = pd.read_csv(url)
df.head()

df = pd.get_dummies(df)

df.drop(labels=['month_dec', 'day_sat'], axis=1, inplace=True)

df.max() - df.min()

from sklearn.linear_model import LinearRegression

data = df.copy()
target = data.pop('area')

lr = LinearRegression(fit_intercept=True)
lr.fit(data, target)

from sklearn.metrics import mean_squared_error

# R^2
print(lr.score(data, target)) 

predictions = lr.predict(data)
mse = mean_squared_error(target, predictions)
rmse = np.sqrt(mse)
print(rmse)


#-------------------------------------------------------------------
# intermediate/test split (gives us test set)
X_intermediate, X_test, y_intermediate, y_test = train_test_split(data, 
                                                                  target, 
                                                                  shuffle=True,
                                                                  test_size=0.2, 
                                                                  random_state=15)

# train/validation split (gives us train and validation sets)
X_train, X_validation, y_train, y_validation = train_test_split(X_intermediate,
                                                                y_intermediate,
                                                                shuffle=False,
                                                                test_size=0.25,
                                                                random_state=2018)
# delete intermediate variables
del X_intermediate, y_intermediate

# print proportions
print('train: {}% | validation: {}% | test {}%'.format(round(len(y_train)/len(target),2),
                                                       round(len(y_validation)/len(target),2),
                                                       round(len(y_test)/len(target),2)))

from sklearn.linear_model import Ridge
alphas = [0.001, 0.01, 0.1, 1, 10]
print('All errors are RMSE')
print('-'*76)
for alpha in alphas:
    # instantiate and fit model
    ridge = Ridge(alpha=alpha, fit_intercept=True, random_state=99)
    ridge.fit(X_train, y_train)
    # calculate errors
    new_train_error = mean_squared_error(y_train, ridge.predict(X_train))
    new_validation_error = mean_squared_error(y_validation, ridge.predict(X_validation))
    new_test_error = mean_squared_error(y_test, ridge.predict(X_test))
    # print errors as report
    print('alpha: {:7} | train error: {:5} | val error: {:6} | test error: {}'.
          format(alpha,
                 round(new_train_error,3),
                 round(new_validation_error,3),
                 round(new_test_error,3)))
    