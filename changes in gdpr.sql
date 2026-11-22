WITH changes AS (
  SELECT
    year,
    (("gdp(r)" - LAG("gdp(r)") OVER (ORDER BY year ASC))
      / LAG("gdp(r)") OVER (ORDER BY year ASC)) AS new_change
  FROM gdpr
)
UPDATE gdpr AS t
SET "gdp(r) change" = c.new_change
FROM changes AS c
WHERE t.year = c.year;


select * from gdpr;