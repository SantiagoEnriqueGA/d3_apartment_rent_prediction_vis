import pandas as pd
import numpy as np

df = pd.read_csv('C:/Users/sega9/Documents/GA Tech/2024.Spring/CSE 6242/Group Project/ApartmentRent/DataModified/merged_data.csv', 
                 encoding='utf-8',
                 index_col=0)

df.columns
df

# Create variable for length of description
# ------------------------------------------------------------------------------------
df['description_len'] = df['body'].apply(len)

# Create Cats_Allowed and Dogs_Allowed dummy variables
# ------------------------------------------------------------------------------------
df['cats_allowed'] = df['pets_allowed'].apply(lambda x: 1 if isinstance(x, str) and 'Cats' in x else 0)
df['dogs_allowed'] = df['pets_allowed'].apply(lambda x: 1 if isinstance(x, str) and 'Dogs' in x else 0)

# Amenities Dummy Variables
# ------------------------------------------------------------------------------------
amen = pd.Series(df['amenities']).astype(str)
# Split by "," and collapse
amen = amen.str.split(",").explode()
# Keep unique values
amen_raw = pd.Series(amen).unique()
# Replace spaces for use in colnames
amen_name = pd.Series(amen_raw).str.replace(" ", "_").str.replace("/", "_")
amen_name = "has_" + amen_name
# Save colnames to add to the final DataFrame
b4 = df.columns.tolist()
# For each amenity, create new dummy variable
for i in amen_raw:
    new_col = pd.Series(df['amenities']).fillna('').str.contains(i).astype(int)
    df[i] = new_col
# Rename added columns
df.columns = b4 + amen_name.tolist()


# Cityname
# ------------------------------------------------------------------------------------
# Count occurrences of each city
city_counts = df['cityname'].value_counts()
# Identify cities with less than 50 records
less_than_50 = city_counts[city_counts < 50].index

# Set values with less than 50 records to "Other"
df.loc[df['cityname'].isin(less_than_50), 'cityname'] = 'Other'


# Price "Monthly Weekly Monthly|Weekly"
# ------------------------------------------------------------------------------------
# Display unique values in 'price_type'
df['price_type'].unique()

# Count rows where 'price_type' is 'Monthly|Weekly'
print(df[df['price_type'] == 'Monthly|Weekly'].shape[0])
# Count rows where 'price_type' is 'Weekly'
print(df[df['price_type'] == 'Weekly'].shape[0])

# only 4 records with non 'Montly' -> Drop rows where 'price_type' is 'Monthly|Weekly' or 'Weekly'
df = df[~df['price_type'].isin(['Monthly|Weekly', 'Weekly'])]


# Drop redundant Cols
# ------------------------------------------------------------------------------------
# List of columns to drop
columns_to_drop = ['category', 'amenities', 'price_type', 'pets_allowed', 'time', 
                   'currency','price_display','index_right','PO_NAME','Shape_Length',
                   'Shape_Area','has_nan','STATE']
# Drop the specified columns
df = df.drop(columns=columns_to_drop)

df.shape

# Drop empty values
df = df[df['price'].notna()]
df = df[df['zipcode'].notna()]
df = df[df['perc_sub25k'].notna()]
df = df[df['bedrooms'].notna()]
df = df[df['bathrooms'].notna()]
df = df[df['POPULATION'].notna()]
df = df[df['state'].notna()]

# Save to CSV
df.to_csv('C:/Users/sega9/Documents/GA Tech/2024.Spring/CSE 6242/Group Project/ApartmentRent/DataModified/engineered_data.csv', 
          encoding='utf-8',
          index= False)
