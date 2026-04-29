import pandas as pd
from .utils import haversine

class StormTrack:
    """
    Represents the track and intensity evolution of a single storm.

    Parameters
    ----------
    storm_id: str
        Unique identifier for the storm.
    df: pandas.DataFrame
        DataFrame containing storm track data. Must include columns 'time', 'lat', 'lon', and 'wind'.
    
    Attributes
    ----------
    storm_id: str
        Identifier for the storm
    df: pandas.DataFrame
        Time-sorted storm track data.
    """

    def __init__(self, storm_id, df):
        self.storm_id = storm_id
        self.df = df.sort_values('time')

    def get_duration(self):
        """
        Calculate total duration of the storm.
        
        Returns
        -------
        float
            Duration of the storm in hours. Returns 0 if fewer than two time points are available.
        """
        if len(self.df) < 2:
            return 0
        
        delta = self.df['time'].iloc[-1] - self.df['time'].iloc[0]
        return delta.total_seconds() / 3600

    def get_max_wind(self):
        """
        Get the maximum sustained wind speed of the storm.
        
        Returns
        -------
        float
            Maximum speed found in the 'wind' column.
        """
        return self.df['wind'].max()

    def get_total_distance(self):
        """
        Compute the total distance traveled by the storm.
        
        Returns
        -------
        float
            Total distance traveled along the track in km.
        """
        total_dist = 0
        for i in range(1,len(self.df)):
            total_dist += haversine(
                self.df['lat'].iloc[i-1],self.df['lon'].iloc[i-1],
                self.df['lat'].iloc[i],self.df['lon'].iloc[i]
            )
        return total_dist
    
class IntensityAnalyzer:
    """
    Analyze intensity changes in a storm track.
    
    Parameters
    ----------
    storm_track: StormTrack
        StormTrack object containing the storm data.
    
    Attributes
    ----------
    df: pandas.DataFrame
        Copy of the storm track data used for analysis.
    """

    def __init__(self, storm_track):
        self.df = storm_track.df
    
    def detect_rapid_intensification(self):
        """
        Detect rapid intensification (RI) events in the storm track.

        Rapid intensification is defined as an increase in wind speed of at least 30 knots within a 24 hour period.

        Returns
        -------
        list of dict
            A list of dictionaries representing RI events. Each dictionary contains:
            - 'start_time': pandas.TimeStamp
            - 'end_time': pandas.TimeStamp
            - 'increase': float
                Wind speed increase (knots)
        
        Notes
        -----
        Only the strongest RI event within overlapping 24-hour windows is retained.
        """
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
