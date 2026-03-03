from pathlib import Path
from src.ingest import enable_cache, load_session, extract_laps
from src.storage import save_partitioned_parquet, load_partitioned_parquet
from src.visualization import animate_race

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

    from src.analytics import lap_delta, sector_analysis, tire_stint_analysis


    # ===== Analytics Section =====
    print("\n--- DRIVER COMPARISON ---")

    delta = lap_delta(laps_df, "VER", "LEC")
    print(f"Average Lap Delta (VER - LEC): {delta}")

    print("\n--- SECTOR ANALYSIS (VER) ---")
    sectors = sector_analysis(laps_df, "VER")

    print("\n--- SECTOR ANALYSIS (VER) ---")
    for sector, value in sectors.items():
        print(f"{sector.replace('_avg', '').replace('Sector', 'Sector ')} Avg: {value}")

    print("\n--- TIRE STINT ANALYSIS (VER) ---")
    stint_data = tire_stint_analysis(laps_df, "VER")
    print(stint_data)


    print(f"\nDataset loaded successfully | Rows: {len(laps_df)}")

    print("\nLaunching track animation...")
    session = load_session(year, event, session_type)
    animate_race(session, drivers=["VER", "LEC", "HAM"])


if __name__ == "__main__":
    main()