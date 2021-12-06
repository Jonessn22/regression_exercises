#PREPARE FUNCTION USED TO SCALE WRANGLED ZILLOW DATA TO PREPARE FOR MODELING
#    using min max scaling method

#a. imports

#b. scale
#    list columns to scale
#    create scaling object
#    fit scaling object to train data
#    transform datasets
#       transform train
#       transform validate
#       transform test

#a.IMPORTS
#******************************************************************************
import wrangle

import sklearn.preprocessing


#b. SCALE
#******************************************************************************
def scale_zillow(test, validate, train):
    
    #listing columns to scale, all excepts fips
    cols_to_scale = train.drop(columns = ['bedrooms', 'bathrooms', 'year_built', 'fips']).columns.to_list()
    
    #create scaler object
    scaler = sklearn.preprocessing.MinMaxScaler()
    
    #fit scaler object to train
    scaler = scaler.fit(train[cols_to_scale])
    
    #transform data
    scaled_train = scaler.transform(train[cols_to_scale])
    scaled_validate = scaler.transform(validate[cols_to_scale])
    scaled_test = scaler.transform(test[cols_to_scale])
    
    return scaled_train, scaled_validate, scaled_test
    