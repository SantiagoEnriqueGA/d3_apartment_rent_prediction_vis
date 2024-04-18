import pandas as pd
import geopy
import geopandas


# reading APT csv file
df = pd.read_csv("C:/Users/sega9/Documents/GA Tech/2024.Spring/CSE 6242/Group Project/ApartmentRent/DataSource/apartments_for_rent_classified_100K.csv",sep=";", encoding='cp1252')
df.shape

# Drop if no Lat/Long
df = df.dropna(subset=['latitude', 'longitude'])

# Encoding/Joining ZIP Codes from Lat/Long
gdf = geopandas.GeoDataFrame(
    # df, geometry=geopandas.points_from_xy(df.latitude, df.longitude), crs="EPSG:4326"
    df, geometry=geopandas.points_from_xy(df.longitude, df.latitude), crs="EPSG:4326"
)
gdf['geometry'].head()

points = geopandas.GeoDataFrame(gdf['geometry'])
zipcodes = geopandas.read_file("C:/Users/sega9/Documents/GA Tech/2024.Spring/CSE 6242/Group Project/ApartmentRent/DataSource/USA_Zip_Code_Boundaries/v10/zip_poly.gdb")
zip_points = points.sjoin(zipcodes, how='left', )

df_wZip = df.join(zip_points)
df_wZip.rename(columns={'ZIP_CODE':'zipcode'}, inplace=True)


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

df_wZip['zipcode'] = df_wZip['zipcode'].astype(str)
reshaped['zipcode'] = reshaped['zipcode'].astype(str)
merged_data = pd.merge(df_wZip, reshaped, on='zipcode', how='left')

# Save dataset
merged_data.to_csv('C:/Users/sega9/Documents/GA Tech/2024.Spring/CSE 6242/Group Project/ApartmentRent/DataModified/merged_data.csv', encoding='utf-8')
