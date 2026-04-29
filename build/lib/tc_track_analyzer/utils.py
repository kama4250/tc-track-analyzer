import math
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm 
from matplotlib.collections import LineCollection

def haversine(lat1, lon1, lat2, lon2):
    """
    Compute the great-circle distance between two points on Earth.

    Parameters
    ----------
    lat1: float
        Latitude of the first point (degrees).
    lon1: float
        Longitude of the first point (degrees).
    lat2: float
        Latitude of the second point (degrees).
    lon2: float
        Longitude of the second point (degrees).
    
    Returns
    -------
    float
        Distance between the two points in km.
    """
    R = 6371  # Earth radius in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Updating plot_track function to overlay on a map
def plot_track(storm_track):
    """
    Plot the geographic track of a storm on a map.

    Parameters
    ----------
    storn_track: StormTrack
        StormTrack object containing storm data. Must include a DataFrame attribute 'df' with columns 'lat', 'lon', and 'wind', and an attribute 'storm_id'.
    
    Returns
    -------
    tuple
        (fig, ax) where:
        - fig: matplotlib.figure.Figure
        - ax: matplotlib.axes._subplots.GeoAxesSubplot
    
    Notes
    -----
    Geographic map added by Clara via PR
    """
    df = storm_track.df
    
    # Setup figure and map projectipn
    fig, ax = plt.subplots(
        figsize = (8,10), 
        subplot_kw={'projection': ccrs.PlateCarree()}, 
        constrained_layout = True
    )

    #Add geographic features
    ax.coastlines(linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5, linestyle='--')
    ax.add_feature(cfeature.LAND, facecolor='gray', alpha=0.3)
    ax.add_feature(cfeature.STATES, edgecolor = 'gray', linewidth = 0.5, alpha = 0.2)
    ax.add_feature(cfeature.OCEAN, facecolor = 'lightblue')
    ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5)
    
    #Add padding: adding extra degrees to the edges of the map so the track doesnt look crammed
    padding = 5 # extra degrees around the track
    ax.set_extent([
        df['lon'].min() - padding, # left edge (minus 10)
        df['lon'].max() + padding, # right edge (plus 10)
        df['lat'].min() - padding, # bottom edge (minus 10)
        df['lat'].max() + padding  # top edge (plus 10)
    ], crs=ccrs.PlateCarree())

    # build line segments from consecutive lat/lon pairs using LineCollection
    points = np.array([df['lon'], df['lat']]).T.reshape(-1,1,2)
    segments = np.concatenate([points[:-1], points[1:]], axis = 1)

    lc = LineCollection(segments, cmap = "plasma", transform = ccrs.PlateCarree(), linewidth = 3)
    # uses df['wind'] to color the line (see the intensiy of the storm on the track)
    lc.set_array(df['wind'].values)
    ax.add_collection(lc)

    # add colorbar 
    plt.colorbar(lc, ax=ax, label = 'Wind Speed (kts)', shrink = 0.5)

    
    # mark start and end points 
    ax.plot(df['lon'].iloc[0], df['lat'].iloc[0], color = 'limegreen', marker = 'o', markersize = 8, transform = ccrs.PlateCarree(), label = 'Start')
    ax.plot(df['lon'].iloc[-1], df['lat'].iloc[-1], color = 'coral', marker = 'o', markersize = 8, transform = ccrs.PlateCarree(), label = 'End')

    ax.set_title("Storm Track: " + storm_track.storm_id)
    plt.legend()
    plt.show()

    return fig, ax

def plot_intensity(storm_track):
    """
    Plot storm intensity (wind speed) as a function of time.
    
    Parameters
    ----------
    storm_track: StormTrack
        StormTrack object containing storm data. Must contain a DataFrame attribute 'df' with columns 'time' and 'wind', and an attribute 'storm_id'.
    
    Returns
    -------
    None
    """
    df = storm_track.df
    
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