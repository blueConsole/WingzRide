# Django REST API

## Bonus SQL Report

```sql
WITH trip_events AS (
    SELECT
        r.id_ride,
        r.id_driver,
        MIN(CASE
            WHEN re.description = 'Status changed to pickup'
            THEN re.created_at
        END) AS pickup_at,
        MIN(CASE
            WHEN re.description = 'Status changed to dropoff'
            THEN re.created_at
        END) AS dropoff_at
    FROM api_ride AS r
    INNER JOIN api_rideevent AS re
        ON re.id_ride = r.id_ride
    WHERE re.description IN (
        'Status changed to pickup',
        'Status changed to dropoff'
    )
    GROUP BY
        r.id_ride,
        r.id_driver
)
SELECT
    strftime('%Y-%m', pickup_at) AS month,
    TRIM(u.first_name || ' ' || u.last_name) AS driver,
    COUNT(*) AS "count_of_trips_gt_1_hr"
FROM trip_events AS te
INNER JOIN api_user AS u
    ON u.id_user = te.id_driver
WHERE
    te.pickup_at IS NOT NULL
    AND te.dropoff_at IS NOT NULL
    AND ((julianday(te.dropoff_at) - julianday(te.pickup_at)) * 24) > 1
GROUP BY
    strftime('%Y-%m', pickup_at),
    u.id_user,
    u.first_name,
    u.last_name
ORDER BY
    month,
    driver;
```
