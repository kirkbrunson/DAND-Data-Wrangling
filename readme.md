### Description:

Project 3 for Udacity's Data Analysis NanoDegree: Wrangle OpenStreetMap Data

This project covers data wrangling using Python and MongoDB. The data set used is an [Open Street Map](https://www.openstreetmap.org/relation/2315704#map=11/42.3225/-70.9061) [MapZen](https://mapzen.com) extract of Boston, Mass.

### QuickStart:

- Clone this repo
- Download [the osm map extract](https://mapzen.com/data/metro-extracts/#boston-massachusetts)
- Move `boston_massachusetts.osm.bz2` to proj dir and extract to `boston_massachusetts.osm`
- Run `python setup.py`
- Start mongod and input the cleaned `boston_massachusetts.json` with: 
  `mongoimport --db project3 --collection boston_massachusetts --drop --file boston_massachusetts.json`
- Run `python overview_stats.py`