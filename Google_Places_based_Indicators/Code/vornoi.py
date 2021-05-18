from scipy.spatial import Voronoi, voronoi_plot_2d
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
np.set_printoptions(threshold=sys.maxsize)

def get_grid_info(district_name,year):
  import re
  dist_results = pd.read_csv('all_indicators/' + district_name+"_"+str(year)+"_all_indicators"+".csv")
  dist_results=dist_results.to_numpy()
  grid_type_arr=(dist_results[:,7]).reshape(dist_results.shape[0],1)
  grid_class_arr=(dist_results[:,11]).reshape(dist_results.shape[0],1)
  dist_results=dist_results[:,0:2]
  lat_coord=np.array([])
  lon_coord=np.array([])
  for i in range(dist_results.shape[0]):
    temp=re.split('\[|\]|,| ',dist_results[i,1])
    lat_coord=np.append(lat_coord,(float(temp[1])+0.005))
    lon_coord=np.append(lon_coord,(float(temp[3])+0.005))
  lat_coord=(lat_coord.reshape(lat_coord.shape[0],1))
  lon_coord=(lon_coord.reshape(lon_coord.shape[0],1))
  dist_results=dist_results[:,0].reshape(dist_results.shape[0],1)
  dist_results=np.append(dist_results,lat_coord,axis=1)
  dist_results=np.append(dist_results,lon_coord,axis=1)
  dist_results=np.append(dist_results,grid_type_arr,axis=1)
  dist_results=np.append(dist_results,grid_class_arr,axis=1)
  return dist_results

EARTH_RADIUS = 6378.137
def get_all_amenities(data, amenity, grid_numbers):
    all_amenities = np.array([[1, 2]])
    for grid_number in grid_numbers:
        arr = data[amenity][grid_number]
        if len(np.shape(arr)) != 0:
            all_amenities = np.concatenate((all_amenities, arr), axis = 0)
    return np.delete(all_amenities, (0), axis = 0)

def get_poly_area(vertices, bbox):
    lat = vertices[:, 0]
    lon = vertices[:, 1]
    area = np.radians(np.roll(lon, 1) - lon) * (2 + np.sin(np.radians(lat)) + np.sin(np.radians(np.roll(lat, 1))))
    return np.absolute(np.sum(area) * EARTH_RADIUS * EARTH_RADIUS/2.0)
    
def get_areas(vor, bbox):
    regions = vor.regions
    vertices = vor.vertices
    flag = True
    min_lat, max_lat, min_lon, max_lon = bbox[0], bbox[1], bbox[2], bbox[3]
    areas = np.array([0])
    for region in regions:
        if (len(region) == 0) or (-1 in region):
            continue
        polygon_vertices = vertices[region, :]
        lat = polygon_vertices[:, 0]
        lon = polygon_vertices[:, 1]
        if np.any(lat < min_lat) or np.any(lat > max_lat) or np.any(lon < min_lon) or np.any(lon > max_lon):
            continue
        x = get_poly_area(polygon_vertices, bbox)
        areas = np.append(areas, x)
    return np.delete(areas, (0), axis=0)
        
def main():
    PATH = '../Data/My_Code/processed_data/'
    # amenities = ['primary_school', 'train_station', 'department_store', 'supermarket', 'bank', 'school', 'police', 'doctor', 'hospital', 'local_government_office', 'taxi_stand', 'bus_station']
    bboxes = {'Bangalore': (12.64, 13.23, 77.32, 77.83), 'Chennai': (12.95, 13.14, 80.16, 80.31), 'Delhi': (28.40, 28.89, 76.83, 77.34), 'Gurgaon': (28.20, 28.55, 76.63, 77.24), 'Hyderabad': (17.29, 17.48, 78.38, 78.54), 'Kolkata': (22.49, 22.63, 88.27, 88.41), 'Mumbai': (18.89, 19.27, 72.77, 72.99)}
    categories = {'Education':['school', 'primary_school'], 'Health': ['hospital', 'doctor'], 'Connectivity': ['taxi_stand', 'bus_station', 'train_station'], 'Utilities': ['supermarket', 'department_store'], 'Govt_facilities': ['bank', 'police', 'local_government_office']}
    distrcts = []
    percentile = {category: [] for category in categories.keys()}

    for district in bboxes.keys():
        print(district)
        distrcts.append(district)
        with open(PATH + district + '.pkl', 'rb') as f:
            data = pkl.load(f)
        cur = {}
        grid_info = get_grid_info(district, '2019')
        grid_numbers = grid_info[(grid_info[:, 3] == 'Urban') | (grid_info[:, 3] =='PeriUrban'), 0]
        for category in categories.keys():
            final_amenities = np.array([[1, 2]])
            print(category)
            for amenity in categories[category]:
                cur_amenities = get_all_amenities(data, amenity, grid_numbers)
                final_amenities = np.concatenate((final_amenities, cur_amenities), axis = 0)
            try:
                vor = Voronoi(np.delete(final_amenities, (0), axis = 0))
                # fig = voronoi_plot_2d(vor, show_vertices=False, line_colors='orange', line_width=1, line_alpha=0.5, point_size=4)
                # plt.show()
                cur[category] = get_areas(vor, bboxes[district])
                percentile[category].append(np.percentile(cur[category], 80))
            except:
                print('######################## Invalid since size is ' + str(cur_amenities.shape[0]))
                cur[category] = 'Invalid since size is ' + str(cur_amenities.shape[0])
        with open('vornoi_areas_combined/' + district + '.pkl', 'wb') as f:
            pkl.dump(cur, f)
        print('')
    
    temp = {category: percentile[category] for category in categories.keys()}
    temp['District'] = distrcts
    df = pd.DataFrame(temp)
    df.to_csv('vornoi_areas_combined/80-percentile.csv')


if __name__ == "__main__":
    main()
