# coding: utf-8
from sqlalchemy import ARRAY, BigInteger, Boolean, CheckConstraint, Column, Date, Float, Integer, Numeric, String, Table, Text, text
from geoalchemy2.types import Geography, Geometry
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CensusTract(Base):
    __tablename__ = 'census_tracts'

    gid = Column(Integer, primary_key=True, server_default=text("nextval('census_tracts_gid_seq'::regclass)"))
    statefp = Column(String(2))
    countyfp = Column(String(3))
    tractce = Column(String(6))
    geoid = Column(String(11))
    name = Column(String(7))
    namelsad = Column(String(20))
    mtfcc = Column(String(5))
    funcstat = Column(String(1))
    aland = Column(Numeric)
    awater = Column(Numeric)
    intptlat = Column(String(11))
    intptlon = Column(String(12))
    geom = Column(Geometry(u'MULTIPOLYGON', 4269))

class ExposureDatum(Base):
    __tablename__ = 'exposure_data'

    id = Column(Integer, primary_key=True, server_default=text("nextval('cmaq_id_seq'::regclass)"))
    date = Column(Date)
    fips = Column(BigInteger)
    latitude = Column(Float(53))
    longitude = Column(Float(53))
    location = Column(Geography(u'POINT', 4326))
    pm25_daily_average = Column(Float(53))
    pm25_daily_average_stderr = Column(Float(53))
    ozone_daily_8hour_maximum = Column(Float(53))
    ozone_daily_8hour_maximum_stderr = Column(Float(53))

class ExposureList(Base):
    __tablename__ = 'exposure_list'

    id = Column(Integer, primary_key=True, server_default=text("nextval('exposure_list_id_seq'::regclass)"))
    variable = Column(Text)
    description = Column(Text)
    units = Column(Text)
    common_name = Column(Text)
    utc_min_date = Column(Date)
    utc_max_date = Column(Date)
    resolution = Column(Text)
    aggregation = Column(Text)


t_geography_columns = Table(
    'geography_columns', metadata,
    Column('f_table_catalog', String),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geography_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', Text)
)


t_geometry_columns = Table(
    'geometry_columns', metadata,
    Column('f_table_catalog', String(256)),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geometry_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', String(30))
)


t_raster_columns = Table(
    'raster_columns', metadata,
    Column('r_table_catalog', String),
    Column('r_table_schema', String),
    Column('r_table_name', String),
    Column('r_raster_column', String),
    Column('srid', Integer),
    Column('scale_x', Float(53)),
    Column('scale_y', Float(53)),
    Column('blocksize_x', Integer),
    Column('blocksize_y', Integer),
    Column('same_alignment', Boolean),
    Column('regular_blocking', Boolean),
    Column('num_bands', Integer),
    Column('pixel_types', ARRAY(Text())),
    Column('nodata_values', ARRAY(Float(precision=53))),
    Column('out_db', Boolean),
    Column('extent', Geometry),
    Column('spatial_index', Boolean)
)


t_raster_overviews = Table(
    'raster_overviews', metadata,
    Column('o_table_catalog', String),
    Column('o_table_schema', String),
    Column('o_table_name', String),
    Column('o_raster_column', String),
    Column('r_table_catalog', String),
    Column('r_table_schema', String),
    Column('r_table_name', String),
    Column('r_raster_column', String),
    Column('overview_factor', Integer)
)


class SpatialRefSy(Base):
    __tablename__ = 'spatial_ref_sys'
    __table_args__ = (
        CheckConstraint('(srid > 0) AND (srid <= 998999)'),
    )

    srid = Column(Integer, primary_key=True)
    auth_name = Column(String(256))
    auth_srid = Column(Integer)
    srtext = Column(String(2048))
    proj4text = Column(String(2048))
