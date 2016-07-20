#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import re
import codecs
import json
from utils import is_address, is_street, mapping, OSMFILE
from cleaning import update_street_suffix, clean_address

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


'''
This file is used to convert the original osm file to a cleaned json file.
Run it before importing with mongoimport:

mongoimport --db project3 --collection boston_massachusetts --drop --file boston_massachusetts.json
'''


def parse_element(element):
    """Parses elem from iterparse, cleans address, returns dict"""

    node = {}
    if element.tag == "node" or element.tag == "way":
        data = dict()

        # Parse data branching on elem.tag
        for elem in element.iter():
            if 'k' in elem.attrib:
                if re.match(problemchars, elem.attrib['k']):
                    print 'Skipping element: ', elem
                    continue

            if elem.tag == 'node':
                data['id'] = elem.attrib['id']
                data['type'] = elem.tag
                if 'visible' in elem.attrib:
                    data['visible'] = elem.attrib['visible']
                data['pos'] = [
                    float(elem.attrib['lat']), float(elem.attrib['lon'])]

                data['created'] = {}

                data['created']['version'] = elem.attrib['version']
                data['created']['changeset'] = elem.attrib['changeset']
                data['created']['timestamp'] = elem.attrib['timestamp']
                data['created']['user'] = elem.attrib['user']
                data['created']['uid'] = elem.attrib['uid']

            elif elem.tag == 'way':
                data['id'] = elem.attrib['id']
                data['type'] = elem.tag
                if 'visible' in elem.attrib:
                    data['visible'] = elem.attrib['visible']

            elif elem.tag == 'tag':
                if re.match(problemchars, elem.attrib['k']):
                    print 'Skipping tag: ', elem.attrib['k']
                    continue

                if is_address(elem):
                    data['address'] = clean_address(elem.attrib['v'])

                if is_street(elem):
                    if 'address' not in data:
                        data['address'] = {}
                    data['address']['street'] = update_street_suffix(
                        elem.attrib['v'])

                elem_key = elem.attrib['k'].split(':')

                if elem_key[0] == 'addr' or elem_key[0] == 'address':
                    continue  # already parsed address

                else:
                    data[':'.join(elem_key)] = elem.attrib['v']

            elif elem.tag == 'nd':
                if 'node_refs' not in data:
                    data['node_refs'] = []

                data['node_refs'].append(elem.attrib['ref'])

        return data
    else:
        return None


def osm_to_json(file_in, data_return=False):
    """writes parsed dict to json file and returns either filename or dict"""

    file_out = "{0}.json".format(file_in.split('.')[0])
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = parse_element(element)
            if el:
                data.append(el)
                fo.write(json.dumps(el) + "\n")
    return data if data_return else file_out


if __name__ == "__main__":
    osm_to_json(OSMFILE)
