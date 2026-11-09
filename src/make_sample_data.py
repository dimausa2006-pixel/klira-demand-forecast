"""Create a SIMULATED booking log shaped like a small cleaning company's records.

The numbers are random (fixed seed), not real company data. To run the analysis on real
records, export your own bookings to data/bookings.csv with the same columns and skip this script.
"""
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
start, end = pd.Timestamp("2025-08-04"), pd.Timestamp("2026-10-25")
days = pd.date_range(start, end, freq="D")

rows = []
client_pool = 0
for d in days:
    weeks = (d - start).days / 7
    base = 1.2 + 0.055 * weeks                      # slow growth as the company gets known
    base *= 1.25 if d.weekday() in (4, 5) else 1.0  # Friday/Saturday busier
    base *= 1.3 if d.month in (3, 4, 9) else 1.0    # spring and September peaks
    for _ in range(rng.poisson(base)):
        client_pool += 1
        repeat = rng.random() < 0.35 and client_pool > 20
        client = int(rng.integers(1, client_pool)) if repeat else client_pool
        service = rng.choice(["apartment", "office", "deep_clean"], p=[0.6, 0.15, 0.25])
        hours = {"apartment": 3, "office": 4, "deep_clean": 6}[service] + int(rng.integers(0, 2))
        rate = {"apartment": 9, "office": 11, "deep_clean": 12}[service]
        rows.append({
            "booking_id": len(rows) + 1,
            "date": d.date().isoformat(),
            "client_id": client,
            "service": service,
            "channel": rng.choice(["telegram", "olx", "referral"], p=[0.45, 0.35, 0.20]),
            "hours": hours,
            "revenue": round(hours * rate * rng.uniform(0.9, 1.1), 2),
        })

out = Path(__file__).resolve().parents[1] / "data" / "bookings_sample.csv"
pd.DataFrame(rows).to_csv(out, index=False)
print(f"wrote {len(rows)} simulated bookings to {out}")
