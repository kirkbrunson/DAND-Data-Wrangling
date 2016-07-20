mapping = {"St": "Street",
           "st": "Street",
           "ST": "Street",
           "St.": "Street",
           "St,": "Street",
           "Street.": "Street",
           "street": "Street",
           "Sq": "Square",
           "Rd.": "Road",
           "Rd": "Road",
           "Roa": "Road",
           "rd.": "Road",
           "ave": "Avenue",
           "Ave": "Avenue",
           "Ave.": "Avenue",
           "AVE": "Avenue",
           "Dr.": "Drive",
           "dr.": "Drive",
           "driveway": "Driveway",
           "Ct": "Court",
           "Ct.": "Court",
           "Crt": "Court",
           "HIghway": "Highway",
           "Hwy": "Highway",
           "Pkwy": "Parkway",
           "Pkwy.": "Parkway",
           "Pk.": "Parkway",
           "Pk": "Parkway",
           "Pl": "Place",
           "place": "Place",
           "floor": "Floor",
           "Blvd.": "Boulevard",
           "Blvd": "Boulevard",
           "blvd": "Boulevard",
           "boulevard": "Boulevard",
           "Ln": "Lane",
           "Ln.": "Lane",
           "LN": "Lane",
           "LN.": "Lane",
           "lane": "Lane",
           "Loga": "Logan",
           "wharf": "Wharf",
           "way": "Way",
           "LEVEL": "Level"
           }

valid_street_suffixes = ["Street", "Square", "Road", "Avenue", "Drive",
                         "Court", "Highway", "Parkway", "Place", "Floor",
                         "Broadway", "Boulevard", "Lane", "Plaza", "Terrace",
                         "Circle", "Complex", "Wharf", "Corner", "Driveway",
                         "Way"]

# sample addresses
test_data = ['500 Broadway, Chelsea MA 02150',
             '123 Main St., Watertown MA 00',
             '130 Louders Lane, Jamaica Plain MA 02130',
             '300 Longwood Avenue, Boston MA 00',
             '73 Hemenway Street',
             '103 Garland St., Everett, MA;103 Garland St., Everett MA 02149',
             '40 New Sudbury St, Boston, MA, 02114',
             '350 Prospect, Belmont MA 02478-2662',
             '650 E. Fourth Street, South Boston MA 02127',
             '77 Massachusetts Avenue, Cambridge, MA 02139, USA']

# move to config
OSMFILE = 'boston_massachusetts.osm'


def is_street(elem):
    return (elem.attrib['k'] == "addr:street")


def is_address(elem):
    return (elem.attrib['k'] == "address")
