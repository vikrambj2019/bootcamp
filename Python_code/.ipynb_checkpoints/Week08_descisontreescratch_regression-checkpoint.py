"""
Make the imports of python packages needed
"""
import pandas as pd
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib import style
style.use("fivethirtyeight")
import os
import time
import keyFunctionsP2 as kf2
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

from sklearn.metrics import mean_squared_error
from math import sqrt

###########################################################################################################

#Import the dataset and define the feature and target columns#
path='C:/Users/Vikram Bandugula/Documents/work_t/python_code/deep_learning-master/data/'
#Get the data file and reading the csv file to data frame using pandas
filename_read = os.path.join(path,"day.csv")

dataset = pd.read_csv(filename_read,usecols=['season','holiday','weekday','workingday','weathersit','temp','atemp','hum','windspeed','casual','registered','cnt']).sample(frac=1)
target='cnt'
mean_data = np.mean(dataset[target])
target_data=dataset[target]




###########################################################################################################
"""
Calculate the varaince of a dataset
This function takes three arguments.
1. data = The dataset for whose feature the variance should be calculated
2. split_attribute_name = the name of the feature for which the weighted variance should be calculated
3. target_name = the name of the target feature. The default for this example is "cnt"
"""    
def var(data,split_attribute_name,target_name="cnt"):
    
    feature_values = np.unique(data[split_attribute_name])
    feature_variance = 0
    for value in feature_values:
        #Create the data subsets --> Split the original data along the values of the split_attribute_name feature
        # and reset the index to not run into an error while using the df.loc[] operation below
        subset = data.query('{0}=={1}'.format(split_attribute_name,value)).reset_index()
        #Calculate the weighted variance of each subset            
        value_var = (len(subset)/len(data))*np.var(subset[target_name],ddof=1)
        #Calculate the weighted variance of the feature
        feature_variance+=value_var
    return feature_variance
    
###########################################################################################################

###########################################################################################################
def determine_type_of_feature(df):
    
    feature_types = []
    n_unique_values_treshold = 10
    for feature in df.columns:
        if feature != "label":
            unique_values = df[feature].unique()
            example_value = unique_values[0]
            #print(example_value)
            if (isinstance(example_value, str)) or (len(unique_values) <= n_unique_values_treshold):
                feature_types.append("categorical")
            else:
                feature_types.append("continuous")
    
    return feature_types


###########################################################################################################
def Classification(data,originaldata,features,min_instances,target_attribute_name,parent_node_class = None):
    """
    Classification Algorithm: This function takes the same 5 parameters as the original classification algorithm in the
    previous chapter plus one parameter (min_instances) which defines the number of minimal instances
    per node as early stopping criterion.
    """   
    #Define the stopping criteria --> If one of this is satisfied, we want to return a leaf node#
    
    #########This criterion is new########################
    #If all target_values have the same value, return the mean value of the target feature for this dataset
    if len(data) <= int(min_instances):
        return np.mean(data[target_attribute_name])
    #######################################################
    
    #If the dataset is empty, return the mean target feature value in the original dataset
    elif len(data)==0:
        return np.mean(originaldata[target_attribute_name])
    
    #If the feature space is empty, return the mean target feature value of the direct parent node --> Note that
    #the direct parent node is that node which has called the current run of the algorithm and hence
    #the mean target feature value is stored in the parent_node_class variable.
    
    elif len(features) ==0:
        return parent_node_class
    
    #If none of the above holds true, grow the tree!
    
    else:
        #Set the default value for this node --> The mean target feature value of the current node
        parent_node_class = np.mean(data[target_attribute_name])
        #Select the feature which best splits the dataset
        item_values = [var(data,feature) for feature in features] #Return the variance for features in the dataset
        best_feature_index = np.argmin(item_values)
        best_feature = features[best_feature_index]
        
        #Create the tree structure. The root gets the name of the feature (best_feature) with the minimum variance.
        tree = {best_feature:{}}
        
        
        #Remove the feature with the lowest variance from the feature space
        features = [i for i in features if i != best_feature]
        
        #Grow a branch under the root node for each possible value of the root node feature
        
        for value in np.unique(data[best_feature]):
            value = value
            #Split the dataset along the value of the feature with the lowest variance and therewith create sub_datasets
            sub_data = data.where(data[best_feature] == value).dropna()
            
            #Call the Calssification algorithm for each of those sub_datasets with the new parameters --> Here the recursion comes in!
            subtree = Classification(sub_data,originaldata,features,min_instances,'cnt',parent_node_class = parent_node_class)
            
            #Add the sub tree, grown from the sub_dataset to the tree under the root node
            tree[best_feature][value] = subtree
            
        return tree   
    
    
###########################################################################################################
###########################################################################################################
 
"""
Predict query instances
"""
    
def predict(query,tree,default = mean_data):
    for key in list(query.keys()):
        if key in list(tree.keys()):
            try:
                result = tree[key][query[key]] 
            except:
                return default
            result = tree[key][query[key]]
            if isinstance(result,dict):
                return predict(query,result)
            else:
                return result
        
###########################################################################################################
###########################################################################################################
"""
Compute the RMSE 
"""
def test(data,tree):
    #Create new query instances by simply removing the target feature column from the original dataset and 
    #convert it to a dictionary
    queries = data.iloc[:,:-1].to_dict(orient = "records")
    
    #Create a empty DataFrame in whose columns the prediction of the tree are stored
    predicted = []
    #Calculate the RMSE
    for i in range(len(data)):
        predicted.append(predict(queries[i],tree,mean_data)) 
    RMSE = np.sqrt(np.sum(((data.iloc[:,-1]-predicted)**2)/len(data)))
    return RMSE,predicted
###########################################################################################################
###########################################################################################################  
def determine_type_of_feature(df):
    
    feature_types = []
    n_unique_values_treshold = 15
    for feature in df.columns:
        if feature != "label":
            unique_values = df[feature].unique()
            example_value = unique_values[0]
            #print(example_value)
            if (isinstance(example_value, str)) or (len(unique_values) <= n_unique_values_treshold):
                feature_types.append("categorical")
            else:
                feature_types.append("continuous")
    
    return feature_types

###########################################################################################################





def getContCatVar(feature_type,dataset):
    cont_variable=[]
    cat_variable=[]

    for column_index in range(len(feature_type)):
        if(feature_type[column_index]=="continuous"):
            cont_variable.append(dataset.columns[column_index])        
        else:
            cat_variable.append(dataset.columns[column_index])

    feature_values=[]
    feature_unq_val=[]
    for i in range(len(cont_variable)):
        feature_values.append(dataset[cont_variable[i]])
        feature_unq_val.append(dataset[cont_variable[i]].unique())
    return cont_variable,cat_variable,feature_values,feature_unq_val
    

######################################################################################################



def newvrbl_bin(dataset,cont_variable,feature_unq_val,bin_type='sqrt'):
    bin_a=0
    for i in range(len(cont_variable)):
        if bin_type=='sqrt':
            bin_a=np.sqrt(len(feature_unq_val[i]))
        else :
            if bin_type=='log':
                bin_a=np.log(len(feature_unq_val[i]))
            else:    
                bin_a=10
        dataset[cont_variable[i] + '_bin'] = pd.qcut(dataset[cont_variable[i]], int(round(bin_a,0)), labels=range(int(round(bin_a,0))))
        
        dataset[cont_variable[i] + '_bin']=dataset[cont_variable[i] + '_bin'].cat.codes
        #dataset.drop(columns=[cont_variable[i]])
        del dataset[cont_variable[i]]
    return bin_a

##########################################################################################################
"""
Create a training as well as a testing set
"""
def train_test_split_method(dataset,size):
    training_data = dataset.iloc[:int(size*len(dataset))].reset_index(drop=True)#We drop the index respectively relabel the index
    #starting form 0, because we do not want to run into errors regarding the row labels / indexes
    testing_data = dataset.iloc[int(size*len(dataset)):].reset_index(drop=True)
    return training_data,testing_data

#def vbFeature(dataset,target,target_data):
#Get all features
    feature=dataset.columns.values

    feature=feature[(feature != target)] # Remove the target variable

    data=dataset[feature] # create another dataset without target variable
    feature_type=determine_type_of_feature(data) # Get all variable type of the features

    # Function that will give categorgical, continous and values of features
    cont_variable,cat_variable,feature_values,feature_unq_val=getContCatVar(feature_type,data)

    # convert the continous variable to bin
    _=newvrbl_bin(data,cont_variable,feature_unq_val,bin_type='log')     

    # join the data with target variable
    data=data.join(target_data)   
 #   return data

#data=vbFeature(dataset,target,target_data)
training_data = train_test_split_method(data,0.7)[0]
testing_data = train_test_split_method(data,0.7)[1]

 
###########################################################################################################
 
"""
Train the tree, Print the tree and predict the accuracy
"""
start = time. time()
tree = Classification(training_data,training_data,training_data.columns[:-1],5,target)
end = time. time()
#pprint(tree)
print('Time it took to run the code: ' , round(end - start,2))
print('#'*50)

RMSE_test,Pred_test=test(testing_data,tree)
RMSE_train,Pred_train=test(training_data,tree)

      
print('Root mean square error (RMSE) of test: ',round(RMSE_test,2))
print('Root mean square error (RMSE) of train: ',round(RMSE_train,2))


##########################################################################################################
#SKlearn Outcomes
# Fit regression model
regr_1 = DecisionTreeRegressor(max_depth=5)
#regr_2 = DecisionTreeRegressor(max_depth=5)
X=[]
x,y = kf2.to_xyreg(data,target)
x_train, x_test, y_train, y_test = train_test_split(    
    x, y, test_size=0.30, random_state=42)

regr_1.fit(x_train, y_train)
y_1 = regr_1.predict(x_test)

meanSquaredError=mean_squared_error(y_test,y_1)
#print("MSE:", meanSquaredError)
rootMeanSquaredError = sqrt(meanSquaredError)
print("RMSE of test:", rootMeanSquaredError)

y_1 = regr_1.predict(x_train)

meanSquaredError=mean_squared_error(y_train,y_1)
#print("MSE:", meanSquaredError)
rootMeanSquaredError = sqrt(meanSquaredError)

print("RMSE of train:", rootMeanSquaredError)
