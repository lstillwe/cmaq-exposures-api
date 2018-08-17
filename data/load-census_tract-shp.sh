shp2pgsql -s 4269 US_Census_Tracts_NAD83/US_Census_Tracts_NAD83.shp public.census_tracts | psql -d cmaq -U datatrans
