import pandas as pd
from sodapy import Socrata
from cycle_collisions.models import *

def add_boroughs_to_db():
    boroughs = ['QUEENS', 'STATEN ISLAND', 'BROOKLYN', 'MANHATTAN', 'BRONX']
    objs = []
    for borough in boroughs:
        objs.append(Borough(borough=borough))
    
    quryset = Borough.objects.bulk_create(objs)
    return quryset


def get_collision_data_nyc(borough, date_range=None):
    client = Socrata("data.cityofnewyork.us", None)

    if borough:
        results = client.get("h9gi-nx95", borough=borough, limit=3000, where="crash_date between '2019-01-01T00:00:00' and '2019-12-12T00:00:00'", )
        df = pd.DataFrame.from_records(results)
        return df[df['number_of_cyclist_injured'] != "0"]
    
    else:
        return None

def get_injured_cyclist_data(data, borough):
    borough_obj = Borough.objects.get(borough=borough)

    if borough_obj:
        objs = []
        for i, v in enumerate(data.index):

            if 'on_street_name' in data.iloc[i].keys():
                on_street_name = data.iloc[i]['on_street_name']
            else:
                on_street_name = None
            if 'off_street_name' in data.iloc[i].keys():
                off_street_name = data.iloc[i]['off_street_name']
            else:
                off_street_name = None
            if 'cross_street_name' in data.iloc[i].keys():
                cross_street_name = data.iloc[i]['cross_street_name']
            else:
                cross_street_name = None

            contributing_factors = [ v  for k,v in data.iloc[i].items() if 'contributing_factor_vehicle' in k and isinstance(v, str)]
            vehicle_type_codes = [ v  for k,v in data.iloc[i].items() if 'vehicle_type_code_' in k and isinstance(v, str)]
            
            loc = CollisionLocation(
                    zip_code=data.iloc[i]['zip_code'],
                    latitude=data.iloc[i]['latitude'],
                    longitude=data.iloc[i]['longitude'],
                    on_street_name = on_street_name,
                    off_street_name = off_street_name,
                    cross_street_name = cross_street_name,
                    borough=borough_obj
            )

            loc.save()

            detail = CollisionDetail(
                crash_date=data.iloc[i]['crash_date'], 
                crash_time=data.iloc[i]['crash_time'],
                collision_id=data.iloc[i]['collision_id'],
                number_of_cyclist_injured=data.iloc[i]['number_of_cyclist_injured'],
                contributing_factor_vehicle=contributing_factors,
                vehicle_type_code=vehicle_type_codes,
                collision_location=loc
                )
            objs.append(detail)
        return CollisionDetail.objects.bulk_create(objs)

def add_data_to_db(borough):
    results = get_collision_data_nyc(borough=borough.upper())
    entries_created = get_injured_cyclist_data(data=results, borough=borough.upper())

    if entries_created:
        return entries_created
    else:
        return "An error occurred or the borough may not exist"

def create_unique_set(csv):
    if not csv.empty: 
        citi_stations = {}
        for i, v in enumerate(csv.index):   
            
            if csv.iloc[i]["start station id"] not in citi_stations and csv.iloc[i]["start station id"] != "NaN":
                citi_stations[csv.iloc[i]["start station id"]] =   {
                    "station_name":csv.iloc[i]["start station name"],
                    "station_latitude":csv.iloc[i]["start station latitude"],
                    "station_longitude":csv.iloc[i]["start station longitude"],
                    }
            
            if csv.iloc[i]["end station id"] not in citi_stations and csv.iloc[i]["end station id"] != "NaN":
                citi_stations[csv.iloc[i]["end station id"]] = {
                "station_name":csv.iloc[i]["end station name"],
                "station_latitude":csv.iloc[i]["end station latitude"],
                "station_longitude":csv.iloc[i]["end station longitude"],
                }
        return citi_stations
    else:
        return None

def get_citi_bike_data():
    from django.contrib.staticfiles import finders
    result = finders.find('201901-citibike-tripdata.csv')
    csv = pd.read_csv(result, usecols=[
        "start station id", 
        "start station name", 
        "start station latitude", 
        "start station longitude", 
        "end station id", 
        "end station name", 
        "end station latitude", 
        "end station longitude"
    ])

    return csv

def add_citibike_station_data(bike_stations):
    objs = []
    for k, v in bike_stations.items():

        objs.append(CitiBikeStation(
            station_id=k, 
            station_name=v["station_name"],
            station_latitude=v["station_latitude"],
            station_longitude=v["station_longitude"],
        ))
    
    citi_stations = CitiBikeStation.objects.bulk_create(objs)
    # Stations with no id
    CitiBikeStation.objects.filter(station_id="NaN").delete()
    return citi_stations


def get_citi_bike_data_and_add_to_db():
    csv = get_citi_bike_data()
    citibike_data = create_unique_set(csv)
    querysets = add_citibike_station_data(citibike_data)
    return querysets

                

