# tc-track-analyzer
This project will analyze tropical cyclone track data and identify key storm characteristics such as movement patterns and intensification events.

## Installation
python -m pip install -e .

## Quick start
Run a simple analysis on HURDAT2 hurricane data (hurricane Ida):
```python
from tc_track_analyzer.core import StormTrack, IntensityAnalyzer
from tc_track_analyzer.io import DataLoader
from tc_track_analyzer.utils import plot_track, plot_intensity

# Load HURDAT2 data
loader = DataLoader("../data/hurdat2-1851-2025-02272026.txt")
df = loader.load_hurdat2()

# Analyze a storm (hurricane Ida)
storm_id = "AL092021"
mask = (df['storm_id'] == storm_id)
storm_df = df[mask]

track = StormTrack(storm_id, storm_df)
analyzer = IntensityAnalyzer(track)
ri_events = analyzer.detect_rapid_intensification()

print("Storm:", storm_id)
print("Max wind:", track.get_max_wind())
print("Duration (hrs):", track.get_duration())
print("RI events:")
for event in ri_events:
    print(
        f"{event['start_time'].strftime('%Y-%m-%d %H:%M')} → "
        f"{event['end_time'].strftime('%Y-%m-%d %H:%M')} | "
        f"+{float(event['increase']):.0f} kt"
    )

# Plot the storm track and intensity
plot_track(track)
plot_intensity(track)
```
