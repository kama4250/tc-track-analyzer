import math
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.collections import LineCollection


def haversine(lat1, lon1, lat2, lon2):
    """
    Compute the great-circle distance between two points on Earth.
    """
    R = 6371  # km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def plot_track(storm_track, save_path=None, show=True):
    """
    Plot the geographic track of a storm on a map.

    Parameters
    ----------
    storm_track : StormTrack
    save_path : str, optional
    show : bool, optional

    Returns
    -------
    fig, ax
    """
    df = storm_track.df

    fig, ax = plt.subplots(
        figsize=(8, 10),
        subplot_kw={"projection": ccrs.PlateCarree()},
        constrained_layout=True,
    )

    # map features
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle="--", alpha=0.5)
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    ax.add_feature(cfeature.OCEAN, facecolor="lightblue")

    # extent
    padding = 5
    ax.set_extent(
        [
            df["lon"].min() - padding,
            df["lon"].max() + padding,
            df["lat"].min() - padding,
            df["lat"].max() + padding,
        ],
        crs=ccrs.PlateCarree(),
    )

    # colored line segments
    points = np.array([df["lon"], df["lat"]]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    lc = LineCollection(segments, cmap="plasma", linewidth=3)
    lc.set_array(df["wind"].values)
    ax.add_collection(lc)

    plt.colorbar(lc, ax=ax, label="Wind Speed (kts)")

    # start/end
    ax.plot(df["lon"].iloc[0], df["lat"].iloc[0], "go", label="Start")
    ax.plot(df["lon"].iloc[-1], df["lat"].iloc[-1], "ro", label="End")

    ax.set_title(f"Storm Track: {storm_track.storm_id}")
    plt.legend()

    if save_path:
        fig.savefig(save_path, dpi=300)

    if show:
        plt.show()

    return fig, ax


def plot_intensity(storm_track, save_path=None, show=True):
    """
    Plot wind speed vs time.

    Parameters
    ----------
    storm_track : StormTrack
    save_path : str, optional
    show : bool, optional

    Returns
    -------
    fig, ax
    """
    df = storm_track.df

    fig, ax = plt.subplots()
    ax.plot(df["time"], df["wind"], marker="o")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))

    plt.xticks(rotation=45)
    ax.set_xlabel("Time")
    ax.set_ylabel("Wind Speed (kts)")
    ax.set_title(f"Intensity: {storm_track.storm_id}")
    ax.grid()

    if save_path:
        fig.savefig(save_path, dpi=300)

    if show:
        plt.show()

    return fig, ax