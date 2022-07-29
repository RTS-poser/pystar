# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 14:31:08 2022

@author: Richard
"""

import json
import numpy as np
import star_lib as starlib


with open('Lake Survey 2.json','r') as temp:
    data = json.loads(temp.read())
    
csv_header = ['way_point','x_deg','y_deg','num_anchors']
csv_data = [csv_header]
for key in data:
    csv_row = [key, data[key]['dec_degrees'][0],data[key]['dec_degrees'][1],len("anchor_name")]
    # print(csv_row)
    csv_data.append([str(x) for x in csv_row])


with open('microtech.json','r') as temp:
    data2 = json.loads(temp.read())
    
csv_header2 = ['ref_point','x_deg','y_deg']
csv_data2 = [csv_header2]

for key in data2:
    if key in ['microTech','OM-1','OM-2']:
        continue
    x_deg, y_deg = starlib.xyz_to_degrees(data2[key])
    print(key,x_deg,y_deg)
    csv_row2 = [key, x_deg, y_deg]
    csv_data2.append([str(x) for x in csv_row2])




with open('lake_survey_2.csv','w') as temp:
    for row in csv_data:
        temp.write(','.join(row)+'\n')

# with open('reference_points.csv','w') as temp:
#     for row in csv_data2:
#         temp.write(','.join(row)+'\n')

#full pu nav guide???
path_1 = r'D:\Data\StarCitizen\PU Nav Guide.csv'

#--------------------------------------
#patch code
in_file = r'D:\Data\StarCitizen\PU Nav Guide.csv'
import csv
keep_cols = [0,3,5,6,7,12]
new_data = []

# with open(in_file) as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         new_row = [row[x] for x in keep_cols]
#         try:
#             if new_row[0].lower().split()[0] == 'microtech':
#                 new_data.append(new_row)
#         except:
#             pass

new_data = [x for x in new_data if x[-1] != 'TRUE'][1:]

csv_header3 = ['ref_point','x_deg','y_deg']
csv_data3 = [csv_header2]

for row in new_data:
    try:
        name_id = row[1]
        x = float(row[2])*1000
        y = float(row[3])*1000
        z = float(row[4])*1000
        
        x_deg, y_deg = starlib.xyz_to_degrees([x,y,z])
        
        new_row = [name_id, x_deg, y_deg]
        
        csv_data3.append([str(x) for x in new_row])
    except:
        print('failed:\t',row)
#--------------------------------------

# with open('off_grid_places.csv','w') as temp:
#     for row in csv_data3:
#         temp.write(','.join(row)+'\n')
        
        
print('done!')