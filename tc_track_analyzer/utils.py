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


def plot_track(storm_track, save_path=None, show=True):
    """
    Plot the geographic track of a storm on a map.

    Parameters
    ----------
    storm_track: StormTrack
        StormTrack object containing storm data. Must include a DataFrame
        attribute 'df' with columns 'lat', 'lon', and 'wind', and an
        attribute 'storm_id'.
    save_path : str, optional
        If provided, saves the figure to this path.
    show : bool, optional
        If True, displays the figure.

    Returns
    -------
    tuple
        (fig, ax) where:
        - fig: matplotlib.figure.Figure
        - ax: cartopy GeoAxes
    """
    df = storm_track.df

    fig, ax = plt.subplots(
        figsize=(8, 10),
        subplot_kw={'projection': ccrs.PlateCarree()},
        constrained_layout=True
    )

    # Map features
    ax.coastlines(linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5, linestyle='--')
    ax.add_feature(cfeature.LAND, facecolor='gray', alpha=0.3)
    ax.add_feature(cfeature.STATES, edgecolor='gray', linewidth=0.5, alpha=0.2)
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5)

    # Map extent
    padding = 5
    ax.set_extent([
        df['lon'].min() - padding,
        df['lon'].max() + padding,
        df['lat'].min() - padding,
        df['lat'].max() + padding
    ], crs=ccrs.PlateCarree())

    # Line segments colored by wind
    points = np.array([df['lon'], df['lat']]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    lc = LineCollection(
        segments,
        cmap="plasma",
        transform=ccrs.PlateCarree(),
        linewidth=3
    )
    lc.set_array(df['wind'].values)
    ax.add_collection(lc)

    plt.colorbar(lc, ax=ax, label='Wind Speed (kts)', shrink=0.5)

    # Start/end markers
    ax.plot(df['lon'].iloc[0], df['lat'].iloc[0],
            color='limegreen', marker='o', markersize=8,
            transform=ccrs.PlateCarree(), label='Start')

    ax.plot(df['lon'].iloc[-1], df['lat'].iloc[-1],
            color='coral', marker='o', markersize=8,
            transform=ccrs.PlateCarree(), label='End')

    ax.set_title("Storm Track: " + storm_track.storm_id)
    plt.legend()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()

    return fig, ax


def plot_intensity(storm_track, save_path=None, show=True):
    """
    Plot storm intensity (wind speed) as a function of time.

    Parameters
    ----------
    storm_track: StormTrack
        StormTrack object containing storm data. Must contain a DataFrame
        attribute 'df' with columns 'time' and 'wind', and an attribute
        'storm_id'.
    save_path : str, optional
        If provided, saves the figure to this path.
    show : bool, optional
        If True, displays the figure.

    Returns
    -------
    tuple
        (fig, ax) where:
        - fig: matplotlib.figure.Figure
        - ax: matplotlib.axes.Axes
    """
    df = storm_track.df

    fig, ax = plt.subplots()
    ax.plot(df['time'], df['wind'], marker='o')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    ax.xaxis.set_major_locator(mdates.DayLocator())

    plt.xticks(rotation=45)
    ax.set_xlabel("Time")
    ax.set_ylabel("Wind Speed (kts)")
    ax.set_title("Intensity: " + storm_track.storm_id)
    ax.grid()
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()

    return fig, ax