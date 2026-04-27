import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def plot_track(storm_track):
    df = storm_track.data

    plt.plot(df['lon'], df['lat'])
    plt.xlabel("Longitude (°)")
    plt.ylabel("Latitude (°)")
    plt.title("Storm track: " + storm_track.storm_id)
    plt.grid()
    plt.show()

def plot_intensity(storm_track):
    df = storm_track.data
    
    plt.figure()
    plt.plot(df['time'], df['wind'], marker='o')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    plt.xticks(rotation=45)
    plt.xlabel("Time")
    plt.ylabel("Wind Speed (kts)")
    plt.title("Intensity: " + storm_track.storm_id)
    plt.grid()
    plt.tight_layout()
    plt.show()
