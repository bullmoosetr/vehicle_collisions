#!/bin/bash

python cycle_collisions/nyc_collision_data/downalod_file.py

unzip 201901-citibike-tripdata.csv.zip

mv 201901-citibike-tripdata.csv  ~/credit_shelf/vehicle_collisions/static/

rm 201901-citibike-tripdata.csv.zip

echo "Download and Operations Completed"