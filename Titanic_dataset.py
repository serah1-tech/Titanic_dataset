# Data Cleaning (Titanic_database.py)
# Step 1: Importing necessary libraries
import pandas as pd  # For data manipulation
import numpy as np   # For numerical operations
import matplotlib.pyplot as plt #For plots and visualization

# Step 2: Loading the dataset
# 'r' is used before the string to treat backslashes (\) as regular characters in the file path
file_path = r'C:\Users\User1\Downloads\Titanic-Dataset.csv'
#pd reads the csv file and loads it into pandas datafreme(table like structure)
titanic_data = pd.read_csv(file_path)


# Step 3: 
# View the first few rows of the data
print("First few rows of the dataset:")
#Prints the first five rows of the data frame.
#head() is a pandas method that returns the first five rows of the DataFrame by default, or any number of rows you specify
print(titanic_data.head(20))

# Checking the structure of the data (columns, data types, and null values)
print("\nThe structure of the data frame:")
print(titanic_data.info())

# Split the 'Name' column into 'Last Name' and 'First Name' columns
titanic_data[['Last Name', 'First Name']] = titanic_data['Name'].str.split(',', expand=True)

# Remove any extra spaces from 'First Name'
titanic_data['First Name'] = titanic_data['First Name'].str.strip()

# Example: Show the updated data
print(titanic_data[['Last Name', 'First Name']].head())


# Step 4: 
# Checking for missing values
print("\nMissing values in each column:")
#Checking for missing values in the Titanic dataset and sum up the missing values in each column
missing_values = titanic_data.isnull().sum()
#missing_values[missing_values > 0]: This filters the missing_values Series, keeping only the columns that have more than 0 missing values
print(missing_values[missing_values > 0])

#Step 5:
# Filling missing values for the 'Age' column
# The 'Age' column contains 177 missing values. Since 'Age' is a numerical column,
# filling the missing values with the median. The median is chosen because it's 
# less sensitive to outliers compared to the mean, making it a more robust option.
titanic_data['Age'] = titanic_data['Age'].fillna(titanic_data['Age'].median())

# Filling missing values for the 'Cabin' column
# The 'Cabin' column has 687 missing values, which is over 70% of the data.
# It may be problematic to drop this column due to the large number of missing values,
# will fill missing values with 'Unknown' as a placeholder. This keeps the 
# column in the dataset and allows us to retain information about passengers who 
# may or may not have had a cabin.
titanic_data['Cabin'] = titanic_data['Cabin'].fillna('Unknown')

# Filling in the missing values for the 'Embarked' column
# The 'Embarked' column has only 2 missing values, which is a small percentage of the data.
# Since 'Embarked' is a categorical variable (port of embarkation), will fill the 
# missing values with the mode (the most frequent value in the column). This is the 
# most logical choice for small gaps in categorical data.
titanic_data['Embarked'] = titanic_data['Embarked'].fillna(titanic_data['Embarked'].mode()[0])

# After handling the missing values,  check if there are any remaining missing values in the dataset.
# This will display the count of missing values for each column after the replacements.
print("\n After handling the missing values, an update on the missing values do we have: ")
print(titanic_data.isnull().sum())

# Step 6
# Checking for duplicates based on the 'PassengerId' column
print("\nDublicates in the passanger_id column")
duplicate_passenger_id = titanic_data[titanic_data.duplicated(subset=['PassengerId'])]

# Printing the duplicate rows based on 'PassengerId'
print(duplicate_passenger_id)

#Step 7
#Checking for data types
# Checking the data types of each column
print(titanic_data.dtypes)

# Step 8
# Checking for outliers in numerical columns (Age, SibSp, Parch, Fare)
numerical_columns = ['Age', 'SibSp', 'Parch', 'Fare']

# Looping through each numerical column and calculate IQR to detect outliers
for column in numerical_columns:
    # Droping missing values for the current column before calculating IQR
    data_column = titanic_data[column].dropna()
    
    Q1 = data_column.quantile(0.25)
    Q3 = data_column.quantile(0.75)
    IQR = Q3 - Q1
    
    # Defining the lower and upper bounds for the column
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Identifing  outliers
    outliers_before = titanic_data[(titanic_data[column] < lower_bound) | (titanic_data[column] > upper_bound)]
    
    # Printing the number of outliers and their percentage
    print(f"\nOutliers in the {column} column:")
    print(f"Number of outliers: {outliers_before.shape[0]}")
    print(f"Percentage of outliers: {100 * outliers_before.shape[0] / titanic_data.shape[0]:.2f}%")
    
    # Dropping the rows with outliers from the DataFrame
    titanic_data = titanic_data[(titanic_data[column] >= lower_bound) & (titanic_data[column] <= upper_bound)]
    # Identifing  outliers
    outliers_after  = titanic_data[(titanic_data[column] < lower_bound) | (titanic_data[column] > upper_bound)]
    # Printing the number of outliers and their percentage
    print(f"\nOutliers in the {column} column:")
    print(f"Number of outliers after removing the outliers: {outliers_after.shape[0]}")
# Summary statistics of the dataset
print(titanic_data.describe())
# Save the cleaned dataset to a new CSV file
titanic_data.to_csv(r'C:\Users\User1\Downloads\titanic_cleaned.csv', index=False)

      