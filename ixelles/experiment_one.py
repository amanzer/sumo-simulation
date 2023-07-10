import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt


def read_data(filename:str) -> pd.DataFrame:
    tree = ET.parse("edgeData.xml")
    root = tree.getroot()
    edge_data = []
    for edge in root.iter('edge'):
        edge_data.append(edge.attrib)
    
    return pd.DataFrame(edge_data)


if __name__ == "__main__":
    df = read_data("edgeData.xml")

    df["congestion_score"] = df["density"].astype(float) 
    sorted_df = df.sort_values(by=['congestion_score'], ascending=False)
    print(sorted_df.head(10))
