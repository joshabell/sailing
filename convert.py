import re
import gpxpy
import gpxpy.gpx

def dms_to_decimal(degree, minute, direction):
    decimal = degree + minute/60
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal

def parse_line(line):
    parts = line.split('|')
    if len(parts) < 5:
        return
    key = parts[0].strip()
    name = parts[1].strip()
    location = parts[2].strip()
    lat = parts[3].strip()
    long = parts[4].strip()
    match_lat = re.match(r"(\d+)° (\d+\.\d+)'", lat)
    match_long = re.match(r"(\d+)° (\d+\.\d+)'", long)
    if match_lat and match_long:
        lat_degree, lat_minute = map(float, match_lat.groups())
        long_degree, long_minute = map(float, match_long.groups())
        lat_decimal = dms_to_decimal(lat_degree, lat_minute, 'N')
        long_decimal = dms_to_decimal(long_degree, long_minute, 'W')
        return key, (name, location, lat_decimal, long_decimal)
    return None

def parse_file(filename):
    waypoints = {}
    with open(filename, 'r') as file:
        for line in file:
            if not line.startswith('#'):
                waypoint = parse_line(line)
                if waypoint:
                    waypoints[waypoint[0]] = waypoint[1]
    return waypoints

waypoints = parse_file('waypoints.txt')
for key, waypoint in waypoints.items():
    print(f"{key}: {waypoint}")
    
    
def create_gpx(waypoints):
    gpx = gpxpy.gpx.GPX()

    for key, waypoint in waypoints.items():
        gpx_waypoint = gpxpy.gpx.GPXWaypoint()
        gpx_waypoint.latitude = waypoint[2]
        gpx_waypoint.longitude = waypoint[3]
        gpx_waypoint.name = f"{key} : {waypoint[1]}"
        gpx.waypoints.append(gpx_waypoint)

    return gpx.to_xml()

waypoints = parse_file('waypoints.txt')
gpx = create_gpx(waypoints)

with open('waypoints.gpx', 'w') as file:
    file.write(gpx)