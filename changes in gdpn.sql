WITH changes AS (
  SELECT
    year,
    (("gdp(N)" - LAG("gdp(N)") OVER (ORDER BY year ASC))
      / LAG("gdp(N)") OVER (ORDER BY year ASC)) AS new_change
  FROM gdpn
)
UPDATE gdpn AS t
SET "gdp(N) change" = c.new_change
FROM changes AS c
WHERE t.year = c.year;


select * from gdpn;