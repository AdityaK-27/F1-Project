from pathlib import Path
import pandas as pd


def save_partitioned_parquet(
    df: pd.DataFrame,
    base_path: str,
    year: int,
    event: str,
    session_type: str,
    dataset_name: str = "laps"
):
    """
    Save dataframe in partitioned parquet format:
    data/raw/year=2023/event=Bahrain/session=R/laps.parquet
    """

    path = Path(base_path) / f"year={year}" / f"event={event}" / f"session={session_type}"
    path.mkdir(parents=True, exist_ok=True)

    file_path = path / f"{dataset_name}.parquet"
    df.to_parquet(file_path, engine="pyarrow")

    print(f"Saved dataset to: {file_path}")