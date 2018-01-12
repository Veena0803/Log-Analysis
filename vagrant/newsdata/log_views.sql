CREATE OR REPLACE VIEW final_log_view AS 
SELECT to_char((time::date), 'Mon,DD YYYY'), (100 * sum(case when status != '200 OK' then 1 else 0 end)::float / count(*)::float)::numeric(3,2) AS error_percentage
FROM log 
GROUP BY time::date;
