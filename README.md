# Urban_indicators_India
## Project Objective
For any district the distribution of various kinds of amenities like school, hospital etc. and population load on these ameni- ties decide their living standards. While, measures like total number of these amenity sites in a district are available through datasets like census of India, there isn’t any information how they are distributed in various regions of the district (especially around urban centres). Our contribution lies in using Google Places and WorldPop data to develop indicators to quantitatively compare living standards of different districts or different regions of a district. This analysis can be utilised by government for policy building, urban planners, or by citizen themselves. Various questions that this analysis answers are-
* How urbanised are the districts?
* How densely populated are the districts and different regions of the district?
* Is population distribution uniform in the districts?
* What is the distance to nearest amenity sites, both overall as a district and also in different regions of the district?
* Which cities have the worst parts that are far away from essential amenities?
* How many amenity sites are there within standard range, both overall as a district and also in different regions of the district?
* What is the Population load on amenities, both overall as a district and also in different regions of the district?

We divided cities in square grids of approximately 1 km square area and identified urbanised grids, then we used the lat- lon values of various amenity sites from Google Places to develop various accessibility and availability indicators. We then use WorldPop data which gives population at 100m x 100m granularity to analyse the population distribution in these urbanised grids and also to identify the load on amenity sites. This analysis has been done for 7 districts Bangalore, Chennai, Delhi, Gurgaon, Hyderabad, Kolkata and Mumbai. The various amenities considered by us were Education, Health, Utilities, Connectivity and Government Facilities. For more information visit - 
## Prerequisites
* WordPop to download population data of a particular area
* Following python libraries to run python scripts
	* urllib
	* urllib2
	* simplejson
	* json
	* time
	* os
	* math
	* sys
	* numpy
	* pandas
	* scipy
	* matplotlib
	* sklearn
	* pickle
	* osgeo
	* shapely

## Directory Structure
This repository contains two directories:-
* Google_Places_based_Indicators - It contains data & results for various Places based Indicators along with scripts to generate these results. Further information is in README file within this directory
* Population_Based_Indicators - It contains data & results for various Population based Indicators along with scripts to generate these results. Further information is in README file within this directory
