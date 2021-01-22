# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 18:00:23 2019

@author: Vikram Bandugula
"""
# Build Decision tree from scratch
# Use both Gini and Entropy method to do it
# This is a classification example only.
import numpy as np
from numpy import array
import pandas as pd


#Data Pure



def checkInput(data):
    type_f=type(data)
    return type_f


def getDataInArray(data):
    if checkInput(data) is list:
        data=array(data)
    else :
        if checkInput(data) is pd.DataFrame:
            data = data.values
            
        else:
            data=data
    return data
    
# Convert data to array

def check_purity(data):
    label=getDataInArray(df)[:,-1]
    if len(np.unique(label))==1:
        return True
    else:
        return False

def classify_data(data):
    
    label_column = data[:, -1]
    unique_classes, counts_unique_classes = np.unique(label_column, return_counts=True)

    index = counts_unique_classes.argmax()
    classification = unique_classes[index]
    
    return classification

#Aggorithm
#I need to do it across continous and categorical variable
#I need to first identify what is categorical and what is continous
# For categorical, it's easy, just pick column=Value
#For continous, I need to get the unique values of     

def checkContinousVsCategorical(data):
    feature_type=[]
    row,column=data.shape
    for column_index in range(column-1):
    #arr_unq_val[column_index] = []
        values=data[:,column_index]
        unique_values=np.unique(values)
    #arr_unq_val[column_index]=unique_values
        if (isinstance(unique_values, str)) or (len(unique_values) <= 1):
            feature_type.append("categorical")
        else:
            feature_type.append("continuous")   
        

    return feature_type

  
    
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
    

def get_potential_splits(data):
    
    potential_splits = {}
    _, n_columns = data.shape
    for column_index in range(n_columns - 1):          # excluding the last column which is the label
        values = data[:, column_index]
        unique_values = np.unique(values)
        
        type_of_feature = FEATURE_TYPES[column_index]
        if type_of_feature == "continuous":
            potential_splits[column_index] = []
            for index in range(len(unique_values)):
                if index != 0:
                    current_value = unique_values[index]
                    previous_value = unique_values[index - 1]
                    potential_split = (current_value + previous_value) / 2

                    potential_splits[column_index].append(potential_split)
        
        # feature is categorical
        # (there need to be at least 2 unique values, otherwise in the
        # split_data function data_below would contain all data points
        # and data_above would be empty)
        elif len(unique_values) > 1:
            potential_splits[column_index] = unique_values
    
    return potential_splits

#global COLUMN_HEADERS, FEATURE_TYPES
#FEATURE_TYPES = determine_type_of_feature(df)
        
def split_data(data, split_column, split_value):
    
    split_column_values = data[:, split_column]

    type_of_feature = FEATURE_TYPES[split_column]
    if type_of_feature == "continuous":
        true_data = data[split_column_values <= split_value]
        false_data = data[split_column_values >  split_value]
    
    # feature is categorical   
    else:
        true_data = data[split_column_values == split_value]
        false_data = data[split_column_values != split_value]
    
    return true_data, false_data


def calculate_entropy(data):
    
    label_column = data[:, -1]
    _, counts = np.unique(label_column, return_counts=True)

    probabilities = counts / counts.sum()
    entropy = sum(probabilities * -np.log2(probabilities))
     
    return entropy

def calculate_overall_entropy(true_data, false_data):
    
    n = len(true_data) + len(false_data)
    p_true_data = len(true_data) / n
    p_false_data = len(false_data) / n

    overall_entropy =  (p_true_data * calculate_entropy(true_data) 
                      + p_false_data * calculate_entropy(false_data))
    
    return overall_entropy

def class_counts(rows):
    """Counts the number of each type of example in a dataset."""
    counts = {}  # a dictionary of label -> count.
    for row in rows:
        # in our dataset format, the label is always the last column
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

def gini(rows):
    """Calculate the Gini Impurity for a list of rows.

    There are a few different ways to do this, I thought this one was
    the most concise. See:
    https://en.wikipedia.org/wiki/Decision_tree_learning#Gini_impurity
    """
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        #print (lbl)
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity

def info_gain(left, right, current_uncertainty):
    """Information Gain.

    The uncertainty of the starting node, minus the weighted impurity of
    two child nodes.
    """
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)

#current_uncertainty = gini(data)




  

def determine_best_split_entropy(data, potential_splits):
    
    overall_entropy = 9999
    for column_index in potential_splits:
        for value in potential_splits[column_index]:
            data_below, data_above = split_data(data, split_column=column_index, split_value=value)
            current_overall_entropy = calculate_overall_entropy(data_below, data_above)

            if current_overall_entropy <= overall_entropy:
                overall_entropy = current_overall_entropy
                best_split_column = column_index
                best_split_value = value
    
    return best_split_column, best_split_value


def determine_best_split_gini(data, potential_splits):
    current_uncertainty = gini(data)
    #overall_entropy = 9999
    best_gain = 0
    for column_index in potential_splits:
        for value in potential_splits[column_index]:
            data_below, data_above = split_data(data, split_column=column_index, split_value=value)
            gain = info_gain(data_below, data_above,current_uncertainty)

            if gain >= best_gain:
                best_gain = gain
                best_split_column = column_index
                best_split_value = value
    
    return best_split_column, best_split_value



def decision_tree_algorithm(df, counter=0, min_samples=2, max_depth=5,method='CART'):
    
    # data preparations
    if counter == 0:
        global COLUMN_HEADERS, FEATURE_TYPES
        COLUMN_HEADERS = df.columns
        FEATURE_TYPES = determine_type_of_feature(df)
        data = df.values
    else:
        data = df           
    
    
    # base cases
    if (check_purity(data)) or (len(data) < min_samples) or (counter == max_depth):
        classification = classify_data(data)
        
        return classification

    
    # recursive part
    else:    
        counter += 1

        # helper functions 
        potential_splits = get_potential_splits(data)
        if method=="CART":
            split_column, split_value = determine_best_split_gini(data, potential_splits)
        else :
            split_column, split_value = determine_best_split_entropy(data, potential_splits)
            
        data_below, data_above = split_data(data, split_column, split_value)
        
        # determine question
        feature_name = COLUMN_HEADERS[split_column]
        type_of_feature = FEATURE_TYPES[split_column]
        if type_of_feature == "continuous":
            question = "{} <= {}".format(feature_name, split_value)
            
        # feature is categorical
        else:
            question = "{} = {}".format(feature_name, split_value)
        
        # instantiate sub-tree
        sub_tree = {question: []}
        
        # find answers (recursion)
        yes_answer = decision_tree_algorithm(data_below, counter, min_samples, max_depth)
        no_answer = decision_tree_algorithm(data_above, counter, min_samples, max_depth)
        
        # If the answers are the same, then there is no point in asking the qestion.
        # This could happen when the data is classified even though it is not pure
        # yet (min_samples or max_depth base case).
        if yes_answer == no_answer:
            sub_tree = yes_answer
        else:
            sub_tree[question].append(yes_answer)
            sub_tree[question].append(no_answer)
        
        return sub_tree

def classify_example(example, tree):
    question = list(tree.keys())[0]
    feature_name, comparison_operator, value = question.split(" ")

    # ask question
    if comparison_operator == "<=":
        if example[feature_name] <= float(value):
            answer = tree[question][0]
        else:
            answer = tree[question][1]
    
    # feature is categorical
    else:
        if str(example[feature_name]) == value:
            answer = tree[question][0]
        else:
            answer = tree[question][1]

    # base case
    if not isinstance(answer, dict):
        return answer
    
    # recursive part
    else:
        residual_tree = answer
        return classify_example(example, residual_tree)


def calculate_accuracy(df, tree):

    df["classification"] = df.apply(classify_example, args=(tree,), axis=1)
    df["classification_correct"] = df["classification"] == df["label"]
    
    accuracy = df["classification_correct"].mean()
    
    return accuracy


training_data = [
    ['Green', 3, 'Pear'],
    ['Green', 2, 'Pear'],
    ['Red', 5, 'Apple'],
    ['Red', 3, 'Apple'],
    ['Green', 6, 'Apple']
]
header = ["color", "diameter", "label"]

#Convert list to pandas
df=pd.DataFrame(training_data,columns=header)
data=getDataInArray(df)

tree = decision_tree_algorithm(df, max_depth=3)
example = df.iloc[0]   
classify_example(example,tree) 

accuracy = calculate_accuracy(df, tree)
accuracy