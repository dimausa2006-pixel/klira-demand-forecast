-- name: weekly_bookings
SELECT strftime('%Y-%W', date) AS week, MIN(date) AS week_start,
       COUNT(*) AS bookings, SUM(hours) AS hours, ROUND(SUM(revenue), 2) AS revenue
FROM bookings GROUP BY week ORDER BY week_start;

-- name: channel_performance
SELECT channel, COUNT(*) AS bookings, COUNT(DISTINCT client_id) AS clients,
       ROUND(SUM(revenue), 2) AS revenue, ROUND(AVG(revenue), 2) AS avg_booking
FROM bookings GROUP BY channel ORDER BY revenue DESC;

-- name: service_mix
SELECT service, COUNT(*) AS bookings, ROUND(AVG(hours), 1) AS avg_hours,
       ROUND(SUM(revenue) / SUM(hours), 2) AS revenue_per_hour
FROM bookings GROUP BY service ORDER BY revenue_per_hour DESC;

-- name: repeat_clients
SELECT ROUND(100.0 * SUM(n > 1) / COUNT(*), 1) AS repeat_client_pct
FROM (SELECT client_id, COUNT(*) AS n FROM bookings GROUP BY client_id);
