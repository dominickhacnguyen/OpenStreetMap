import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from buildings import is_float, is_int, is_height, update_height
from states import is_state, update_state
from zipcodes import is_zip, update_zip
"""
This file transforms the shape of the XML data from OSM file into a JSON format.
"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
addr = re.compile(r'^addr:')
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
    node = {}
    address = {}
    created = {}
    coord = [0, 0]
    node_refs = []
    
    if element.tag == "node" or element.tag == "way" :
        
        if element.tag == "node":
            node["type"] = "node"
        else:
            node["type"] = "way"
        
        for attrib in element.attrib:
            attrib_value = element.attrib[attrib]

            # ADDED: Change numerical data in strings to float or int
            if is_int(attrib_value):
                attrib_value = int(attrib_value)
            elif is_float(attrib_value):
                attrib_value = float(attrib_value)

            # If value is a coordinate
            if attrib in ["lat", "lon"]:
                if attrib == "lat":
                    coord[0] = attrib_value
                else:
                    coord[1] = attrib_value
                node["pos"] = coord

            # If value should be in Created subdocument
            elif attrib in CREATED:
                created[attrib] = attrib_value

            else:
                node[attrib] = attrib_value
            
        if len(created) > 0:    
            node["created"] = created
        
        # Second level tags
        for tag in element.iter("tag"):
            
            k_attrib = tag.attrib['k']
            v_attrib = tag.attrib['v']

            # ADDED: Change numerical data in strings to float or int
            if is_int(v_attrib):
                v_attrib = int(v_attrib)
            elif is_float(v_attrib):
                v_attrib = float(v_attrib)

            # If contains problem characters or has more than 1 colon
            if problemchars.search(k_attrib) or k_attrib.count(':') > 1:
                pass

            # If address related tag
            elif addr.match(k_attrib):

                # ADDED: Resolve problematic zip codes.
                if is_zip(k_attrib):
                    v_attrib = update_zip(v_attrib)

                # ADDED: Clean state in address
                if is_state(k_attrib, v_attrib):
                    v_attrib = update_state(v_attrib)

                elif k_attrib == "addr:housenumber":
                    v_attrib = str(v_attrib)

                address[k_attrib.split(':')[1]] = v_attrib

            elif k_attrib.count(':') == 1:
                node[k_attrib.split(':')[1]] = v_attrib

            # ADDED: Clean heights
            elif is_height(k_attrib):
                node[k_attrib] = update_height(v_attrib)

            else:
                node[k_attrib] = v_attrib

        if len(address) > 0:
            node["address"] = address
            
        for node_ref in element.iter("nd"):
            node_refs.append(node_ref.attrib["ref"])
            
        if len(node_refs) > 0:
            node["node_refs"] = node_refs

        return node
    else:
        return None

def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")

    return data

if __name__ == "__main__":
    process_map('sample_200.osm', False)
