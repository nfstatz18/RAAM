#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 20:28:39 2024

@author: nickstatz
"""

import course
import weatherv2
import prediction
import time
import config



#inputs
read_lat = 33.06112398
read_lon = -115.728762
#speed_est = 10  # m/s
analysis_window_size = 100
epoch_time = int(time.time())


def next_x_segment_variables(read_lat,read_lon):
    #get course object 
    course_object = course.Course()
    
    #establish current location on course from method in course.py
    current_segment_index = course_object.find_current_course_segment(read_lat, read_lon) 
    
    #get df from current segment to future segments within analysis window from method in course.py
    analysis_df = course_object.segment_df.iloc[current_segment_index:current_segment_index + analysis_window_size]
    
    #set time counter to zero
    add_time = 0
    
    #establish empty list and zero out i
    predicted_segment_variables = []
    i = 0
    
    #iterate through the next x segments (set analysis window)
    for i in range(len(analysis_df)):
        # just indexing the analysis df to get segment info
        lat =  analysis_df.loc[analysis_df.index[i], 'from_lat']
        lon =  analysis_df.loc[analysis_df.index[i], 'from_lon']
        seg_id =  analysis_df.loc[analysis_df.index[i],'segment_id']
        seg_bearing =  analysis_df.loc[analysis_df.index[i], 'bearing']
        seg_slope = analysis_df.loc[analysis_df.index[i],'slope']
        segment_distance = analysis_df.loc[analysis_df.index[i],'length_m']
        
        #get future weather data for a segment based on coordinates and incrementing timer variable
        future_segment_weather = weatherv2.get_future_seg_weather(lat, lon, add_time)
        
        #access prediced wind speed in m/s from result of valling weatherv2.get_future_seg_weather
        wind_speed_pred = future_segment_weather['wind_speed(m/s)']
        #access predicted direction of wind
        wind_direction_pred = future_segment_weather['wind_dir']
        #calculate relative wind speed calling prediction.calculate_headwind
        pred_headwind = prediction.calculate_headwind(seg_bearing,wind_speed_pred,wind_direction_pred)
        
        #create a dict to store variables created that can be used to predict speed
        info_dict = {
            'seg_distance':segment_distance,
            'pred_rel_wind_speed':pred_headwind,
            'seg_slope': seg_slope,
            'seg_id': seg_id
            }
        #append the dict into a list to store in case need to access
        predicted_segment_variables.append(info_dict)
        
        #estimate how long segment i will take based on everything found in lines above 
        # routes to prediction.predict segment duration - incomlete function
        segment_duration = prediction.predict_segment_duration(segment_distance,pred_headwind,seg_slope)
        
        #add found time to time counter to establish when to look at weather forecast for next seg
        add_time = add_time+segment_duration
        
    return predicted_segment_variables

    
if __name__ == '__main__':
    
    ran = next_x_segment_variables(read_lat,read_lon)
    print('no errors :)')
