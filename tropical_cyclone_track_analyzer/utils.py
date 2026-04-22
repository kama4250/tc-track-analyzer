import math
import matplotlib.pyplot as plt

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def plot_track(storm_track):
    lats = []
    lons = []

    for point in storm_track.data:
        lats.append(point['lat'])
        lons.append(point['lon'])

    plt.figure()
    plt.plot(lons, lats)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Storm track: " + storm_track.storm_id)
    plt.grid()
    plt.show()

def plot_intensity(storm_track):
    times = []
    winds = []

    for point in storm_track.data:
        times.append(point['time'])
        winds.append(point['wind'])

    plt.figure()
    plt.plot(times, winds)
    plt.xlabel("Time")
    plt.ylabel("Wind Speed")
    plt.title("Intensity: " + storm_track.storm_id)
    plt.grid()
    plt.show()
