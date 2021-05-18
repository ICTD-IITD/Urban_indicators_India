import urllib
import urllib2
import simplejson
import json
import time
import os
import math
import sys

TOTAL_REQUESTS = int(sys.argv[1])
INITIAL_REQUESTS = 4299
with open('api_key.txt', 'r') as f:
    API_KEY = f.readline().strip()

bboxes = {'bangalore': (12.64, 13.23, 77.32, 77.83), 'chandigarh': (30.66, 30.80, 76.69, 76.84), 'chennai': (12.95, 13.13, 80.17, 80.31), 'delhi': (28.40, 28.89, 76.83, 77.34), 'gurgaon': (28.20, 28.55, 76.63, 77.24), 'hyd': (17.29, 17.48, 78.38, 78.54), 'kolkata': (22.49, 22.63, 88.27, 88.41), 'mumbai': (18.89, 19.27, 72.77, 72.99)}
sides = {'bus_station': 3, 'taxi_stand':3, 'train_station': 4, 'primary_school': 2, 'school': 2, 'bank': 2, 'local_government_office': 2, 'police': 2, 'hospital': 2, 'doctor': 2, 'department_store': 4, 'supermarket': 2}

def make_request_google_places(lat,lng,category,api_key,rankby,radius=None):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    values = {'key' : api_key,
              'location' : lat+','+lng,
              'type' : category,
              'language' : 'en'
              }
    if rankby == 'prominence':
       values['radius'] = radius
    else:
       values['rankby'] = 'distance'

    arguments = urllib.urlencode(values)
    req = urllib2.Request(url+arguments)
    response = simplejson.load(urllib2.urlopen(req))
    if not response['status'] == "OK":
        #print '%s' %response
        raise Exception(response['status'])
    return response

def make_request_google_places_nextpage(api_key, nextpagetoken):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    values = {'key' : api_key,
              'pagetoken': nextpagetoken
              }

    arguments = urllib.urlencode(values)
    req = urllib2.Request(url+arguments)
    response = simplejson.load(urllib2.urlopen(req))
    if not response['status'] == "OK":
        #print '%s' %response
        raise Exception(response['status'])
    return response

def make_request(API_KEY, path, lat = '', lng = '', amenity = '', nextpage = False, nextpagetoken = '', rankby='prominence', radius='1414'):
    global TOTAL_REQUESTS
    try:
        if TOTAL_REQUESTS - INITIAL_REQUESTS > 4900:
            print(str(TOTAL_REQUESTS - INITIAL_REQUESTS) + ' requests made. Stopping the program')
            exit()
        TOTAL_REQUESTS +=1
        if not nextpage:
            res = make_request_google_places(lat, lng, amenity, API_KEY, rankby, radius = radius)
        else:
            print('NEXT PAGE. WAIT FOR 5 SEC')
            time.sleep(5)
            print('RESUMED')
            res = make_request_google_places_nextpage(API_KEY, nextpagetoken)
        with open(path, 'w') as f:
            json.dump(res, f)
        return res
    except Exception,detail:
        error =  str(detail)
        print '%s' % error
        if error.__contains__('INVALID_REQUEST'):
            raise Exception(error)
        elif error.__contains__('OVER_QUERY_LIMIT') and  error.__contains__('REQUEST_DENIED'):
            print('QPS EXCEEDED. WAITING FOR 5 MINS')
            time.sleep(300)
            print('RESUMED')
        elif error.__contains__('HTTP Error 500: Internal Server Error'):
            print('INTERNAL SERVER ERROR')
        elif error.__contains__('urlopen error [Errno -2]'):
            print("URL OPEN ERROR")
    return {'status':'INVALID'}


def fetch_data(district, address, amenity, API_KEY, side):
    min_lat, max_lat = int(bboxes[district][0]*1000)/10, int(bboxes[district][1]*1000)/10
    min_lon, max_lon = int(bboxes[district][2]*1000)/10, int(bboxes[district][3]*1000)/10
    center_list = []
    lat_lim = max_lat + (not (max_lat-min_lat)%side==0)*(side-(max_lat-min_lat)%side)
    lon_lim = max_lon + (not (max_lon-min_lon)%side==0)*(side-(max_lon-min_lon)%side)
    radius = str(int(float(side*math.sqrt(2))/2.0*1000))
    cur_lon = float(min_lon) + float(side)/2.0
    while(cur_lon<lon_lim):
        cur_lat = float(min_lat) + float(side)/2.0
        while (cur_lat<lat_lim):
            center_list.append((str(float(cur_lat)/100.0), str(float(cur_lon)/100.0)))
            cur_lat += float(side)
        cur_lon = cur_lon + float(side)
    n = 0
    file_name = 0
    print('##################  '+str(len(center_list))+' GRIDS ARE PRESENT   ####################')
    while(n<len(center_list)):
        for i in range(n, min(n+50, len(center_list))):
            res = make_request(API_KEY, address + '/'+ str(file_name)+ '.json',lat = center_list[i][0], lng = center_list[i][1], amenity = amenity, radius=radius)
            if not res['status'] == 'INVALID':
                file_name+=1
            ####################################################
            if res.get('next_page_token'):
                nextpagetoken = res['next_page_token']
                res = make_request(API_KEY, address + '/'+ str(file_name)+ '.json', nextpage=True, nextpagetoken=nextpagetoken)
                if not res['status'] == 'INVALID':
                    file_name+=1
            ####################################################
            if res.get('next_page_token'):
                nextpagetoken = res['next_page_token']
                res = make_request(API_KEY,address + '/'+ str(file_name)+ '.json', nextpage=True, nextpagetoken=nextpagetoken)
                if not res['status'] == 'INVALID':
                    file_name+=1
        print('##################  '+str(min(n+50, len(center_list))) + '/' + str(len(center_list))+' GRIDS PROCESSED. WAITING FOR 2 SECS  ####################')
        time.sleep(2)
        print('RESUMED')
        n+=50
               

DISTRICT = 'kolkata'
CATEGORY = 'utilites'
AMENITY = ['supermarket', 'department_store']

for x in AMENITY:
    PATH = 'data/' + DISTRICT + '/' + CATEGORY + '/' + x
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    fetch_data(DISTRICT, PATH, x, API_KEY, sides[x])

print('Total ' + str(TOTAL_REQUESTS) + ' requests have been made')
