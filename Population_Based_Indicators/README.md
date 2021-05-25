# Urban_indicators_India

## Project Objective
Use the Google Places Data and World Pop Data to obtain various Livability parameters.

## Directory Structure
* Input_Data - contains pre processed data for the 7 districts for which we obtained results
* Results - contains population based indicator results for the 7 districts

* Code

### Obtaining Population Based Indicators
The code uses "DistrictName_year_all_indicators.csv", "district_coordinates.csv" & "DistrictName.pkl" files to generate various Google Places based indicators.

To run the code follow these steps:

* The WorldPop data being too big is stored on MTP drive. Link to dataset is - https://drive.google.com/file/d/1uCh1amKcQ9zjYZBFY65E09MXHICG2uA1/view?usp=sharing

* Create a Google Collab notebook (with MTP drive credentials) and paste the code from "population_based_indicators.py" into it
* Replace line 13 of code where its written {cd 'drive/My Drive/Data/Population_Based_Indicators'}, with {cd 'path_to_worldpop_data_in_MTP_drive'}
* Place "DistrictName_year_all_indicators.csv", "district_coordinates.csv" & "DistrictName.pkl" files in the same directory as WorldPop data
* Enter bounding box lat-lon for the district concerned in "district_coordinates.csv"
* Enter name of district in "districts" list for the district you want to obtain the results, similarly modify "category_dict" dictionary which contains combined category name as key and their obtained parameters as value. Also modify "year" variable as per the need
* Run collab code to obtain various indicators
* Result csv files will be created within the same directory on google drive
