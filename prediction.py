#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 14:28:13 2024

@author: nickstatz
"""
import math

def calculate_headwind(rider_bearing, wind_speed, wind_direction):
        """
        
        Parameters
        ----------
        rider_bearing : bearing of the rider from segment info in radians
        wind_speed : speed of wind in m/s
        wind_direction : direction of wind from weather in degrees

        Returns
        -------
        headwind : the relative wind estimated for duration of segment in m/s

        """
         # return in m/s - same as wind_speed input
         # convert wind direction to radians
        wind_direction = math.radians(wind_direction)
        # find the relative angle between the two 
        relative_wind_angle = min((2 * math.pi) - abs(rider_bearing - wind_direction), abs(rider_bearing - wind_direction))
        #calculate effective wind speed
        headwind = math.cos(relative_wind_angle) * wind_speed
        return headwind
    
    
#TODO FUNCTION ESTIMATES TIME BASED OFF OF AN ASSUMED SPEED OF 7m/s 
# NEEDS CHANGE BASED ON HOW WE WANT TO CALCULATE SPEED W/ VARIABLES
def predict_segment_duration(dist,rel_wind,slope):
        """
        Parameters
        ----------
        sdist: distance of segment  (m)
        rel_wind: relative wind speed  (m/s)
        slope: slope of segment (m/m)

        Returns
        -------
        estimated time to complete segment in seconds

        """
        distance = dist
        rel_wind = rel_wind
        slope = slope
        speed = 7 #m/s
        est_time = distance/speed
        
        return est_time 

