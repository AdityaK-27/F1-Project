import pandas as pd


def filter_quicklaps(laps: pd.DataFrame) -> pd.DataFrame:
    """
    Filter accurate, non-deleted quick laps.
    """
    return laps[
        (laps["IsAccurate"] == True) &
        (laps["Deleted"] == False)
    ].copy()


def calculate_average_lap_time(laps: pd.DataFrame, driver: str):
    """
    Calculate average lap time for a driver.
    """
    driver_laps = laps[laps["Driver"] == driver]
    return driver_laps["LapTime"].mean()


def lap_delta(laps: pd.DataFrame, driver1: str, driver2: str):
    """
    Compute average lap delta between two drivers in seconds.
    Positive delta means driver1 slower than driver2.
    """
    laps = filter_quicklaps(laps)

    avg1 = calculate_average_lap_time(laps, driver1)
    avg2 = calculate_average_lap_time(laps, driver2)

    delta = avg1 - avg2

    # Convert to seconds (float)
    return delta.total_seconds()


def sector_analysis(laps: pd.DataFrame, driver: str):
    """
    Compute formatted average sector times for a driver.
    """
    laps = filter_quicklaps(laps)
    driver_laps = laps[laps["Driver"] == driver]

    sector_avgs = {
        "Sector1_avg": driver_laps["Sector1Time"].mean(),
        "Sector2_avg": driver_laps["Sector2Time"].mean(),
        "Sector3_avg": driver_laps["Sector3Time"].mean(),
    }

    # Format sector times
    formatted_sectors = {
        k: format_sector_time(v)
        for k, v in sector_avgs.items()
    }

    return formatted_sectors


def format_timedelta(td):
    """
    Convert pandas Timedelta to mm:ss.mmm format.
    """
    if pd.isna(td):
        return None

    total_seconds = td.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60

    return f"{minutes}:{seconds:06.3f}"

def format_sector_time(td):
    """
    Convert Timedelta to seconds.milliseconds format.
    Example: 31.151 s
    """
    if pd.isna(td):
        return None

    return f"{td.total_seconds():.3f} s"


def tire_stint_analysis(laps: pd.DataFrame, driver: str):
    """
    Analyze average lap time per stint and compound.
    Returns formatted lap times (mm:ss.mmm).
    """
    laps = filter_quicklaps(laps)
    driver_laps = laps[laps["Driver"] == driver]

    stint_summary = (
        driver_laps
        .groupby(["Stint", "Compound"])
        .agg(
            AvgLapTime=("LapTime", "mean"),
            LapCount=("LapNumber", "count")
        )
        .reset_index()
    )

    # Format lap time for readability
    stint_summary["AvgLapTime"] = stint_summary["AvgLapTime"].apply(format_timedelta)

    return stint_summary