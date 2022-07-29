# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:53:22 2022
@author: watso330
"""


print(r'''https://gis.stackexchange.com/questions/14731/how-do-i-specify-a-crs-for-a-fictional-game-map-in-qgis
      
      https://www.reddit.com/r/QGIS/comments/lw96ix/crs_for_a_fictional_planet_map_raster_custom_crs/
      
      
      https://www.cartographersguild.com/showthread.php?t=32309
      
      ''')

print('\n\nsee above for link to custom crs\n\n')

from PyQt5.QtWidgets import (QApplication, QMainWindow, QCompleter, QTableWidgetItem, QHeaderView)
from PyQt5.uic import loadUi
from add_anchor_form import Ui_MainWindow
import sys
from PyQt5.QtCore import Qt

import numpy as np

import json
#load local data files
with open('microtech.json','r') as temp:
    anchor_points = json.loads(temp.read())


import star_lib as starlib

session_data = {}

quantum_data = {}

for key, value in anchor_points.items():
    quantum_data[key]={}
    quantum_data[key]['xyz']=value
    np_xyz = np.array(value)
    dec_degrees = starlib.xyz_to_degrees(value)
    quantum_data[key]['dec_degrees']=dec_degrees



class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        
        #auto complete logic/demo
        #https://pythonbasics.org/pyqt-auto-complete/
        

        completer = QCompleter(starlib.names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        #completer.setCompletionMode(QCompleter.InlineCompletion)
        self.txt_q_marker.setCompleter(completer)
        
        
        #init table?
        
        
        self.tbl_anchor_points.setRowCount(1)
        self.tbl_anchor_points.setColumnCount(2)
        
        self.tbl_anchor_points.setItem(0,0,QTableWidgetItem('Marker Name'))
        self.tbl_anchor_points.setItem(0,1,QTableWidgetItem('Distance'))
        
        self.change_cbo_orig_type()
        self.change_cbo_dest_type()
        
    def reset_table(self):
        #init the table?
        self.tbl_anchor_points.setRowCount(1)
        self.tbl_anchor_points.setColumnCount(2)
        
        self.tbl_anchor_points.setItem(0,0,QTableWidgetItem('Marker Name'))
        self.tbl_anchor_points.setItem(0,1,QTableWidgetItem('Distance'))
    #-----------------------
    #---  app functions?
    #-----------------------

    def press_btn_add_anchor(self):
        #get values
        qm_text = self.txt_q_marker.text()
        qm_dist_text = self.txt_q_dist.text()
        qm_dist_type = self.cbo_dist_unit.currentText()
        
        targ_name = self.txt_notes.text() #fix form's name latter...
        targ_notes = self.lineEdit_4.text() 
        
        
        try:
            qm_dist = float(qm_dist_text)
        except:
            print('must enter a number for distance!')
        
        if qm_dist_type == 'km':
            qm_dist=qm_dist*1000
        
        #try and find anchor point key...
        anchor_keys = [x for x in anchor_points.keys() if qm_text in x]
        anchor_key = anchor_keys[0]
        anchor_xyz = anchor_points[anchor_key]
        
        
        
        if targ_name not in session_data.keys():
            session_data[targ_name]={}
            session_data[targ_name]['anchor_name']=[]
            session_data[targ_name]['anchor_point']=[]
            session_data[targ_name]['distance']=[]
        
        session_data[targ_name]['anchor_name'].append(anchor_key)
        session_data[targ_name]['anchor_point'].append(anchor_xyz)
        session_data[targ_name]['distance'].append(qm_dist)
        session_data[targ_name]['notes']=targ_notes

        #update table
        cur_row_id = len(session_data[targ_name]['anchor_point'])+1
        
        print(cur_row_id)
        print(anchor_key)
        print(qm_dist)
        
        self.tbl_anchor_points.setRowCount(cur_row_id)
        self.tbl_anchor_points.setItem(cur_row_id-1,0,QTableWidgetItem(str(anchor_key)))
        self.tbl_anchor_points.setItem(cur_row_id-1,1,QTableWidgetItem(str(qm_dist)))
        self.tbl_anchor_points.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        if len(anchor_keys)==1:
            pass
        else:
            print('invalid anchor key?')
            raise()
        
        print(qm_text, qm_dist_text, qm_dist_type, anchor_key[0], anchor_xyz)
        
        #populate the table?
        #tbl_anchor_points
        
        
        #reset values
        self.txt_q_marker.setText('')
        self.txt_q_dist.setText('')
        # self.txt_notes.setText('')
        self.lineEdit_4.setText('')
        print(json.dumps(session_data,indent=4))
        
        self.txt_q_marker.setFocus()
    
    def press_btn_clear_anchors(self):
        # self.reset_table()
        targ_name = self.txt_notes.text()
        cur_row_id = len(session_data[targ_name]['anchor_name'])
        
        
        self.tbl_anchor_points.setRowCount(cur_row_id)
        try:
            session_data[targ_name]['anchor_name'].pop()
            session_data[targ_name]['anchor_point'].pop()
            session_data[targ_name]['distance'].pop()
        except:
            session_data.pop(self.txt_notes.text())
            self.txt_notes.setText('')
            
        print(json.dumps(session_data,indent=4))
        
        # session_data.pop(self.txt_notes.text())
        
        # self.txt_notes.setText('')
        self.txt_q_marker.setFocus()


    def press_btn_save_anchors(self):
        #attempt to return/populate multilateration and DD coordiantes
        targ_name = self.txt_notes.text()
        distances_to_station = np.array(session_data[targ_name]['distance'])
        stations_coordinates = np.array(session_data[targ_name]['anchor_point'])
        print(distances_to_station)
        print(stations_coordinates)
        x,y,z = starlib.gps_solve(distances_to_station, stations_coordinates)
        
        
        self.lineEdit.setText(','.join([str(i) for i in [x,y,z]]))
        
        ##and DD coordiantes
        
        x_proj, y_proj = starlib.xyz_to_degrees([x,y,z])
        
        self.lineEdit_2.setText(str(x_proj)+', '+str(y_proj))
        #save full output to json file
        
        
        session_data[targ_name]['dec_degrees']=[x_proj, y_proj]
        session_data[targ_name]['xyz']=[x,y,z]
        
        
        with open('star_gui.json','w') as temp:
            temp.write(json.dumps(session_data, indent=4))
        
        
        #clear everything in the inputs box but DO NOT clear session data
        self.txt_notes.setFocus()
    #-----------------------
    #---  form 2, calculate bearing logic
    #-----------------------
    def change_cbo_orig_type(self):
        type_key = self.cbo_orig_type.currentText()
        
        if type_key == 'Quantum Marker':
            driver_dict = quantum_data
        elif type_key == 'Survey Point':
            driver_dict = session_data
        else:
            print('This is probably an error...')
            raise()
        
        #remove all entries...
        self.cbo_orig_name.clear()
        #populate cbo box: cbo_orig_name
        for key in driver_dict.keys():
            self.cbo_orig_name.addItem(key)

    def change_cbo_dest_type(self):
        type_key = self.cbo_dest_type.currentText()
        
        if type_key == 'Quantum Marker':
            driver_dict = quantum_data
        elif type_key == 'Survey Point':
            driver_dict = session_data
        else:
            print('This is probably an error...')
            raise()
        #remove all entries...
        self.cbo_dest_name.clear()
        #populate cbo box: cbo_orig_name
        for key in driver_dict.keys():
            self.cbo_dest_name.addItem(key)
    
    # def change_cbo_orig_name(self):
    #     pass
    
    def press_btn_calc_heading(self):
        #set up dicts
        type_key_orig = self.cbo_orig_type.currentText()
        
        if type_key_orig == 'Quantum Marker':
            driver_dict_orig = quantum_data
        elif type_key_orig == 'Survey Point':
            driver_dict_orig = session_data

        type_key_dest = self.cbo_dest_type.currentText()
        
        if type_key_dest == 'Quantum Marker':
            driver_dict_dest = quantum_data
        elif type_key_dest == 'Survey Point':
            driver_dict_dest = session_data

        origin_key = self.cbo_orig_name.currentText()
        dest_key = self.cbo_dest_name.currentText()

        origin_point = driver_dict_orig[origin_key]
        dest_point = driver_dict_dest[dest_key]
        
        print('\n\n--------------------')
        print(origin_point)
        print('--------------------')
        print(dest_point)
        print('--------------------')
        
        x1, y1 = origin_point['dec_degrees']
        x2, y2 = dest_point['dec_degrees']
        
        bearing = starlib.get_bearing(y1, x1, y2, x2)
        print(bearing)
        self.heading_2_target.setText(str(bearing))
        
        point_1 = np.array(origin_point['xyz'])
        point_2 = np.array(dest_point['xyz'])
        distance = np.linalg.norm(point_1-point_2)
        self.dist_2_target.setText(str(round(distance, 2)))
        pass
    #-----------------------    
    #manual data entry
    #-----------------------    
    
    def press_btn_man_add(self):
        targ_name = self.target_name_manual.text()
        
        x = float(self.txt_man_x.text())
        y = float(self.txt_man_y.text())
        z = float(self.txt_man_z.text())
        session_data[targ_name]={}
        session_data[targ_name]['xyz'] = [x,y,z]
        session_data[targ_name]['dec_degrees'] = starlib.xyz_to_degrees([x,y,z])
        
        self.txt_dec_degrees.setText(str(round(session_data[targ_name]['dec_degrees'][0], 2))+', '+str(round(session_data[targ_name]['dec_degrees'][1],2)))
        
        # qt_dist = 0.0
        # self.txt_qt_dist.setText(qt_dist)
        pass



    #-----------------------    

    def connectSignalsSlots(self):
        self.pushButton.clicked.connect(self.press_btn_add_anchor)
        self.btn_clear_anchors.clicked.connect(self.press_btn_clear_anchors)
        self.btn_save_anchors.clicked.connect(self.press_btn_save_anchors)
        #---  form 2, calculate bearing logic
        self.cbo_orig_type.currentIndexChanged.connect(self.change_cbo_orig_type)
        self.cbo_dest_type.currentIndexChanged.connect(self.change_cbo_dest_type)
        self.btn_calc_heading.clicked.connect(self.press_btn_calc_heading)
        #---  form 3, manual data entry
        self.btn_man_add.clicked.connect(self.press_btn_man_add)


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec()) 