import pandas as pandas
import numpy as numpy
import matplotlib.pyplot as plt

date_cols = [
    "action_date", "phase_start", "phase_end", "prev_deadline_date", "next_deadline_date",
]

boolean_cols = [
    "recess", "in_recess", "floor_session_only", "is_holiday", "is_deadline_day",
]

category_cols = [
    "bill_param", "bill_session", "bill_session_code", "calendar_session", "phase", "prev_deadline", "next_deadline",
]

number_cols = [
    "seq", "bill_year_of_session", "calendar_session_year", "calendar_year", "phase_ordinal", "phase_n_days", "days_into_phase", "phase_progress",
    "days_since_prev_deadline", "days_to_next_deadline",
    "days_to_house_of_origin_deadline", "days_to_final_passage_deadline",
]

df = pandas.read_csv("action_calendar_features.csv", parse_dates=date_cols,)


def plot_bool_pie(df, column, title=None):
    import matplotlib.pyplot as plt
    counts = df[column].value_counts(dropna=False)
    labels = counts.index.astype(str)
    values = counts.values

    palette = ["#4C72B0", "#DD8452", "#C44E52"]
    colors = palette[:len(values)]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
    )
    # Get all cols, make doc
    ax.set_title(title or f"Distribution of {column}")
    ax.axis("equal")

    plt.tight_layout()
    plt.legend()
    plt.subplots_adjust(top=0.85)
    plt.show()


def plot_bar_chart(df, column, title=None, top_n=None):
    import matplotlib.pyplot as plt
    counts = df[column].value_counts(dropna=False)
    if top_n is not None:
        counts = counts.head(top_n)
    labels = counts.index.astype(str)
    values = counts.values
    fig, ax = plt.subplots(figsize=(6, 6))
    bars = ax.bar(
        labels,
        values,
        color="#4C72B0"
    )
    ax.set_ylim(0, max(values) * 1.15)
    ax.bar_label(bars, fmt="%d")
    ax.set_title(f"Distribution of {column}")
    ax.set_xlabel(f"{column}")
    ax.set_ylabel("Count")
    ax.tick_params(axis="x", rotation=90)

    plt.subplots_adjust(bottom=0.35)
    plt.tight_layout()
    plt.legend()
    plt.show()


def plot_by_date_bar(df, column, title=None):
    import matplotlib.pyplot as plt
    import calendar
    # df[column] selects a single column, using what is passed from the function(df, column)
    # .dt is the datetime accessor. Like how .str gives you string tools, .dt gives you datetime tools
    # .month gives you an integer for month. So, .month.value_counts() makes a tally of how many times a unique month appears
    # Then, sort_index() sorts the month counts by index number.
    month_counts = df[column].dt.month.value_counts().sort_index()
    # .reindex forces a list to follow indexing rules given in range(), and fill_value makes it so NaN values become 0.
    month_counts = month_counts.reindex(range(1, 13), fill_value=0)
    labels = []
    for m in month_counts.index:
        labels.append(calendar.month_abbr[m])
    # .values pulls the raw numbers out of the series as a NumPy array, no index
    values = month_counts.values

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, values, color="#4C72B0")
    ax.set_ylim(0, max(values) * 1.40)
    # fmt is a format package, %d converts a number to an integer
    ax.bar_label(bars, fmt="%d")
    ax.set_ylabel("Count")
    ax.set_xlabel("Month")

    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.title(f"{column} Date Month Distribution")
    plt.show()

