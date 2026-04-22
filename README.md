# tc-track-analyzer
This project will analyze tropical cyclone track data and identify key storm characteristics such as movement patterns and intensification events.

## Installation
pip install -e .

## Quick start
Run a simple analysis on HURDAT2 hurricane data:
```python
from tc-track-analyzer.io import DataLoader
from tc-track-analyzer.core import StormTrack, IntensityAnalyzer
from tc-track-analyzer.utils import plot_track

# Load HURDAT2 data
loader = DataLoader("hurdat2-1851-2025-02272026.txt")
data = loader.load_hurdat2()

# Group data by storm
storms = {}
for row in data:
    if row['storm_id'] not in storms:
        storms[row]['storm_id'] = []
    storms.append(row)

# Analyze the first storm
storm_id = list(storms.keys())[0]
track = StormTrack(storm_id, storms[storm_id])

print("Storm:", storm_id)
print("Max wind:", track.get_max_wind())
print("Duration (hrs):", track.get_duration())

# Plot the storm track
plot_track(track)
```
