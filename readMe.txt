Apartment Classified 

Data Sources:
	Apt Listing Data: https://archive.ics.uci.edu/dataset/555/apartment+for+rent+classified
	GIS Zip Data: https://www.arcgis.com/home/item.html?id=8d2012a2016e484dafaac0451f9aea24
	IRS Zip Data: https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-statistics-2020-zip-code-data-soi
	USA GeoJSON Data: https://eric.clst.org/tech/usgeojson/
	US States GeoJSON Data: https://github.com/OpenDataDE/State-zip-code-GeoJSON

	
dataJoining.py -> Joins all three datasets together
	Zip codes generated on Apt Lat/Long from GIS Zip Data
	Apt data joined to IRS data on Zip	
		df before zips (99492, 22)
		df after zips  (99467, 32)
		df after IRS   (99467, 38)

dataFeatureEng.py -> Cleans data and creates dummy variables 
	Create variable for length of description
	Create Cats_Allowed and Dogs_Allowed dummy variables
	Amenities Dummy Variables
	Cityname (if less than 50 records per city set to 'Other')
	Droped rows with nulls for ['price','zipcode','perc_sub25k','bedrooms','bathrooms','POPULATION','state']
		df after (87063, 56)
	
modelCreation.ipynb -> Creates preditive models
	Linear regression model 
	XGBoost model
	XGBoost model (Tuned)
	Predicted price saved to dataset
	
aptVis - Proof of concept
	Draws all states using gz_2010_us_040_00_500k.json
	Predicted datapoints drawn with lat/long converted to pojection 
	STATES.csv converts state names to two letter codes
	
	State-zip-code-GeoJSON-master-mapshaped folder
		contains each State's geoJSON, labeled by two letter State id ex: tx_zip_codes_geo.min.geojson
		
		data converted from JSON and compressed/simplified using Mapshaper
		
	
