### Data Set overview:

*Stats as of 8-1-16*

- Size of osm uncompressed: 433.8 MB
- Number of Unique Users: 969
- Number of Nodes: 1930900
- Number of Ways: 308199


### Challenges Encountered:

- Address parsing. Many nodes have both an `address` key/ value pair and `addr:XYZ` fields for a second copy of the address. I added the `is_address` and `is_street` helpers and branch address parsing/ cleaning on the return value of these helpers. 

- Often the top result for group & sum aggregation queries returns `None`. This makes sense as not all tag types will have a value. However, this should be cleaned from the data set.


### Resources:

MongoDB and PyMongo docs and Stack Overflow.


### Additional Stats:

There is quite a bit of dirty data from these queries. For instance, there are at least four names for Starbucks ("Starbucks", "Starbuck's Coffee", "Starbucks Coffee", and "Starbucks (SMG)"). This would be a good area to do further data cleaning.

- Coffee shops:
`db.boston_massachusetts.aggregate([{$match: { "amenity" : "cafe", "cuisine": "coffee_shop" }}, {$group: {_id: "$name", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])`

This shows that Starbucks is the most numerous coffee shop with a total of 29 locations, followed by Dunkin's with 10. (Dunkin's tends to be classified as a cafe where it has 49 locations).



- Cafes:
`db.boston_massachusetts.aggregate([{$match: { "amenity" : "cafe" }}, {$group: {_id: "$name", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])`

A more general query than above, but I think this gives a better view of the data. The same issues with data cleaning exist, and after the chains (Starbucks, Dunkin's, Au Bon Pain) it's mostly independent locations with a single or perhaps two locations.


Universities / Colleges:
`db.boston_massachusetts.aggregate([{$match: { "amenity" : {$in: ["university", "college"]} }}, {$group: {_id: "$name", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])`

Here Boston University has the most data points with 41. However, a challenge with this query is that it doesn't take into account names that don't directly conform (Eg: "Harvard" has 5 data points, but doesn't include "Harvard Medical School", or other related locations like "Eliot House")

- Number of bookstores: 25
`db.boston_massachusetts.find({"shop": "books"}).count()`

- Banks:
`db.boston_massachusetts.aggregate([{$match: { "amenity" : "bank" }}, {$group: {_id: "$name", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])`

Bank of America comes in with 14 locations followed by Citizens Bank with 11. Note the same issues with cleaning bank names exist.

- Convenience shops
`db.boston_massachusetts.aggregate([{$match: { "shop" : "convenience" }}, {$group: {_id: "$name", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])`

Here 7-Eleven (or 7/11) has the most locations at 14.




### Ideas for further work:

- The `source` tag seems like a good candidate for further data cleaning and analysis. It looks like the majority of the sources are from MASS GIS and MASS DOT. However, the data is rather dirty, and there are a number of cases where people, search engines, or other nonstandard values are listed. Additionally, there's a number of links to the source, but many are broken. These could be parsed, validated, and linked to the data that contributes to a confidence index in the related data points. Additionally, the source data could be listed with the node/ way data for further investigation by users. 

A couple challanges to this could be that this value doesn't exist for every data point in the data set, that links are broken, that the sources come from widely varying sources (Eg: a GIS database, pdf, or "local knowledge"). 

- The `pos` values in the cleaned data set could be correlated with the amenity/ tag type data to show clustering or densities for the selected tag type. This could displayed as a heat map or used as input to make prediction about where to to go for a given tag type.

- Clean the dirty data mentioned in the additional Stats section. This would make the queries more accurate.
- Clean phone numbers. There's a bit of variance in how phone numbers are present. Since we have a gold standard (a phone book) and precise way of representing phone numbers, we could parse and clean this data point. This shouldn't be hard, and would likely include the same or fewer challenges as cleaning addresses.


---

### Documented queries:

**Number of Unique Users:**
`db.boston_massachusetts.aggregate([{"$group": {"_id": "$created.user", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])`

**Number of nodes and ways:**
`db.boston_massachusetts.aggregate([{"$group": {"_id": "$type", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])`

**Number of tag subtypes:**

- Amenities:
 -  `db.boston_massachusetts.aggregate([{"$group": {"_id": "$amenity", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])`
- Shops:
 -  `db.boston_massachusetts.aggregate([{"$group": {"_id": "$shop", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])`
- Tourism:
 -  `db.boston_massachusetts.aggregate([{"$group": {"_id": "$tourism", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])`


*See `overview_stats.py` for more.*

---

**Number of node types for amenities, shops, and tourism locations:**

- Top 30 Amenity Types:
  - 1314 - parking
  - 1034 - bench
  - 725 - school
  - 607 - restaurant
  - 446 - parking_space
  - 420 - place_of_worship
  - 321 - library
  - 243 - bicycle_parking
  - 240 - cafe
  - 186 - fast_food
  - 143 - university
  - 140 - bicycle_rental
  - 110 - fire_station
  - 101 - post_box
  - 95 - hospital
  - 93 - fuel
  - 90 - bank
  - 72 - waste_basket
  - 67 - pub
  - 67 - fountain
  - 55 - police
  - 55 - bar
  - 54 - post_office
  - 52 - pharmacy
  - 50 - atm
  - 42 - college
  - 39 - toilets
  - 36 - drinking_water
  - 35 - theatre

- Top 30 Shop Types:
  - 96 - convenience
  - 76 - supermarket
  - 57 - hairdresser
  - 45 - alcohol
  - 43 - clothes
  - 40 - car_repair
  - 31 - bicycle
  - 31 - beauty
  - 28 - bakery
  - 25 - books
  - 23 - car
  - 21 - laundry
  - 19 - gift
  - 19 - dry_cleaning
  - 17 - yes
  - 16 - hardware
  - 13 - mobile_phone
  - 11 - electronics
  - 11 - furniture
  - 10 - department_store
  - 10 - doityourself
  - 10 - florist
  - 9 - sports
  - 8 - pet
  - 8 - art
  - 8 - music
  - 7 - copyshop
  - 6 - stationery
  - 6 - optician

 - Top 16 Tourism Types:
  - 96 - hotel
  - 53 - museum
  - 50 - artwork
  - 31 - viewpoint
  - 29 - attraction
  - 27 - picnic_site
  - 22 - information
  - 5 - guest_house
  - 3 - hostel
  - 3 - motel
  - 2 - chalet
  - 2 - aquarium
  - 2 - zoo
  - 1 - gallery
  - 1 - theme_park
