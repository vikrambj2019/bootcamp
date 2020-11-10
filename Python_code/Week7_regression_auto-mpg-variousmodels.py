%matplotlib inline

import pandas as pd
import io
import os
import numpy as np
from sklearn import metrics
import  keyFunctions as kf
import keyFunctionsP2 as kf2
from sklearn.model_selection import train_test_split
#Assigning the path
path ='https://raw.githubusercontent.com/vikrambj2019/basic/master/Data/'
filename_read=os.path.join(path,"auto-mpg.csv")

df=pd.read_csv(filename_read,na_values=['NA','?'])

preprocess = True
#Get the data file and reading the csv file to data frame using pandas

# Shuffle
np.random.seed(42)
df = df.reindex(np.random.permutation(df.index))
df.reset_index(inplace=True, drop=True)

# create feature vector
kf.missing_median(df, 'horsepower')
kf.encode_text_dummy(df, 'origin')
kf.encode_text_dummy(df, 'cylinders')

df.drop('name',1,inplace=True)

if preprocess:
    kf.encode_numeric_zscore(df, 'horsepower')
    kf.encode_numeric_zscore(df, 'weight')
    #kf.encode_numeric_zscore(df, 'cylinders')
    kf.encode_numeric_zscore(df, 'displacement')
    kf.encode_numeric_zscore(df, 'acceleration')
# Encode to a 2D matrix for training
x,y = kf2.to_xy(df,"mpg")


# Split into train/test
x_train, x_test, y_train, y_test = train_test_split(    
    x, y, test_size=0.20, random_state=42)

# sckit-learn implementation
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Model initialization
regression_model = LinearRegression()
# Fit the data(train the model)
regression_model.fit(x_train, y_train)

# Predict
y_pred_train = regression_model.predict(x_train)
y_pred_test = regression_model.predict(x_test)

path ='https://raw.githubusercontent.com/vikrambj2019/basic/master/Data/'
filename_read=os.path.join(path,"auto-mpg_new.csv")
kf.missing_median(df, 'horsepower')
kf.encode_text_dummy(df, 'origin')
kf.encode_text_dummy(df, 'cylinders')

x_new=np.array(newdf)
y_pred_new = regression_model.predict(x_new)



# Measure RMSE error.  
score_test = np.sqrt(metrics.mean_squared_error(y_pred_test,y_test))
score_train = np.sqrt(metrics.mean_squared_error(y_pred_train,y_train))

print("Final score (RMSE) of Test: {}".format(score_test))
print("Final score (RMSE) of Train: {}".format(score_train))
print('Slope:' ,regression_model.coef_)
print('Intercept:' ,regression_model.intercept_)

#model_1_features=list(df.columns)[1:]

coef=[]
for i in range(len(model_1_features)):
    coef.append([model_1_features[i],float(np.array(regression_model.coef_.reshape(-1,1).tolist()[i]))])
    

# Plot the chart
kf.chart_regression(y_pred_test.flatten(),y_test)
kf.chart_regression(y_pred_test.flatten(),y_test,sort=False)


# Sample predictions
for i in range(10):
    print("{}. Car name: {}, MPG: {}, predicted MPG: {}".format(i+1,cars[i],y_test[i],pred[i]))


#########################################################################################
    # Fitting Simple Decision tree  Regression model to the data set
from sklearn.tree import DecisionTreeRegressor
regressor = DecisionTreeRegressor(random_state = 0)

regressor.fit(x_train, y_train)
# Predict
y_pred_train = regressor.predict(x_train)
y_pred_test = regressor.predict(x_test)

# Measure RMSE error.  
score_test = np.sqrt(metrics.mean_squared_error(y_pred_test,y_test))
score_train = np.sqrt(metrics.mean_squared_error(y_pred_train,y_train))

print("Final score (RMSE) of Test: {}".format(score_test))
print("Final score (RMSE) of Train: {}".format(score_train))

#https://medium.com/cracking-the-data-science-interview/a-tour-of-the-top-10-algorithms-for-machine-learning-newbies-7228aa8ef541
#https://medium.com/ml-research-lab/machine-learning-algorithm-overview-5816a2e6303
#https://hackernoon.com/choosing-the-right-machine-learning-algorithm-68126944ce1f
