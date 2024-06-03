Work starts with the reduced_segs.ipynb file which uses .gpx file from the RAAM website to create track segments and store in a .pkl file (segments_reduced.pkl)

Used course.py from previous repo and modified to work with this .pkl file to create a course and be able to find current segment on the course when given lat,lon.
Need to adjust lines 33 and 182 with .pkl location to work

get_future_seg_weather(lat,lon,time_in_future) in weatherv2.py takes latitude, longitude, and a time from now in seconds to gather estimated wind speed and direction 
for the desired point of a segment from the 2 day hourly forecast API. This is called in main_trial.py where main work is done

calculate_headwind(rider_bearing, wind_speed, wind_direction) in prediction.py uses previously made formula to calculate the wind relative to rider in m/s. This is also called in
main_trial.py

Adjust latitude (line17), longitude (line18), and desired window (line20) in main_trial.py prior to running the whole file. When ran, the script uses these given variables to find the 
current segment and next x segements as defined. It then iterates over this data, gathers wind data from weatherv2, calculates headwind, and sends it with the segment distance and slope
to predict_segment_duration in prediction.py to estimate how long the segment will take. Then adds this time to a counter for when to gather the next segments weather data for, and so on.

Current limitations besides not having a final rest/race decision chart are the redict_segment_duration which just assumes a generic speed of 7 m/s and does not used and of the variables.
Could in theory use an estimated power and other coefficients to get a changing speed - but just altering this function should work with the rest of the code. These segment duration 
estimates can be used in combination with other code to decide when it could be most beneficial to rest.

Elevation profile: average elevation line not properly weighted with segment length
![elevation_profile_map_reduced](https://github.com/nfstatz18/RAAM/assets/124414802/8e2fc1a8-0de9-4717-9b13-7983b4290fa7)

RAAM track from coordinates after processing segments:
![RAAM_Track_reduced](https://github.com/nfstatz18/RAAM/assets/124414802/d5558f5f-94e7-445a-9cb2-da885e0d113d)




