"""
Reads the output inside output.xml file

the format is :
<tripinfos>
    <tripinfo>
        ...
"""

import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

def read_xml_file(xml_file_name):
    tree = ET.parse(xml_file_name)
    root = tree.getroot()
    return root


filename= "output.xml"

f = read_xml_file(filename)

children=[]

for child in f:
    children.append(child.attrib)
    #print(child.attrib["arrivalPos"])

print(type(children[0]))