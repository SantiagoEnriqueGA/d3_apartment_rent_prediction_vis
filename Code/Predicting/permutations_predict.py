import pandas as pd
import geopy
import geopandas
import numpy as np
import itertools

# Getting all the permiutations of the following lists
beds = [1,2,3,4]
baths = [1,2,3,4]
square_feet = [250,500,750,1000,1250,1500,2000,2500]

permutations = list(itertools.product(beds, baths, square_feet))
len(permutations)

print("Number of permuatitons:",len(permutations))

for permutation in permutations:
    print(permutation)


# Join IRS income data
irs_data = pd.read_csv("C:/Users/sega9/Documents/GA Tech/2024.Spring/CSE 6242/Group Project/ApartmentRent/DataSource/20zpallagi.csv")
irs_data = irs_data[['STATEFIPS', 'STATE', 'zipcode', 'agi_stub', 'N1']] #Relevant cols
zip_sum = irs_data.groupby('zipcode')['N1'].sum().reset_index(name='num_returns') # Get count of returns by zip code
irs_data = pd.merge(irs_data, zip_sum, on='zipcode', how='left') # Left join back to data
irs_data['agi_stub_perc'] = irs_data['N1'] / irs_data['num_returns'] # Calculate percentage per range
irs_data_agg = irs_data.groupby(['zipcode', 'agi_stub'])['agi_stub_perc'].mean().reset_index()
reshaped = irs_data_agg.pivot(index='zipcode', columns='agi_stub', values='agi_stub_perc').reset_index()
reshaped.rename({
    1 :"perc_sub25k",
    2 :"perc_25-50k",
    3 :"perc_50-75k",
    4 :"perc_75-100k",
    5 :"perc_100-200k",
    6 :"perc_abv200k"
    }, axis='columns', inplace=True)

zipStates = irs_data.groupby(['zipcode'])['STATE'].agg(pd.Series.mode).to_frame().reset_index()
reshaped = pd.merge(reshaped, zipStates, on='zipcode', how='left') # Left join back to data


reshaped.drop(reshaped.head(1).index,inplace=True) # drop first row
reshaped.drop(reshaped.tail(1).index,inplace=True) # drop last row

### Generate ZIP Codes from Lat/Long using GeoPandas
zipcodes = geopandas.read_file("C:/Users/sega9/Documents/GA Tech/2024.Spring/CSE 6242/Group Project/ApartmentRent/DataSource/USA_Zip_Code_Boundaries/v10/zip_poly.gdb")
zipcodes = pd.DataFrame(zipcodes)
zipcodes['ZIP_CODE']=zipcodes['ZIP_CODE'].astype(int)
reshaped_zip = pd.merge(reshaped, zipcodes, left_on='zipcode', right_on='ZIP_CODE', how='left') # Left join back to data

allZipsData = reshaped_zip[[
    "zipcode",
    "perc_sub25k",
    "perc_25-50k",
    "perc_50-75k",
    "perc_75-100k",
    "perc_100-200k",
    "perc_abv200k",
    "STATE_x",
    "POPULATION",
    "POP_SQMI",
    "SQMI"
]]

# allZipsData.to_csv('C:/Users/sega9/Documents/GA Tech/2024.Spring/CSE 6242/Group Project/ApartmentRent/DataModified/permTEST.csv', encoding='utf-8')


new_rows = []

# Iterate through each row in allZipsData and add permutations as new rows
for idx, row in allZipsData.iterrows():
    for perm in permutations:
        new_row = row.copy()
        new_row['beds'], new_row['baths'], new_row['square-feet'] = perm
        new_rows.append(new_row)

# Create a new DataFrame with the new rows
allZipsPermu = pd.DataFrame(new_rows)

# Reset the index of the new DataFrame
allZipsPermu.reset_index(drop=True, inplace=True)

# Display the updated DataFrame
print(allZipsPermu)

allZipsPermu.to_csv('C:/Users/sega9/Documents/GA Tech/2024.Spring/CSE 6242/Group Project/ApartmentRent/DataModified/permTEST2.csv', 
          encoding='utf-8',
          index= False)





test = pd.read_csv('C:/Users/sega9/Documents/GA Tech/2024.Spring/CSE 6242/Group Project/ApartmentRent/DataModified/permsPredictedFIN.csv',
                   dtype={'zipcode': object})

test.head()
irs_data = pd.read_csv("C:/Users/sega9/Documents/GA Tech/2024.Spring/CSE 6242/Group Project/ApartmentRent/DataSource/20zpallagi.csv",
                       dtype={'zipcode': object})
irs_data = irs_data[['STATE', 'zipcode']] #Relevant cols
irs_data.head()

zipsToState = irs_data.groupby(['zipcode'])['STATE'].agg(pd.Series.mode).to_frame().reset_index()

zipsToState.drop(zipsToState.head(1).index,inplace=True) # drop first row
zipsToState.drop(zipsToState.tail(1).index,inplace=True) # drop last row
zipsToState

testwithstate = pd.merge(test, zipsToState, on='zipcode', how='left') # Left join back to data
testwithstate.head()

testwithstate.to_csv('C:/Users/sega9/Documents/GA Tech/2024.Spring/CSE 6242/Group Project/ApartmentRent/DataModified/permsPredictedFIN.csv', 
          encoding='utf-8',
          index= False)