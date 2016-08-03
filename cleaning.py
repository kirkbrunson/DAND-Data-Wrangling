import xml.etree.cElementTree as ET
from collections import defaultdict
from utils import is_address, is_street, mapping, OSMFILE


def update_street_suffix(name, mapping=mapping):
    """Updates street suffix to value in mapping"""

    name = name.split()
    if len(name) > 1 and name[-1] in mapping:
        name[-1] = mapping[name[-1]]
    return ' '.join(name)


def clean_address(address):
    """parses & corrects k='address' string"""

    try:
        house_num, street, city, state, zip_code = [None]*5
        _addr = address.split(',')

        if len(_addr) < 2:
            raise Exception

        t = _addr[0].split()
        house_num = t[0]

        # parse & update street str
        street = ' '.join(t[1:])
        street = update_street_suffix(street, mapping)

        # deal with Eg: , Cambridge, MA 02139, USA
        _addr = ' '.join(_addr[1:]).split()

        # rm trailing country or incomplete zip
        if _addr[-1] == 'USA' or _addr[-1] == '00':
            _addr.pop()

        # last val should be zip. All zips start 0
        if _addr[-1].startswith('0'):
            zip_code = _addr.pop()

        # Mass state abbreviations
        if (_addr[-1].startswith('m') or _addr[-1].startswith('M')) and len(_addr[-1]) in [2, 4, 13]:
            _addr.pop()  # rm current state value and standardize
            state = "Massachusetts"

        city = ' '.join(_addr)
        return {'house_number': house_num,
                'street': street,
                'city': city,
                'state': state,
                'zip_code': zip_code}

    except Exception as e:
        print 'Skipping possible bad address: ', address
