import xml.etree.cElementTree as ET
import json
import pprint
from collections import Counter
from utils import is_address, is_street, valid_street_suffixes, OSMFILE

problem_suffixes = set()
key_set = Counter()


def audit_suffix(street, suffixes=valid_street_suffixes):
    """Identifies possibly bad street suffix"""
    street = street.split()
    if street[-1] not in suffixes:
        problem_suffixes.add(street[-1])


def audit_address(address):
    """Parses/ Audits full address for street suffix"""
    try:
        _addr = address.split(',')

        if len(_addr) < 2:
            raise Exception

        # strip street from string and audit
        t = _addr[0].split()
        street = ' '.join(t[1:])
        street = audit_suffix(street)

    except Exception as e:
        print 'Address error: ', address


def audit(osmfile):
    """Audits osmfile for address and key type info"""
    osm_file = open(osmfile, "r")

    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):

                # tag: k="address"
                if is_address(tag):
                    audit_address(tag.attrib['v'])

                # tag: k="addr:street"
                elif is_street(tag):
                    audit_suffix(tag.attrib['v'])

                # enumerate tag keys
                if tag.attrib['k']:
                    if tag.attrib['k'] in key_set.keys():
                        key_set[tag.attrib['k']] += 1
                    else:
                        key_set[tag.attrib['k']] = 1

    osm_file.close()


if __name__ == '__main__':
    audit(OSMFILE)
    print '\nProblem_suffixes:\n', problem_suffixes
    print '\nCommon Key types:\n', '--'*30, '\n'
    pprint.pprint(key_set.most_common(100))
