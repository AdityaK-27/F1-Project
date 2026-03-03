import fastf1
import pandas as pd
from pathlib import Path


def enable_cache(cache_dir: str = "data/cache"):
    """
    Enable FastF1 local caching.
    """
    Path(cache_dir).mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(cache_dir)


def load_session(year: int, event: str, session_type: str):
    session = fastf1.get_session(year, event, session_type)
    session.load(laps=True, telemetry=True)
    return session


def extract_laps(session) -> pd.DataFrame:
    """
    Extract lap-level data from a session.
    """
    laps = session.laps.copy()
    return laps