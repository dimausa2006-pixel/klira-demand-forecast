# Results

Data file: `bookings_sample.csv`  |  bookings: 1556  |  weeks: 63

## Forecast accuracy (last 8 weeks held out)

|                           |   MAE |   MAPE % |
|:--------------------------|------:|---------:|
| last value                |  7.38 |     21.1 |
| 4-week average            |  4.62 |     11   |
| trend + season regression |  5.59 |     13.2 |

Best model by MAE: **4-week average**.

## Staffing (assumes 30 billable hours per cleaner per week, 4.4 hours per booking)

Cleaners needed for the 8 test weeks: [6, 6, 6, 6, 6, 6, 6, 6]

## channel performance

| channel   |   bookings |   clients |   revenue |   avg_booking |
|:----------|-----------:|----------:|----------:|--------------:|
| telegram  |        708 |       621 |   32298.8 |         45.62 |
| olx       |        538 |       474 |   23764.8 |         44.17 |
| referral  |        310 |       288 |   14135.4 |         45.6  |

## service mix

| service    |   bookings |   avg_hours |   revenue_per_hour |
|:-----------|-----------:|------------:|-------------------:|
| deep_clean |        372 |         6.5 |              11.98 |
| office     |        212 |         4.5 |              11.02 |
| apartment  |        972 |         3.5 |               9.01 |

## repeat clients

|   repeat_client_pct |
|--------------------:|
|                27.5 |
