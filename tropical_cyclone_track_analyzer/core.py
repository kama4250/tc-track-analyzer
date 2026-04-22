from .utils import haversine
import matplotlib.pyplot as plt

class StormTrack:
    def __init__(self, storm_id, data):
        self.storm_id = storm_id
        self.data = data

    def get_duration(self):
        if len(self.data < 2):
            return 0
        
        delta = self.data[0]['time'] - self.data[-1]['time']
        return delta / 3600

    def get_max_wind(self):
        return self.data['wind'].max()

    def get_total_distance(self):
        total_dist = 0
        for ii in range(1,len(self.data)):
            total_dist += haversine(
                self.data[ii-1]['lat'],self.data[ii-1]['lon'],
                self.data[ii]['lat'],self.data[ii]['lon']
            )
        return total_dist
    
class IntensityAnalyzer:
    def __init__(self, storm_track):
        self.storm_track = storm_track

    def detect_rapid_intensification(self):
        ri_events = []
        for ii in range(len(self.storm_track.data)):
            for jj in range(ii+1, len(self.storm_track.data)):
                time_diff = (self.storm_track.data[jj]['time'] - self.storm_track.data[ii]['time'])

                if time_diff > 24:
                    break

                wind_diff = self.storm_track.data[jj]['wind'] - self.storm_track.data[ii]['wind']

                if wind_diff >= 30:
                    ri_events.append({
                        'start_time': self.storm_track.data[ii]['time'],
                        'end_time': self.storm_track.data[jj]['time'],
                        'increase': wind_diff
                    })
            return ri_events

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

