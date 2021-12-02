# FUNCTIONS TO ACQUIRE AND PREPARE ZILLOW DATA FOR EXPLORATION

>a. Imports<br>
b. `acquire_zillow` function<br>
c. `remove_outliers` function<br>
d. data visualizations<br>
- d-01. `get_hist` histograph function
- d-02. `get_box` boxplots function
> e. `prepare_zillow` function
- e-01. remove outliers
- e-02. visualizations to get distributions of numeric data
    - e-02a. `get_hist` histographs
    - e-02b. `get_box` boxplots
- e-03. convert `fips` and `year_built` columns to objects
- e-04. train/valiate/test split
- e-05. impute year using median

## Final function
`wrangle_zillow` will take in the above functions and code and return three DataFrames, prepared for exploration

