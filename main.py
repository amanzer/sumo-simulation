import requests
import os
import xml.etree.ElementTree as ET
import sumolib
import json
import pandas as pd
from shapely.geometry import Point

API_KEY = os.getenv('API_KEY')

class SimulationResults:
    endpoint = 'https://maps.googleapis.com/maps/api/distancematrix/json'

    def __init__(self) -> None:
        net = sumolib.net.readNet('ulb/ulb.net.xml')
        data_trips = self.read_trips()

    
    def read_trips(self):
        tree = ET.parse('ulb/trips.trips.xml')
        root = tree.getroot()
        data = {}
        for trip in root:
            data[trip.attrib['id']] = {'depart' : trip.attrib['depart'], 'from' : trip.attrib['from'], 'to' : trip.attrib['to']}
        return data

    def find_trip_id(self, fromLane, toLane):
        for trip in self.data_trips:
            if self.data_trips[trip]['from'] == fromLane and self.data_trips[trip]['to'] == toLane:
                return trip
        return None

    def getGeocoordinates(self, coord):
        '''
        Returns the geocoordinates of the sumo network coordinates
        '''
        #geocoordinates = []
        point = Point(coord)
        lon, lat = net.convertXY2LonLat(point.x, point.y)
        return str(lat) + "," + str(lon)
        #geocoordinates.append((lat, lon))
        #return geocoordinates
    
    def OD_lists():
        self.origins=[]
        self.destinations=[]
        for trip in data:
            fromShape = net.getEdge(data[trip]['from']).getShape()
            toShape = net.getEdge(data[trip]['to']).getShape()
            
            self.origins.append( getGeocoordinates(fromShape[0]))
            self.destinations.append( getGeocoordinates(toShape[0]))

        print(self.origins)
        print(self.destinations)
    
    def get_google_data(self, origins, destinations):
        params = {
            'origins': origins[:5],
            'destinations':destinations[:5],
            'key': API_KEY
        }

        response = requests.get(endpoint, params=params)

        if response.status_code == 200:
            data = response.json()
            rows = data['rows']
            for row in rows:
                elements = row['elements']
                for element in elements:
                    distance = element['distance']['text']
                    duration = element['duration']['text']
                    print(f"Distance: {distance}")
                    print(f"Duration: {duration}")
        else:
            print("fail")
    
    