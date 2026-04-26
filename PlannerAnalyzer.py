import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from contextlib import nullcontext
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


# ------------------------------ CONFIG ------------------------------

# allowed format: - [ ] xx:xx - xx:xx contents
# allowed format: - [x] xx:xx - xx:xx contents
PLANNER_PATTERN = re.compile(
    r"^- \[(?P<done>[ xX])\]\s+"
    r"(?P<start>\d{2}:\d{2})\s*-\s*"
    r"(?P<end>\d{2}:\d{2})\s+"
    r"(?P<content>.+)$"
)

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


# ------------------------------ FONT SETUP ------------------------------

KOREAN_FONT_PROP = None


def setup_korean_font(weight: str = "bold") -> None:
    """
    Set a Korean-capable matplotlib font.

    xkcd style overrides font settings, so this function stores a FontProperties
    object and each graph function reapplies it directly to title, labels,
    ticks, and legend.
    """
    global KOREAN_FONT_PROP

    font_candidates = [
        r"C:\Windows\Fonts\malgunbd.ttf",        # Windows: Malgun Gothic Bold
        r"C:\Windows\Fonts\malgun.ttf",          # Windows: Malgun Gothic
        r"C:\Windows\Fonts\malgunsl.ttf",        # Windows: Malgun Gothic Semilight
        "/System/Library/Fonts/AppleGothic.ttf", # macOS
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]

    for font_path in font_candidates:
        path = Path(font_path)
        if path.exists():
            KOREAN_FONT_PROP = fm.FontProperties(fname=str(path), weight=weight)
            plt.rcParams["font.family"] = KOREAN_FONT_PROP.get_name()
            plt.rcParams["font.weight"] = weight
            print(f"[FONT] Using Korean font: {KOREAN_FONT_PROP.get_name()} ({weight})")
            break

    if KOREAN_FONT_PROP is None:
        print("[WARNING] Korean font not found. Korean text may be broken.")

    plt.rcParams["axes.unicode_minus"] = False


def apply_korean_font_to_axes(ax, weight: str = "bold") -> None:
    """
    Reapply Korean font after plotting.

    This is especially important with plt.xkcd(), because xkcd style changes
    the font family and can break Korean text rendering.
    """
    if KOREAN_FONT_PROP is None:
        return

    ax.title.set_fontproperties(KOREAN_FONT_PROP)
    ax.title.set_fontweight(weight)

    ax.xaxis.label.set_fontproperties(KOREAN_FONT_PROP)
    ax.yaxis.label.set_fontproperties(KOREAN_FONT_PROP)
    ax.xaxis.label.set_fontweight(weight)
    ax.yaxis.label.set_fontweight(weight)

    for label in ax.get_xticklabels():
        label.set_fontproperties(KOREAN_FONT_PROP)
        label.set_fontweight(weight)

    for label in ax.get_yticklabels():
        label.set_fontproperties(KOREAN_FONT_PROP)
        label.set_fontweight(weight)

    legend = ax.get_legend()
    if legend is not None:
        for text in legend.get_texts():
            text.set_fontproperties(KOREAN_FONT_PROP)
            text.set_fontweight(weight)


# ------------------------------ BASIC UTILS ------------------------------

def week_of_month(date: datetime) -> int:
    first_day = date.replace(day=1)
    return (date.day + first_day.weekday() - 1) // 7 + 1


def get_day_note_path(date: datetime, base_path: Path) -> Path:
    return (
        base_path
        / str(date.year)
        / f"{MONTH_NAME[date.month]}. {date.year}"
        / f"{MONTH_NAME[date.month]}. Week {week_of_month(date)}"
        / f"{date.strftime('%Y-%m-%d')}.md"
    )


# ------------------------------ PARSING ------------------------------

def parse_planner_line(line: str):
    match = PLANNER_PATTERN.match(line.strip())
    if not match:
        return None

    start = datetime.strptime(match.group("start"), "%H:%M")
    end = datetime.strptime(match.group("end"), "%H:%M")

    duration_min = int((end - start).total_seconds() // 60)

    return {
        "done": match.group("done").lower() == "x",
        "start": match.group("start"),
        "end": match.group("end"),
        "duration_min": duration_min,
        "content": match.group("content"),
    }


def parse_planner_file(path: Path):
    records = []

    for line in path.read_text(encoding="utf-8").splitlines():
        parsed = parse_planner_line(line)
        if parsed is not None:
            parsed["file"] = path.name
            records.append(parsed)

    return records


def parse_planner_range(start_date: str, end_date: str, base_path: Path):
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    if end_dt < start_dt:
        raise ValueError("end_date must be greater than or equal to start_date")

    all_records = []
    missing_files = []

    current = start_dt
    while current <= end_dt:
        path = get_day_note_path(current, base_path)

        if path.exists():
            records = parse_planner_file(path)
            date_str = current.strftime("%Y-%m-%d")

            for record in records:
                record["date"] = date_str

            all_records.extend(records)
        else:
            missing_files.append(path)

        current += timedelta(days=1)

    return all_records, missing_files


# ------------------------------ CATEGORY BUILDER ------------------------------

def category_keys(records, categories: list):
    keys = defaultdict(set)

    for record in records:
        lowered = record["content"].lower()

        for category in categories:
            if lowered.endswith(category.lower()) or lowered.startswith(category.lower()):
                keys[category].add(lowered)
            else:
                keys[category]  # keep empty category

    return keys


def generate_category_keywords(raw_category_keys: dict, option=None):
    candidates = []

    for _, values in raw_category_keys.items():
        for value in values:
            candidates.append(value)

    if option is None:
        category_keywords = {}
        for idx, value in enumerate(candidates):
            category_keywords[str(idx)] = {value}
        return category_keywords

    if option == "interactive":
        category_keywords = {}
        used = set()

        print("\nDetected category candidates:")
        for idx, value in enumerate(candidates):
            print(f"[{idx}] {value}")

        print("\nEnter indices to merge.")
        print("Example: 0 1 3")
        print("Press Enter without input to finish.\n")

        while True:
            user_input = input("Merge indices: ").strip()

            if user_input == "":
                break

            try:
                indices = [int(x) for x in user_input.split()]
            except ValueError:
                print("Invalid input. Please enter numbers separated by spaces.")
                continue

            invalid = [i for i in indices if i < 0 or i >= len(candidates)]
            if invalid:
                print(f"Invalid indices: {invalid}")
                continue

            already_used = [i for i in indices if i in used]
            if already_used:
                print(f"Already used indices: {already_used}")
                continue

            category_name = input("Category name: ").strip()
            if category_name == "":
                print("Category name cannot be empty.")
                continue

            category_keywords[category_name] = {candidates[i] for i in indices}
            used.update(indices)

        # merge 안 한 나머지 후보들은 각각 독립 category로 둠
        suffixes = list(raw_category_keys.keys())

        for idx, value in enumerate(candidates):
            if idx not in used:
                category_name = value

                for suffix in suffixes:
                    category_name = category_name.removesuffix(" " + suffix.lower())
                    category_name = category_name.removesuffix(suffix.lower())

                category_keywords[category_name] = {value}

        return category_keywords

    raise ValueError(f"Unknown option: {option}")


# ------------------------------ CLASSIFIER / SUMMARIZER ------------------------------

def classify_content(content: str, category_keywords: dict) -> str:
    lowered = content.lower()

    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword.lower() in lowered:
                return category

    return "uncategorized"


def filter_uncategorized_summary(summary: dict, exclude_uncategorized: bool = False):
    if not exclude_uncategorized:
        return dict(summary)

    return {
        category: value
        for category, value in summary.items()
        if category != "uncategorized"
    }


def summarize_by_category(
    records,
    category_keywords: dict,
    exclude_uncategorized: bool = False,
):
    summary = defaultdict(int)

    for record in records:
        category = classify_content(record["content"], category_keywords)
        summary[category] += record["duration_min"]

    return filter_uncategorized_summary(summary, exclude_uncategorized)


def summarize_daily_by_category(
    records,
    category_keywords: dict,
    exclude_uncategorized: bool = False,
):
    daily_summary = {}

    for record in records:
        date = record["date"]
        category = classify_content(record["content"], category_keywords)

        if exclude_uncategorized and category == "uncategorized":
            continue

        if date not in daily_summary:
            daily_summary[date] = defaultdict(int)

        daily_summary[date][category] += record["duration_min"]

    return {
        date: dict(summary)
        for date, summary in daily_summary.items()
    }


# ------------------------------ VISUALIZER ------------------------------

def draw_category_bar_graph(
    summary: dict,
    title="Planner Summary",
    xkcd=True,
    exclude_uncategorized: bool = False,
    font_weight: str = "bold",
):
    summary = filter_uncategorized_summary(summary, exclude_uncategorized)

    if not summary:
        print("No data to visualize.")
        return

    categories = list(summary.keys())
    hours = [summary[category] / 60 for category in categories]

    context = plt.xkcd() if xkcd else nullcontext()

    with context:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(categories, hours)
        ax.set_xlabel("Category")
        ax.set_ylabel("Hours")
        ax.set_title(title)
        ax.tick_params(axis="x", rotation=30)

        for label in ax.get_xticklabels():
            label.set_ha("right")

        apply_korean_font_to_axes(ax, weight=font_weight)

        fig.tight_layout()
        plt.show()


def draw_daily_category_line_graph(
    daily_summary: dict,
    xkcd=True,
    exclude_uncategorized: bool = False,
    font_weight: str = "bold",
):
    if exclude_uncategorized:
        daily_summary = {
            date: {
                category: value
                for category, value in summary.items()
                if category != "uncategorized"
            }
            for date, summary in daily_summary.items()
        }

    daily_summary = {
        date: summary
        for date, summary in daily_summary.items()
        if summary
    }

    if not daily_summary:
        print("No data to visualize.")
        return

    dates = sorted(daily_summary.keys())

    categories = set()
    for summary in daily_summary.values():
        categories.update(summary.keys())

    context = plt.xkcd() if xkcd else nullcontext()

    with context:
        fig, ax = plt.subplots(figsize=(12, 6))

        for category in sorted(categories):
            hours = [
                daily_summary[date].get(category, 0) / 60
                for date in dates
            ]
            ax.plot(dates, hours, marker="o", label=category)

        ax.set_xlabel("Date")
        ax.set_ylabel("Hours")
        ax.set_title("Daily Planner Summary by Category")
        ax.tick_params(axis="x", rotation=45)
        ax.legend()

        for label in ax.get_xticklabels():
            label.set_ha("right")

        apply_korean_font_to_axes(ax, weight=font_weight)

        fig.tight_layout()
        plt.show()


# ------------------------------ CLI ------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze Obsidian Day Planner notes and visualize time usage."
    )

    parser.add_argument(
        "--base-path",
        required=True,
        help="Path to the Obsidian Planner root directory",
    )
    parser.add_argument(
        "--start-date",
        required=True,
        help="Start date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--end-date",
        required=True,
        help="End date in YYYY-MM-DD format, inclusive",
    )
    parser.add_argument(
        "--categories",
        nargs="+",
        default=["공부", "연습"],
        help="Suffix categories used to detect candidate tasks, e.g. 공부 연습",
    )
    parser.add_argument(
        "--exclude-uncategorized",
        action="store_true",
        help="Exclude uncategorized records from summaries and graphs",
    )
    parser.add_argument(
        "--no-xkcd",
        action="store_true",
        help="Disable xkcd graph style",
    )
    parser.add_argument(
        "--font-weight",
        default="bold",
        choices=["normal", "bold", "heavy"],
        help="Font weight for graph text",
    )
    parser.add_argument(
        "--category-mode",
        default="interactive",
        choices=["interactive", "auto"],
        help="How to generate category keywords",
    )
    parser.add_argument(
        "--show-missing",
        action="store_true",
        help="Print missing daily note files in the selected date range",
    )

    return parser.parse_args()


# ------------------------------ MAIN ------------------------------

def main():
    args = parse_args()

    setup_korean_font(weight=args.font_weight)

    base_path = Path(args.base_path)
    xkcd = not args.no_xkcd
    category_mode = None if args.category_mode == "auto" else "interactive"

    records, missing_files = parse_planner_range(
        start_date=args.start_date,
        end_date=args.end_date,
        base_path=base_path,
    )

    if args.show_missing and missing_files:
        print("\nMissing files:")
        for path in missing_files:
            print(f"[MISSING] {path}")

    raw_category_keys = category_keys(records, args.categories)
    category_keywords = generate_category_keywords(raw_category_keys, option=category_mode)

    summary = summarize_by_category(
        records,
        category_keywords,
        exclude_uncategorized=args.exclude_uncategorized,
    )

    print("\nCategory Keywords:")
    print(category_keywords)

    print("\nSummary:")
    print(summary)

    title = f"{args.start_date} ~ {args.end_date} Planner Summary"

    draw_category_bar_graph(
        summary,
        title=title,
        xkcd=xkcd,
        exclude_uncategorized=args.exclude_uncategorized,
        font_weight=args.font_weight,
    )

    daily_summary = summarize_daily_by_category(
        records,
        category_keywords,
        exclude_uncategorized=args.exclude_uncategorized,
    )

    draw_daily_category_line_graph(
        daily_summary,
        xkcd=xkcd,
        exclude_uncategorized=args.exclude_uncategorized,
        font_weight=args.font_weight,
    )


if __name__ == "__main__":
    main()
