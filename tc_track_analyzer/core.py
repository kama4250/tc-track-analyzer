import pandas as pd
from .utils import haversine

class StormTrack:
    def __init__(self, storm_id, df):
        self.storm_id = storm_id
        self.data = df.sort_values('time')

    def get_duration(self):
        if len(self.data) < 2:
            return 0
        
        delta = self.data['time'].iloc[-1] - self.data['time'].iloc[0]
        return delta.total_seconds() / 3600

    def get_max_wind(self):
        return self.data['wind'].max()

    def get_total_distance(self):
        total_dist = 0
        for i in range(1,len(self.data)):
            total_dist += haversine(
                self.data['lat'].iloc[i-1],self.data['lon'].iloc[i-1],
                self.data['lat'].iloc[i],self.data['lon'].iloc[i]
            )
        return total_dist
    
class IntensityAnalyzer:
    def __init__(self, storm_track):
        self.df = storm_track.data
    
    def detect_rapid_intensification(self):
        ri_events = []

        self.df['time'] = pd.to_datetime(self.df['time'])
        self.df = self.df.sort_values('time').reset_index(drop=True)

        for i in range(len(self.df)):
            for j in range(i + 1, len(self.df)):
                time_diff = self.df.iloc[j]['time'] - self.df.iloc[i]['time']

                if time_diff.total_seconds() > 24 * 3600:
                    break

                wind_diff = self.df.iloc[j]['wind'] - self.df.iloc[i]['wind']

                if wind_diff >= 30:
                    ri_events.append({
                        'start_time': self.df.iloc[i]['time'],
                        'end_time': self.df.iloc[j]['time'],
                        'increase': wind_diff
                    })

        strongest_events = []

        for event in ri_events:
            if not strongest_events:
                strongest_events.append(event)
                continue

            last_event = strongest_events[-1]
            time_gap = (event['start_time'] - last_event['start_time']).total_seconds()

            if time_gap < 24 * 3600:
                # replace if stronger
                if event['increase'] > last_event['increase']:
                    strongest_events[-1] = event
            else:
                strongest_events.append(event)
        return strongest_events
