-- 1. Počet transakcí za měsíc
SELECT t.Year, t.Month, COUNT(*) AS TransactionCount
FROM transaction_fact f
JOIN time_dim t ON f.TimeID = t.TimeID
GROUP BY t.Year, t.Month
ORDER BY t.Year, t.Month;

-- 2. Celkový obrat za jednotlivé roky
SELECT t.Year, SUM(f.TotalValue) AS TotalRevenue
FROM transaction_fact f
JOIN time_dim t ON f.TimeID = t.TimeID
GROUP BY t.Year
ORDER BY t.Year;

-- 3. Sezónnost: obrat podle kvartálu (opravena verze s FLOOR)
SELECT 
    t.Year, 
    FLOOR((CAST(t.Month AS INTEGER) - 1) / 3) + 1 AS Quarter,
    SUM(f.TotalValue) AS QuarterlyRevenue
FROM transaction_fact f
JOIN time_dim t ON f.TimeID = t.TimeID
GROUP BY t.Year, Quarter
ORDER BY t.Year, Quarter;




-- 4. Průměrná denní tržba v jednotlivých měsících
SELECT
    daily_data.Year,
    daily_data.Month,
    AVG(daily_data.DailyRevenue) AS AvgDailyRevenue
FROM (
    SELECT
        t.Year,
        t.Month,
        t.Day,
        SUM(f.TotalValue) AS DailyRevenue
    FROM transaction_fact f
    JOIN time_dim t ON f.TimeID = t.TimeID
    GROUP BY t.Year, t.Month, t.Day
) AS daily_data
GROUP BY daily_data.Year, daily_data.Month
ORDER BY daily_data.Year, daily_data.Month;
