from src.ingest import enable_cache, load_session, extract_laps
from src.storage import save_partitioned_parquet


def main():
    year = 2023
    event = "Bahrain"
    session_type = "R"

    enable_cache()

    session = load_session(year, event, session_type)
    laps = extract_laps(session)

    print(laps.head())
    print(f"\nTotal laps extracted: {len(laps)}")

    save_partitioned_parquet(
        laps,
        base_path="data/raw",
        year=year,
        event=event,
        session_type=session_type
    )


if __name__ == "__main__":
    main()