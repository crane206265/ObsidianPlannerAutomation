from datetime import datetime, timedelta
from pathlib import Path


MONTH_NAME = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}


def week_of_month(date: datetime) -> int:
    first_day = date.replace(day=1)
    return (date.day + first_day.weekday() - 1) // 7 + 1


def write_md(date: datetime, base_path: Path, overwrite=True) -> None:
    folder_path = (
        base_path
        / str(date.year)
        / f"{MONTH_NAME[date.month]}. {date.year}"
        / f"{MONTH_NAME[date.month]}. Week {week_of_month(date)}"
    )

    date_str = date.strftime("%Y-%m-%d")
    prev_str = (date - timedelta(days=1)).strftime("%Y-%m-%d")
    next_str = (date + timedelta(days=1)).strftime("%Y-%m-%d")

    folder_path.mkdir(parents=True, exist_ok=True)

    file_path = folder_path / f"{date_str}.md"

    if file_path.exists() and not overwrite:
        return
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"Prev : [[{prev_str}]]\n")
        f.write(f"Next : [[{next_str}]]\n")
        f.write("\n")


def main(start_date: str, end_date: str, base_path: str, overwrite=True) -> None:
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    base_path = Path(base_path)

    current = start_dt
    while current <= end_dt:   # end_date 포함
        write_md(current, base_path, overwrite=True)
        current += timedelta(days=1)


if __name__ == "__main__":
    base_path = r"C:\Users\dlgkr\OneDrive\문서\Obsidian\Planner"
    start_date = "2026-05-01"
    end_date = "2026-06-30"

    main(start_date, end_date, base_path, overwrite=True)