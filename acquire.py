# Functions to acquire Telco data

# ******ignore warnings
import warnings
warnings.filterwarnings("ignore")


import numpy as np
import pandas as pd
from scipy import stats
import os


# ******files/data
from pydataset import data
import env
# import acquire
# import prepare


# ******visualizations
import matplotlib.pyplot as plt
import seaborn as sns


# ******sklearn
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# -------------------------------------
# Part I | Input Functions
# these two functions will be inputs for the main acquire_telco_data() function

def get_connection(db, user = env.user, host = env.host, password = env.password):
    '''
    This function takes in login credentials from env file as an arguments and will be used to establish a 
    connection to Codeup Database by returning a connection URL.
    
    This will be the first of two input functions for our final acquire_telco_data function.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

    
def new_telco_data():
    '''
    This function will store the sequel query that will be used, along with the get_connection function, 
    to read the telco data into a DataFrame, storing that DataFrame
    
    This will be the second of two input functions for our final acquire_telco_data function.
    ''' 
    
#   creating the variable that will hold the code used to query the Codeup database    
    sql_query = '''select * from customers 
                    join contract_types using (contract_type_id) 
                    join internet_service_types using (internet_service_type_id) 
                    join payment_types using (payment_type_id)'''
    
#   using the get_connection() function and sql_query to read in DataFrame from Codeup database
    df = pd.read_sql(sql_query, get_connection('telco_churn'))
    
    return df

# -------------------------------------
# Part II | Main Acquire Function

def acquire_telco_data():
    '''
    This is the main acquire_telco_data function that checks to see if a local csv for telco data exists.
        If it does it will write the csv data into a DataFrame
            (else)
        If the telco data csv file does not exist locally, it will use the input function new_telco_data to 
        query the Codeup database and return the query as DataFrame .
            It will then cache the DataFrame and create local csv file. 
    '''
    if os.path.isfile('telco_data'):
#   if csv file already exists in local directory, this code will run

        df = pd.read_csv('telco_data', index_col = 0)
#       this line of code reads the telco csv file into a Database

    else:
#   if csv file does not exist in local directory, this code will run instead

        df = new_telco_data()
#       this line of code reads telco database into a DataFrame using the input function new_telco_data

        df.to_csv('telco_data.csv')
#       this line of code caches the telco data, creating a local csv file

    return df

# -------------------------------------
# Next step 02 Prepare (see prepare.py)