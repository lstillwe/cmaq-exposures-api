-- Format
-- variable,description,units,common_name,utc_min_date,utc_max_date,resolution,aggregation
-- o3,1000.0*O3[1],ppbV,ozone,2011-01-01,2011-12-31,day;7day;14day,max;avg
DROP TABLE IF EXISTS exposure_list;

-- create a temporary table for holding the raw data
CREATE TEMP TABLE tmp (
  exposure_type TEXT,
  exposure_desc TEXT,
  exposure_unit TEXT,
  common_name TEXT,
  start_date TEXT,
  end_date TEXT,
  resolution TEXT,
  aggregation TEXT
);

-- copy the raw data from sample csv file
COPY tmp FROM '/var/lib/pgsql/cmaq-exposures-api/init-database/exposure_list.csv' DELIMITER ',' CSV HEADER ;

-- create a table to load data into named exposure_list
CREATE TABLE IF NOT EXISTS exposure_list (
  ID SERIAL UNIQUE PRIMARY KEY,
  VARIABLE TEXT,
  DESCRIPTION TEXT,
  UNITS TEXT,
  COMMON_NAME TEXT,
  UTC_MIN_DATE DATE,
  UTC_MAX_DATE DATE,
  RESOLUTION TEXT,
  AGGREGATION TEXT
);

-- load the exposure_type table with properly formatted data
INSERT INTO exposure_list (VARIABLE, DESCRIPTION, UNITs, COMMON_NAME, UTC_MIN_DATE, UTC_MAX_DATE, RESOLUTION, AGGREGATION)
  SELECT
    exposure_type,
    exposure_desc,
    exposure_unit,
    common_name,
    cast(START_DATE as DATE),
    cast(END_DATE as DATE),
    resolution,
    aggregation
  FROM tmp;

-- drop the temporary table
DROP TABLE tmp;

-- set owner to datatrans user
ALTER TABLE exposure_list OWNER TO datatrans;

-- display a sample of contents to user
SELECT * FROM exposure_list ORDER BY variable ASC LIMIT 10;
