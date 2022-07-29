# -*- coding: utf-8 -*-
"""
worry about doc strings later...

as a novice developer i hardcode assumed paths but keep them towards the top of code
can always go back and add sys arguments later

may eventually repalce with GUI?
"""
#export csv from google docs spreadsheet, save in a known location


#assumption, only doing this for one system, for now...


import os
import csv
import json

#should replace with a config file, eventually...
sys_name = 'stanton'
gdoc_export_file = 'Copy of 3.17.2-PTU Navigation Tool - 3.17.2-PTU 8121594.csv'
default_path = os.path.join(os.getcwd(), 'data','raw_input', gdoc_export_file)




new_data = []
keep_cols = [0,3,5,6,7,12]
with open(default_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        new_row = [row[x] for x in keep_cols]
        new_data.append(new_row)


#screen out anything without qt marker
stock_header = new_data[0]
adjusted_header = ['sys_name','waypoint','x','y','z','qt']

new_data = [x for x in new_data if x[-1] == 'TRUE']

out_path = os.path.join(os.getcwd(), 'data', 'app', sys_name+'.csv')

#save csv, because why not?
with open(out_path,'w') as temp:
    temp.write(','.join(adjusted_header)+'\n')
    for row in new_data:
        temp.write(','.join(row)+'\n')


#generate json file for system?

out_json = {}

for row in new_data:
    p_name = row[0].split()[0]
    marker_name = row[1]
    x,y,z = [float(x) for x in row[2:-1]]
    
    if p_name not in out_json.keys():
        out_json[p_name]={}
    out_json[p_name][marker_name]=[x,y,z]
    
json_path = os.path.join(os.getcwd(), 'data', 'app', sys_name+'.json')
with open(json_path,'w') as temp:
    temp.write(json.dumps(out_json, indent=4))
    

print('Done with data prep, should only need to do this when google doc spreadsheet is updated?')