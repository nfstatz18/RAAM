#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 14:20:56 2024

@author: nickstatz
"""

import requests
import time
import math
import config

#not in use but could be useful
def get_current_seg_weather(lat,lon):
    # Base URL 2 Day Hourly https://api.weather.com/v3/wx/forecast/hourly/2day?geocode=33.74,-84.39&format=json&units=m&language=en-US&apiKey=yourApiKey
    # doc https://docs.google.com/document/d/1IeQP1PSRQMWVBqtxj2kMZvyym6GShU8u9I3FdwihMzw/edit
    #wind speed returns in km/h divide by 3.6 to get m/s

    
    API_KEY = config.API_KEY
    unit = 'm' #metric units - wind speed (km/h) 
    url = f'https://api.weather.com/v3/wx/forecast/hourly/2day?geocode={lat},{lon}&format=json&units={unit}&language=en-US&apiKey={API_KEY}'

    r = requests.get(url)
    if r.status_code != 200:
        print(f'Failed: status_code {r.status_code}, response body {r.text}')

    else:
        r_json = r.json()
    info = {}
    curr_time = r_json['validTimeUtc'][0]
    wind_dir = r_json['windDirection'][0]
    wind_speed_kmh = r_json['windSpeed'][0]
    wind_speed_m_s = wind_speed_kmh/3.6
    info = {
    "timeUTC": curr_time,
    "wind_dir": wind_dir,
    "wind_speed(m/s)": wind_speed_m_s
    }

    return info

def get_future_seg_weather(lat,lon,time_in_future):
    # Base URL 2 Day Hourly https://api.weather.com/v3/wx/forecast/hourly/2day?geocode=33.74,-84.39&format=json&units=m&language=en-US&apiKey=yourApiKey
    # doc https://docs.google.com/document/d/1IeQP1PSRQMWVBqtxj2kMZvyym6GShU8u9I3FdwihMzw/edit
    #wind speed returns in km/h divide by 3.6 to get m/s
    """
    give a latitude and longitude for a point to find weather prediction
    give an amount of time into the future you want to look for (in seconds)
    """
    # current time in UTC seconds - found easiest to work with weather API and estimate segments in seconds
    # and also helps not mess with time zones
    epoch_time = int(time.time())

    #find the time you want to predict at now + time to complete segments
    est_time = time_in_future + epoch_time
    
    # round time to nearest hour in UTC seconds
    time_rounded_to_search = 3600 * round(est_time/3600)
    
    # if we are on front half of an hour TWC API removes 'forecast' for that hour so jump to next hour
    if time_rounded_to_search < epoch_time:
        time_rounded_to_search = 3600 * math.ceil(est_time/3600)
    else:
        time_rounded_to_search = 3600 * round(est_time/3600)
        
    API_KEY = config.API_KEY
    unit = 'm' #metric units - wind speed (km/h) 
    url = f'https://api.weather.com/v3/wx/forecast/hourly/2day?geocode={lat},{lon}&format=json&units={unit}&language=en-US&apiKey={API_KEY}'

    r = requests.get(url)
    if r.status_code != 200:
        print(f'Failed: status_code {r.status_code}, response body {r.text}')

    else:
        r_json = r.json()
    #list of times in the next 48 hours valid for
    times = r_json['validTimeUtc']

    # find the index of the nearest future time to gather wind predictions for
    index = times.index(time_rounded_to_search)
    
    
    #establish varibles at desired hour prediction
    fut_time = r_json['validTimeUtc'][index]
    fut_wind_dir = r_json['windDirection'][index]
    fut_wind_speed_kmh = r_json['windSpeed'][index]
    fut_wind_speed_m_s = fut_wind_speed_kmh/3.6
    
    #establish dict containing wind vairables
    info = {
    "timeUTC": fut_time,
    "wind_dir": fut_wind_dir,
    "wind_speed(m/s)": fut_wind_speed_m_s
    }
    
    return info
        
        
        
        
        
        
        
        