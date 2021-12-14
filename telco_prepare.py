# Functions to prepare Telco data for exploration and modeling

import pandas as pd 
import numpy as np

from sklearn.model_selection import train_test_split

import pandas as pd

# This function will feed into our main prep_telco function

def split_telco(df):
    '''
    This function takes in as arguments cleaned DataFrame and a random seed and splits the cleaned DataFrame,
    first into two samples, train_and_validate (80%) and test (20%). It stratifies the split on our target variable
    ----> churn. It then splits the train_and_validate into train (70% of the 80%, 56% of total) and validate 
    (30% of the 80%, 24% of the total). again, stratifying on churn.
    The function returns x3 DataFrames, train, validate, and test.
    
    This function is fed into our main prep_telco function.
    '''
    
    train_validate, test = train_test_split(
                                        df, 
                                        test_size = 0.2, 
                                        random_state = 123, 
                                        stratify = df.churn)
    
    train, validate = train_test_split(
                                        train_validate,
                                        test_size = 0.3,
                                        random_state = 123,
                                        stratify = train_validate.churn)
    
    return train, validate, test

# --------------------------------------------------------------------
# Main Clean and Split Function

def prep_telco(df):
    '''
    This function takes in the raw DataFrame as an argument and returns a cleaned, split DataFrame, performing the following cleaning actions:
    a. Drop unecessary columns
    b. Map binary, yes/no to 1/0
    c. Map gender column male/female to 1/0
    d. split the data

    '''
    
#                                       a. drop unnecessary columns
    df.drop(columns = ['total_charges', 'customer_id', 'multiple_lines', 'online_security', 'online_backup', 'device_protection', 
                    'streaming_tv', 'tech_support', 'streaming_movies',  'contract_type', 'internet_service_type','payment_type'], 
                    inplace = True)

#                                       b. map binary, yes/no columns
    float_cols = [] #creating empty list to hold floats
    int_cols = [] #creating empty list to hold ints
    obj_cols = [] #creating empty list to hold objects

    for col in df.columns: #for loop to cycle through each df column and add to list according to dtype
        if df[col].dtype == 'float64':
            float_cols.append(col)
        elif df[col].dtype == 'int64':
            int_cols.append(col)
        else:
            obj_cols.append(col)

    obj_cols.remove('gender') #will encode gender separately since no yes/no value

    for col in obj_cols: #the for loop that will map the yes/no columns
        df[col] = df[col].map({'Yes': 1, 'No': 0})

#                                    c. map gender column
    df.gender = df.gender.map({'Male': 1, 'Female': 0}) #to map gender

#                                    d. split the data
    train, validate, test = split_telco(df)
    
    

    return train, validate, test



