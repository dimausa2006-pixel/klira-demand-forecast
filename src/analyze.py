"""Load bookings into SQLite, answer business questions with SQL, then forecast weekly demand."""
import sqlite3
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
csv = ROOT / "data" / ("bookings.csv" if (ROOT / "data" / "bookings.csv").exists() else "bookings_sample.csv")
HOLDOUT = 8  # weeks kept back to test the forecasts


def load_queries():
    queries, name = {}, None
    for line in (ROOT / "sql" / "queries.sql").read_text(encoding="utf-8").splitlines():
        if line.startswith("-- name:"):
            name = line.split(":")[1].strip()
            queries[name] = ""
        elif name:
            queries[name] += line + "\n"
    return queries


def features(n_weeks, start_week_of_year):
    t = np.arange(n_weeks)
    woy = (start_week_of_year + t) % 52
    return np.column_stack([np.ones(n_weeks), t,
                            np.sin(2 * np.pi * woy / 52), np.cos(2 * np.pi * woy / 52)])


def main():
    df = pd.read_csv(csv, parse_dates=["date"])
    con = sqlite3.connect(":memory:")
    df.assign(date=df["date"].dt.strftime("%Y-%m-%d")).to_sql("bookings", con, index=False)
    q = load_queries()
    results = {k: pd.read_sql(v, con) for k, v in q.items()}

    weekly = results["weekly_bookings"].iloc[1:-1].reset_index(drop=True)  # drop partial first/last week
    y = weekly["bookings"].to_numpy(float)
    train, test = y[:-HOLDOUT], y[-HOLDOUT:]
    start_woy = pd.Timestamp(weekly["week_start"].iloc[0]).isocalendar().week

    naive = np.repeat(train[-1], HOLDOUT)
    ma4 = np.repeat(train[-4:].mean(), HOLDOUT)
    X = features(len(y), start_woy)
    beta, *_ = np.linalg.lstsq(X[:-HOLDOUT], train, rcond=None)
    reg = X[-HOLDOUT:] @ beta

    def score(pred):
        return {"MAE": round(float(np.mean(np.abs(test - pred))), 2),
                "MAPE %": round(float(np.mean(np.abs(test - pred) / test) * 100), 1)}

    table = pd.DataFrame({"last value": score(naive), "4-week average": score(ma4),
                          "trend + season regression": score(reg)}).T

    best = table["MAE"].idxmin()
    best_pred = {"last value": naive, "4-week average": ma4, "trend + season regression": reg}[best]
    hours_per_booking = weekly["hours"].sum() / weekly["bookings"].sum()
    staff_hours_week = 30  # assumption: one cleaner works about 30 billable hours a week
    needed = np.ceil(best_pred * hours_per_booking / staff_hours_week).astype(int)

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(range(len(y)), y, color="#16213A", label="actual")
    ax.plot(range(len(y) - HOLDOUT, len(y)), best_pred, color="#C0392B", ls="--", label=f"forecast ({best})")
    ax.axvline(len(y) - HOLDOUT - 0.5, color="grey", lw=0.8)
    ax.set_xlabel("week"); ax.set_ylabel("bookings per week"); ax.legend(); fig.tight_layout()
    (ROOT / "reports").mkdir(exist_ok=True)
    fig.savefig(ROOT / "reports" / "forecast.png", dpi=140)

    md = ["# Results", f"\nData file: `{csv.name}`  |  bookings: {len(df)}  |  weeks: {len(y)}\n",
          "## Forecast accuracy (last 8 weeks held out)\n", table.to_markdown(),
          f"\nBest model by MAE: **{best}**.\n",
          f"## Staffing (assumes {staff_hours_week} billable hours per cleaner per week, "
          f"{hours_per_booking:.1f} hours per booking)\n",
          f"Cleaners needed for the 8 test weeks: {needed.tolist()}\n"]
    for k, v in results.items():
        if k != "weekly_bookings":
            md += [f"## {k.replace('_', ' ')}\n", v.to_markdown(index=False), ""]
    (ROOT / "reports" / "results.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    sys.exit(main())
