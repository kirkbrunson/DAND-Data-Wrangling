from pymongo import MongoClient
from string import capitalize

client = MongoClient()
db = client.project3
boston = db.boston_massachusetts


def user_stats(n=10):
    """Prints num unique users and top n users"""

    res = list(db.boston_massachusetts.aggregate(
        [{"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
         {"$sort": {"count": -1}}]))

    _len = n if n <= len(res) else len(res)

    print "Num Unique Users: ", len(res)
    print "Top %i Users: \n" % _len
    for i in res[:_len]:
        print i['count'], '-', i['_id']


def num_nodes_ways():
    """Prints number of Nodes and number of Ways"""

    res = list(db.boston_massachusetts.aggregate(
        [{"$group": {"_id": "$type", "count": {"$sum": 1}}},
         {"$sort": {"count": -1}}]))

    print "\nNum Nodes: ", res[0]['count']
    print "Num Ways: ", res[1]['count']


def tag_overview():
    """Prints summation stats for Amentity, Shop, and Tourism tags"""

    tags = ['$amenity', '$shop', '$tourism']
    for tag in tags:
        res = list(db.boston_massachusetts.aggregate(
            [{"$group": {"_id": tag, "count": {"$sum": 1}}},
             {"$sort": {"count": -1}}]))

        _len = len(res) if len(res) < 30 else 30
        print "\nTop %i %s Types:" % (_len, capitalize(tag[1:]))

        # print results excluding top "None" result
        for i in res[1:30]:
            print i['count'], '-', i['_id']

        print "Press any key to continue or 'q' to quit..."
        if raw_input() == 'q':
            break


def list_sources():
    test = "$source"
    res = list(db.boston_massachusetts.aggregate(
        [{"$group": {"_id": test, "count": {"$sum": 1}}},
         {"$sort": {"count": -1}}]))
    print "\nSources:"
    for i in res:
        print i['count'], '-', i['_id']


# call aggregation methods
user_stats()
num_nodes_ways()
tag_overview()

# uncomment to see sources. Good candidate for further cleaning/ analysis
# list_sources()
