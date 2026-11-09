# Weekly demand forecast for a small cleaning company

A small analytics project: turn a booking log into answers about demand, channels and staffing,
using SQL (SQLite), Python (pandas, NumPy) and a forecast checked on weeks the model has not seen.

**About the data.** `data/bookings_sample.csv` is **simulated** (random numbers, fixed seed),
shaped like the records of a small cleaning service. It is not real company data, and the results below
describe the simulation, not a real business. To run it on real records, put them in `data/bookings.csv`
with the same columns (`booking_id, date, client_id, service, channel, hours, revenue`); the script
uses that file first, and it is git-ignored so private data is never uploaded.

## Questions
1. How many bookings should we expect each week, and how many cleaners does that need?
2. Which acquisition channel brings the most revenue?
3. Which service earns the most per hour?
4. What share of clients come back?

## Method
- `sql/queries.sql`: weekly bookings, channel performance, service mix, repeat-client rate.
- `src/analyze.py`: loads the CSV into SQLite, runs the queries, then compares three forecasts of weekly
  bookings on the last 8 weeks (held out): last value, 4-week average, and a regression with a linear trend
  plus a yearly seasonal cycle. Error is measured with MAE and MAPE.
- Staffing: forecast bookings x average hours per booking / 30 billable hours per cleaner per week
  (30 is an assumption).

## Results on the simulated data
| model | MAE | MAPE % |
|:--|--:|--:|
| last value | 7.38 | 21.1 |
| 4-week average | 4.62 | 11.0 |
| trend + season regression | 5.59 | 13.2 |

The simplest smoothing model won. With only about 60 weeks of data, a seasonal regression has too little
history to learn a yearly cycle, so it does not beat a plain moving average. Full tables are in
`reports/results.md`; the chart is `reports/forecast.png`.

## Limits
- Simulated data: channel and service figures only show the code works.
- About 60 weeks cannot show a yearly pattern reliably.
- No holidays, weather or price changes in the model.
- Next steps: use real data; try exponential smoothing and cross-validation over several time splits.

## Run it
```bash
pip install -r requirements.txt
python src/make_sample_data.py   # skip if you have data/bookings.csv
python src/analyze.py
```
