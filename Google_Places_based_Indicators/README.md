# Urban_indicators_India

## Project Objective
Use the Google Places Data and World Pop Data to obtain various Livability parameters.

## Directory Structure
* Input_Data - contains pre processed data for the 7 districts for which we obtained results
* Raw_Data - contains raw json data for the 7 districts we worked upon
* Results - contains google places based indicator results for the 7 districts

* Code

### Raw Data Extraction
The code generates HTTP Request on places API which takes type of category, centre and radius as input and returns the data of that type of amenities present in the circular region including their latitude and longitude.
To run the code, set the following variables in the code
bboxes-dictionary of bounding box lat lon(value) of the district(key)
DISTRICT string
CATEGORY string 
AMENITIES list of type of amenities under $CATEGORY$

After setting these variables run places_data_extraction.py

It then saves the results in ./data/$DISTRICT$/$CATEGORY$/$AMENITY$ folder as json files.
Also keep the api key in ./api_key.txt in the cwd

### Preprocessing Raw Data
This script processes the raw data and generates pkl and csv files for each district which is essentially a dictionary that contains key as the type of AMENITY and its value is a list such that i-th entry of list is a nx2 numpy array which are the lat lon of amenities (of type AMENITY) of each of n amenities present in grid number i

To run the code, set the variables "bboxes" and "CATEGORY" accordingly. it assumes the directory structure as created by the file "places_dataextraction.py". Then run preprocess_places_data.py

### Generating Places Based Indicators
The code uses "DistrictName_year_all_indicators.csv", "district_coordinates.csv" & "DistrictName.pkl" files to generate various Google Places based indicators.
To run the code:
* Place "DistrictName_year_all_indicators.csv", "district_coordinates.csv" & "DistrictName.pkl" files in the same directory as places_indicator.py
* Enter bounding box lat-lon for the district concerned in "district_coordinates.csv"
* Enter name of district in "districts" list for the district you want to obtain the results, similarly modify "category_dict" dictionary which contains combined category name as key and various amenities in that category as value. Also modify "year" variable as per the need
* Run places_indicator.py to obtain various indicators
* Result csv files will be created within the same directory

### Generating Voronoi Result
This script generates the voronoi diagram for each amenity in the district and then saves 80 percentile of the areas for each amenity for each district. We considered amenities only in urban and peri urban grids to generate the voronoi diagram. It takes indicators csv file as input to filter out only urban and peri urban grids and the processed pkl to take lat lon of the amenities present in the grids of the district. Appropriate path variables should be set for these files to take the input.