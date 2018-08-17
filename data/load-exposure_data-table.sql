-- Format
-- Date,FIPS,Longitude,Latitude,pm25_daily_average,pm25_daily_average_stderr,ozone_daily_8hour_maximum,ozone_daily_8hour_maximum_stderr
-- 2011/01/01,1001020100,-86.49001,32.47718,4.925,3.8543,31.603,6.2108

-- create a temporary table for holding the raw data
CREATE TEMP TABLE tmp (
    date TEXT,
    fips TEXT,
    lon TEXT,
    lat TEXT,
    pm25 TEXT,
    pm25_err TEXT,
    o3 TEXT,
    o3_err TEXT
);

-- copy the raw data from sample csv file
COPY tmp FROM '/projects/datatrans/new_cmaq_data/merged_cmaq_2011.csv' DELIMITER ',' CSV HEADER ;

-- create a table to load data into named cmaq
CREATE TABLE IF NOT EXISTS exposure_data (
  id SERIAL UNIQUE PRIMARY KEY,
  date DATE,
  fips BIGINT,
  latitude FLOAT,
  longitude FLOAT,
  location GEOGRAPHY(POINT,4326),
  pm25_daily_average FLOAT,
  pm25_daily_average_stderr FLOAT,
  ozone_daily_8hour_maximum FLOAT,
  ozone_daily_8hour_maximum_stderr FLOAT
);

-- load the cmaq table with properly formatted data
INSERT INTO cmaq (date, fips, latitude, longitude, location, pm25_daily_average, pm25_daily_average_stderr, ozone_daily_8hour_maximum, ozone_daily_8hour_maximum_stderr)
    SELECT
      cast(date as DATE),
      cast(fips as BIGINT),
      cast(lat as FLOAT),
      cast(lon as FLOAT),
      ST_GeographyFromText('SRID=4326;POINT('||lon||' '||lat||')'),
      cast(pm25 as FLOAT),
      cast(pm25_err as FLOAT),
      cast(o3 as FLOAT),
      cast(o3_err as FLOAT)
    FROM tmp;

-- drop the temporary table
DROP TABLE tmp;

-- set owner to datatrans user
ALTER TABLE cmaq OWNER TO datatrans;

-- display a sample of contents to user
SELECT * FROM cmaq ORDER BY date ASC LIMIT 10;
