import pandas as pd
import itertools

# Existing DataFrame (sample data for illustration)
allZipsData = pd.DataFrame({
    'zipcode': [1001, 1002, 1005],
    'perc_sub25k': [0.272532, 0.296559, 0.257028],
    'perc_25-50k': [0.246781, 0.209514, 0.232932],
    'perc_50-75k': [0.182403, 0.122470, 0.164659],
    'perc_75-100k': [0.114807, 0.081984, 0.128514],
    'perc_100-200k': [0.153433, 0.189271, 0.192771],
    'perc_abv200k': [0.030043, 0.100202, 0.024096],
    'POPULATION': [16979.0, 35703.0, 5619.0],
    'POP_SQMI': [1405.55, 615.25, 126.50],
    'SQMI': [12.08, 58.03, 44.42]
})

# Permutations
beds = [1, 2, 3, 4]
baths = [1, 2, 3, 4]
square_feet = [250, 500, 750, 1000, 1250, 1500, 2000, 2500]

permutations = list(itertools.product(beds, baths, square_feet))
len(permutations)
# Create a list to hold the new rows
new_rows = []

# Iterate through each row in allZipsData and add permutations as new rows
for idx, row in allZipsData.iterrows():
    for perm in permutations:
        new_row = row.copy()
        new_row['beds'], new_row['baths'], new_row['square-feet'] = perm
        new_rows.append(new_row)

# Create a new DataFrame with the new rows
new_allZipsData = pd.DataFrame(new_rows)

# Reset the index of the new DataFrame
new_allZipsData.reset_index(drop=True, inplace=True)

# Display the updated DataFrame
print(new_allZipsData)
