import json
import os
import numpy as np
import pandas as pd
import pickle as pkl

def lat_lon_to_grid_no(lat, lon, min_lat, max_lat, min_lon, max_lon):
  num_rows = np.round((max_lat - min_lat)/0.01).astype(int)
  num_cols = np.round((max_lon - min_lon)/0.01).astype(int)
  row_id_from_bottom = np.maximum(1, np.ceil((lat - min_lat)*100))
  row_id_from_bottom = np.minimum(row_id_from_bottom, num_rows) 
  col_id_from_left = np.maximum(1, np.ceil((lon - min_lon)*100))
  col_id_from_left = np.minimum(col_id_from_left, num_cols)
  grid_no = (col_id_from_left-1)*num_rows + row_id_from_bottom
  return grid_no.astype(int)

def get_num_grids(min_lat, max_lat, min_lon, max_lon):
    return (int(max_lat*1000)/10 - int(min_lat*1000)/10)*(int(max_lon*1000)/10 - int(min_lon*1000)/10)

def process_amenity_data(path, min_lat, max_lat, min_lon, max_lon):
    total_grids = get_num_grids(min_lat, max_lat, min_lon, max_lon)
    ans = [None]*total_grids
    jsons = os.listdir(path)
    added = {}

    for json_name in jsons:
        try:
            with open(path + '/' + json_name, 'r') as f:
                data = json.load(f)
            
            for result in data['results']:
                cur_location = result['geometry']['location']
                cur_lat, cur_lon = cur_location['lat'], cur_location['lng']
                if (cur_lat < min_lat or cur_lat > max_lat or cur_lon < min_lon or cur_lon > max_lon): ## Amenity out of district
                    continue
                name = result['name']
                if name in added.keys() and ((cur_lat, cur_lon) not in added[name]):
                    added[name].append((cur_lat, cur_lon))
                else:
                    added[name] = [(cur_lat, cur_lon)]
        except:
            continue

    for key in added.keys():
        temp = np.array(added[key])
        added[key] = list(temp.sum(axis=0)/temp.shape[0])
    
    for value in added.values():
        grid_number = lat_lon_to_grid_no(value[0], value[1], min_lat, max_lat, min_lon, max_lon)-1
        if ans[grid_number] == None:
            ans[grid_number] = [value]
        elif value not in ans[grid_number]:
            ans[grid_number].append(value)

    final_ans = []
    for i in range(0, total_grids):
        final_ans.append(np.array(ans[i]))

    return final_ans


def main():
    bboxes = {'bangalore': (12.64, 13.23, 77.32, 77.83), 'chandigarh': (30.66, 30.80, 76.69, 76.84), 'chennai': (12.95, 13.14, 80.16, 80.31), 'delhi': (28.40, 28.89, 76.83, 77.34), 'gurgaon': (28.20, 28.55, 76.63, 77.24), 'hyd': (17.29, 17.48, 78.38, 78.54), 'kolkata': (22.49, 22.63, 88.27, 88.41), 'mumbai': (18.89, 19.27, 72.77, 72.99)}
    CATEGORY = {'school': 'education', 'primary_school': 'education', 'bus_station': 'connectivity', 'taxi_stand': 'connectivity', 'train_station': 'connectivity', 'bank': 'govt_services', 'local_government_office': 'govt_services', 'police': 'govt_services', 'doctor': 'health', 'hospital': 'health', 'department_store': 'utilities', 'supermarket': 'utilities'}

    for DISTRICT in bboxes.keys():
        print(DISTRICT)
        min_lat = bboxes[DISTRICT][0]
        max_lat = bboxes[DISTRICT][1]
        min_lon = bboxes[DISTRICT][2]
        max_lon = bboxes[DISTRICT][3]
        TOTAL_GRIDS = get_num_grids(min_lat, max_lat, min_lon, max_lon)
        data = {'Grid_number': [i for i in range(0, TOTAL_GRIDS)]}
        for AMENITY in CATEGORY.keys():
            PATH = 'data/' + DISTRICT + '/' + CATEGORY[AMENITY] + '/' + AMENITY
            data[AMENITY] = process_amenity_data(PATH, min_lat, max_lat, min_lon, max_lon)
            
        with open('processed_data/' + DISTRICT + '.pkl', 'wb') as f:
            pkl.dump(data, f)
        df = pd.DataFrame(data, columns = data.keys())
        df.to_csv('processed_data/' + DISTRICT + '.csv', index=False)

if __name__ == "__main__":
    main()
