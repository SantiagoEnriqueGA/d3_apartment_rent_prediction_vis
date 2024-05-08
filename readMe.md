## Apartment Classifieds Prediction and Visualization

#### Overview/Goal
This project focuses on predicting apartment prices and visualizing data related to apartment listings. It combines various datasets to create predictive models and interactive visualizations using geographic and demographic information. Many models were tested including a using custom random forest implementation, XGBoost, as well as H2O autoML. The final dashboard is built in javascript using D3.

#### Data Sources
- **Apt Listing Data:** [UCI Apartment Listing Dataset](https://archive.ics.uci.edu/dataset/555/apartment+for+rent+classified)
- **GIS Zip Data:** [ArcGIS Zip Data](https://www.arcgis.com/home/item.html?id=8d2012a2016e484dafaac0451f9aea24)
- **IRS Zip Data:** [IRS Individual Income Tax Statistics](https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-statistics-2020-zip-code-data-soi)
- **USA GeoJSON Data:** [US GeoJSON Data](https://eric.clst.org/tech/usgeojson/)
- **US States GeoJSON Data:** [State-zip-code-GeoJSON](https://github.com/OpenDataDE/State-zip-code-GeoJSON)

#### Key Files
- **dataJoining.py:** Joins all three datasets together, generates zip codes based on apartment latitude/longitude, and joins apartment data with IRS data based on zip codes.
- **dataFeatureEng.py:** Cleans data and creates dummy variables such as length of description, Cats_Allowed and Dogs_Allowed flags, amenities dummy variables, city names (grouping cities with less than 50 records as 'Other'), and drops rows with null values for specific columns. The resulting dataset size is (87063, 56).
- **modelCreation.ipynb:** Creates predictive models including linear regression and XGBoost models. The predicted prices are saved back to the dataset.
- **aptVis.html:** A proof-of-concept interactive visualization tool using D3.js. It draws all states and zip codes using GeoJSON data, displays predicted apartment data points with latitude/longitude converted to projection, and allows user input to predict apartment prices based on various features such as zip code, bedrooms, bathrooms, square footage, parking, and pets.

#### How to Use
1. Clone the repository and set up the required dependencies.
2. Run `dataJoining.py` to combine the datasets and generate zip codes.
3. Execute `dataFeatureEng.py` to clean the data and create dummy variables.
4. Open and run `modelCreation.ipynb` to build predictive models and save predicted prices.
5. Launch `aptVis.html` in a web browser to interact with the visualization tool. Enter the necessary inputs to predict apartment prices based on selected criteria.

#### Screenshot
![127 0 0 1_5500_Code_Visual_aptVisFull html (2)](https://github.com/SantiagoEnriqueGA/d3_apartment_rent_prediction_vis/assets/50879742/7ed87ad8-c643-4608-ad89-fafc3b797acd)

