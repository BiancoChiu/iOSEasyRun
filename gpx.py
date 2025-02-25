import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

import config
from waypoints import waypoints

round = config.config.n_round
coordinates = waypoints(v=config.config.v)

gpx = ET.Element('gpx', version="1.1", creator="Python")

trk = ET.SubElement(gpx, 'trk')
trk_name = ET.SubElement(trk, 'name')
trk_name.text = "Sample Track"

trkseg = ET.SubElement(trk, 'trkseg')

start_time = datetime(2025, 1, 1, 0, 0, 0)

for n in range(round):
    for i, loc in enumerate(coordinates):
        lat, lon = loc.values()

        time = start_time + timedelta(seconds=i*0.2+len(loc)*n*0.2)
        time_str = time.isoformat() + "Z"
        
        trkpt = ET.SubElement(trkseg, 'trkpt', lat=str(lat), lon=str(lon))
        time_element = ET.SubElement(trkpt, 'time')
        time_element.text = time_str

tree = ET.ElementTree(gpx)
tree.write("track.gpx", encoding="UTF-8", xml_declaration=True)

print("GPX Track file has been generated successfully!")
