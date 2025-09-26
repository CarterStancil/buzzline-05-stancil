import pathlib
import argparse
import matplotlib.pyplot as plt


from consumers.sqlite_consumer_case import get_category_counts_over_time
import utils.utils_config as config


def plot_category_trends(db_path: pathlib.Path, interval="day"):
    """
    Plot category frequencies over time.
    """
    rows = get_category_counts_over_time(db_path, interval=interval)

    if not rows:
        print("No data found in the database.")
        return

    # Convert rows into a dict
    data_by_cat = {}
    for period, category, count in rows:
        data_by_cat.setdefault(category, []).append((period, count))

    # Plot each category
    for category, values in data_by_cat.items():
        periods, counts = zip(*values)
        plt.plot(periods, counts, marker="o", label=category)

    plt.xlabel("Time Period")
    plt.ylabel("Message Count")
    plt.title(f"Category Frequency Over Time ({interval})")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Plot category counts over time from SQLite DB")
    parser.add_argument(
    "--db",
    type=str,
    default="buzz.sqlite",   
    help="SQLite database file name (default: buzz.sqlite)",
    )
    parser.add_argument(
        "--interval",
        type=str,
        choices=["day", "week", "month"],
        default="day",
        help="Time interval for grouping (day, week, month). Default: day",
    )
    args = parser.parse_args()

    
    DATA_PATH: pathlib.Path = config.get_base_data_path()
    DB_PATH: pathlib.Path = DATA_PATH / args.db

    print(f"Using database: {DB_PATH}")
    plot_category_trends(DB_PATH, interval=args.interval)


if __name__ == "__main__":
    main()