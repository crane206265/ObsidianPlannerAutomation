from datetime import datetime, timedelta
from pathlib import Path
import argparse


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

WEEKDAY_NAME = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"


def week_of_month(date: datetime) -> int:
    first_day = date.replace(day=1)
    return (date.day + first_day.weekday() - 1) // 7 + 1


def validate_templates(template_dir: Path) -> None:
    missing = []
    for day in WEEKDAY_NAME:
        path = template_dir / f"{day}.md"
        if not path.exists():
            missing.append(path)

    if missing:
        raise FileNotFoundError(
            "Missing templates:\n" + "\n".join(str(p) for p in missing)
        )


def get_month_folder_path(date: datetime, base_path: Path) -> Path:
    return base_path / str(date.year) / f"{MONTH_NAME[date.month]}. {date.year}"


def get_week_folder_path(date: datetime, base_path: Path) -> Path:
    return (
        get_month_folder_path(date, base_path)
        / f"{MONTH_NAME[date.month]}. Week {week_of_month(date)}"
    )


def write_day_note(
    date: datetime,
    base_path: Path,
    overwrite: bool = True,
    dry_run: bool = False,
) -> None:
    folder_path = get_week_folder_path(date, base_path)

    date_str = date.strftime("%Y-%m-%d")
    prev_str = (date - timedelta(days=1)).strftime("%Y-%m-%d")
    next_str = (date + timedelta(days=1)).strftime("%Y-%m-%d")

    file_path = folder_path / f"{date_str}.md"

    weekday = WEEKDAY_NAME[date.weekday()]
    template_path = TEMPLATE_DIR / f"{weekday}.md"

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    if file_path.exists() and not overwrite:
        print(f"[SKIP] {file_path}")
        return

    if dry_run:
        action = "OVERWRITE" if file_path.exists() else "CREATE"
        print(f"[DRY RUN] {action} day note: {file_path}")
        return

    folder_path.mkdir(parents=True, exist_ok=True)
    template_text = template_path.read_text(encoding="utf-8")

    nav_block = (
        f"Prev : [[{prev_str}]]\n"
        f"Next : [[{next_str}]]\n\n"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(nav_block)
        f.write(template_text)

    print(f"[OK] Wrote day note: {file_path}")


def month_dates_in_range(start_dt: datetime, end_dt: datetime):
    current = start_dt.replace(day=1)
    while current <= end_dt:
        yield current.year, current.month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1, day=1)
        else:
            current = current.replace(month=current.month + 1, day=1)


def write_month_note(
    year: int,
    month: int,
    base_path: Path,
    overwrite: bool = True,
    dry_run: bool = False,
) -> None:
    month_dt = datetime(year, month, 1)
    month_folder = get_month_folder_path(month_dt, base_path)
    month_note_path = month_folder / f"{MONTH_NAME[month]}. {year}.md"

    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)

    last_day = (next_month - timedelta(days=1)).day

    lines = []
    lines.append("### Notes\n\n")

    for day in range(1, last_day + 1):
        date_str = datetime(year, month, day).strftime("%Y-%m-%d")
        lines.append(f"- [[{date_str}]]\n")

    content = "".join(lines)

    if month_note_path.exists() and not overwrite:
        print(f"[SKIP] {month_note_path}")
        return

    if dry_run:
        action = "OVERWRITE" if month_note_path.exists() else "CREATE"
        print(f"[DRY RUN] {action} month note: {month_note_path}")
        return

    month_folder.mkdir(parents=True, exist_ok=True)
    month_note_path.write_text(content, encoding="utf-8")

    print(f"[OK] Wrote month note: {month_note_path}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Obsidian Day Planner notes."
    )
    parser.add_argument(
        "--base-path",
        required=True,
        help="Path to the Obsidian vault planner root",
    )
    parser.add_argument(
        "--start-date",
        required=True,
        help="Start date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--end-date",
        required=True,
        help="End date in YYYY-MM-DD format (inclusive)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without writing files",
    )
    parser.add_argument(
        "--generate-month-notes",
        action="store_true",
        help="Also generate month notes",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    start_dt = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(args.end_date, "%Y-%m-%d")
    base_path = Path(args.base_path)

    if end_dt < start_dt:
        raise ValueError("end-date must be greater than or equal to start-date")

    validate_templates(TEMPLATE_DIR)

    current = start_dt
    while current <= end_dt:
        write_day_note(
            current,
            base_path,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
        )
        current += timedelta(days=1)

    if args.generate_month_notes:
        for year, month in month_dates_in_range(start_dt, end_dt):
            write_month_note(
                year,
                month,
                base_path,
                overwrite=args.overwrite,
                dry_run=args.dry_run,
            )


if __name__ == "__main__":
    main()