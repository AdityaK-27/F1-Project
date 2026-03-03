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
    """
    Load a Formula 1 session.
    
    session_type examples:
    'R'  -> Race
    'Q'  -> Qualifying
    'FP1', 'FP2', 'FP3'
    """
    session = fastf1.get_session(year, event, session_type)
    session.load()
    return session


def extract_laps(session) -> pd.DataFrame:
    """
    Extract lap-level data from a session.
    """
    laps = session.laps.copy()
    return laps