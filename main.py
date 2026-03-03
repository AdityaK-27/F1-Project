from pathlib import Path
from src.ingest import enable_cache, load_session, extract_laps
from src.storage import save_partitioned_parquet, load_partitioned_parquet


def data_exists(base_path, year, event, session_type):
    path = (
        Path(base_path)
        / f"year={year}"
        / f"event={event}"
        / f"session={session_type}"
        / "laps.parquet"
    )
    return path.exists()


def main():
    year = 2023
    event = "Bahrain"
    session_type = "R"
    base_path = "data/raw"

    enable_cache()

    # Only ingest if dataset not already stored
    if not data_exists(base_path, year, event, session_type):
        print("Dataset not found. Ingesting from FastF1...")
        session = load_session(year, event, session_type)
        laps = extract_laps(session)

        save_partitioned_parquet(
            laps,
            base_path=base_path,
            year=year,
            event=event,
            session_type=session_type
        )
    else:
        print("Dataset already exists. Skipping ingestion.")

    # Load dataset for analytics
    laps_df = load_partitioned_parquet(
        base_path=base_path,
        year=year,
        event=event,
        session_type=session_type
    )

    print(laps_df.head())
    print(f"\nTotal laps loaded: {len(laps_df)}")


if __name__ == "__main__":
    main()