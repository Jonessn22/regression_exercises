# WRANGLE FUNCTIONS TO ACQUIRE AND PREPARE ZILLOW DATA FOR EXPLORATION

#a. Imports

#b. acquire_zillow function

#c. remove_outliers function

#d. data visualizations
#    d-01. get_hist histograph function
#    d-02. get_box boxplots function

#e. prepare_zillow function
#    e-01. remove outliers
#    e-02. visualizations to get distributions of numeric data
#        e-02a. get_hist histographs
#        e-02b. get_box boxplots
#    e-03. convert fips and year_built columns to objects
#    e-04. train/valiate/test split
#    e-05. impute year using median
#

### FiINAL FUNCTION
#wrangle_zillow will take in the above functions and code and return three DataFrames, prepared for exploration

#a.IMPORTS
#******************************************************************************
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

from env import user, password, host

import warnings
warnings.filterwarnings('ignore')

#b.ACQUIRE_ZILLOW FUNCTION
#******************************************************************************
def acquire_zillow():
    '''
    This function acquires Zillow data from Codeup SQL database, by supplying the credentials to access the 
    database and then running the SQL query that will retrieve the selected data. 
    
    It will read the queried data into a returned pandas DataFrame.
    '''
    
    url = f'mysql+pymysql://{user}:{password}@{host}/zillow'
    query = '''SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, 
                      taxvaluedollarcnt, yearbuilt, taxamount, fips
               FROM properties_2017
               WHERE propertylandusetypeid = 261;'''

    #read queried data into DataFrame
    df = pd.read_sql(query, url)
    
    #rename columns
    df.rename(columns = {'bedroomcnt': 'bedrooms',
                         'bathroomcnt': 'bathrooms',
                         'calculatedfinishedsquarefeet': 'sqft',
                         'taxvaluedollarcnt': 'tax_value',
                         'yearbuilt': 'year_built',
                         'taxamount': 'tax_amt',
                         'fips': 'fips'}, inplace = True)
    return df
    
#c.REMOVE_OUTLIERS FUNCTION
#******************************************************************************
def remove_outliers(df, k, col_list):
    '''
    This function removes outliers from a the col_list list of columns in a dataframe, returning
    a dataframe with the outlier records removed
    '''
    
    for col in col_list: 
        
        #get quartiles
        q1, q3 = df[col].quantile([.25, .75])
        
        #calculate interquartile range (IQR)
        iqr = q3 - q1
        
        #get upper and lower bounds
        upper_bound = q3 + k * iqr
        lower_bound = q1 - k * iqr
        
        #dataframe without outliers
        df = df[(df[col] > lower_bound) & (df[col] < upper_bound)]
        
    return df

#d.DATA VISUALIZATIONS
#***************************************S***************************************
def get_hist(df):
    '''
    This function takes in a DataFrame and returns histograms for each of the continuous variables
    '''
    
    plt.figure(figsize = (16, 3))
    
    #list of columns
    cols = [col for col in df.columns if col not in ['fips', 'year_built']]
    
    for i, col in enumerate(cols):
        
        #i starts at 0, but plot numbers should start at 1
        plot_number = i + 1
        
        #create subplot
        plt.subplot(1, len(cols), plot_number)
        
        #title with column names
        plt.title(col)
        
        #display histogram for column
        df[col].hist(bins = 5)
        
        #hide gridlines
        plt.grid(False)
        
        #turn off sci method
        plt.ticklabel_format(useOffset = False)
        
        plt.tight_layout()
        
    plt.show()
    
    
def get_box(df):
    
    '''
    This function takes in a DataFrame and returns boxplots for each of the continuous variables
    '''
    
    plt.figure(figsize = (16, 3))
    
    #list of columns
    cols = [col for col in df.columns if col not in ['fips', 'year_built']]    
    
    for i, col in enumerate(cols):
        
        #i starts at 0, but plot numbers should start at 1
        plot_number = i + 1
        
        #create subplot
        plt.subplot(1, len(cols), plot_number)
        
        #title with column names
        plt.title(col)
        
        #display boxplots for column
        sns.boxplot(data = df[[col]])
        
        #hide gridlines
        plt.grid(False)
        
        #set proper spacing between plots
        plt.tight_layout()
        
    plt.show()
    

#e.PREPARE_ZILLOW FUNCTION
#******************************************************************************
def prepare_zillow(df):
    '''
    Function takes in dataframe and prepares for exploration using the prior functions
    '''
    
    #removing outliers
    df = remove_outliers(df, 1.5, acquire_zillow().columns)
    
    #get distributions of numeric data
    get_hist(df)
    get_box(df)
    
    #converting column datatypes
    df.fips = df.fips.astype(object)
    df.year_built = df.year_built.astype(object)
    
    #train/validate/test split
    train_validate, test = train_test_split(df, test_size = .2, random_state = 123)
    train, validate = train_test_split(train_validate, test_size = .3, random_state = 123)
    
    #impute year built using median
    imputer = SimpleImputer(strategy = 'median')
    
    imputer.fit(train[['year_built']])
    
    train[['year_built']] = imputer.transform(train[['year_built']])
    validate[['year_built']] = imputer.transform(validate[['year_built']])
    test[['year_built']] = imputer.transform(test[['year_built']])
    
    return train, validate, test
    

### FiINAL FUNCTION
#******************************************************************************
def wrangle_zillow():
    '''
    This function consolidates the above functions, acquiring and preparing data from Zillow db for exploration.
    '''
    
    train, validate, test = prepare_zillow(acquire_zillow())
    
    return train, validate, test

