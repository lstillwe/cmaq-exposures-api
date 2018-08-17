import sys
from configparser import ConfigParser
from datetime import datetime, timedelta
from sqlalchemy import extract, func, cast
from geoalchemy2 import Geography

import pytz
from swagger_server.controllers import Session
from flask import jsonify
from swagger_server.models.models import ExposureDatum, ExposureList, CensusTract

parser = ConfigParser()
parser.read('swagger_server/ini/connexion.ini')
sys.path.append(parser.get('sys-path', 'exposures'))
sys.path.append(parser.get('sys-path', 'controllers'))
from enum import Enum


class MeasurementType(Enum):
    # lat: 0 to +/- 90, lon: 0 to +/- 180 as lat,lon

    LATITUDE = '^[+-]?(([1-8]?[0-9])(\.[0-9]+)?|90(\.0+)?)$'
    LONGITUDE = '^[+-]?((([1-9]?[0-9]|1[0-7][0-9])(\.[0-9]+)?)|180(\.0+)?)$'

    def isValid(self, measurement):
        import re
        if re.match(self.value, str(measurement)) is None:
            return False
        else:
            return True

class CmaqExposures(object):

    def is_valid_date_range(self, **kwargs):
        session = Session()
        var_set = {'o3', 'pm25'} ################ TODO: CHANGE THIS TO GET FULL SET FROM DB #################
        for var in var_set:
            min_date = session.query(ExposureList.utc_min_date).filter(
                ExposureList.variable == var).one()
            max_date = session.query(ExposureList.utc_max_date).filter(
                ExposureList.variable == var).one()
            session.close()
            if min_date[0] > kwargs.get('end_date'):
                return False
            elif max_date[0] < kwargs.get('start_date'):
                return False
            elif kwargs.get('start_date') > kwargs.get('end_date'):
                return False

        return True

    def is_valid_lat_lon(self, **kwargs):
        # lat: 0 to +/- 90, lon: 0 to +/- 180 as lat,lon
        if not MeasurementType.LATITUDE.isValid(kwargs.get('latitude')):
            return False, ('Invalid parameter', 400, {'x-error': 'Invalid parameter: latitude'})
        if not MeasurementType.LONGITUDE.isValid(kwargs.get('longitude')):
            return False, ('Invalid parameter', 400, {'x-error': 'Invalid parameter: longitude'})

        return True, ''

    def is_valid_resolution(self, **kwargs):
        res_set = set()
        session = Session()
        #var_set = kwargs.get('variable').split(';')
        var_set = {'o3', 'pm25'} ################ TODO: CHANGE THIS TO GET FULL SET FROM DB #################
        for var in var_set:
            res = session.query(ExposureList.resolution).filter(
                ExposureList.variable == var).one()
            session.close()
            for item in res:
                res_set.update(item.split(';'))
            if kwargs.get('resolution') not in res_set:
                return False

        return True

    def is_valid_aggregation(self, **kwargs):
        agg_set = set()
        session = Session()
        #var_set = kwargs.get('variable').split(';')
        var_set = {'o3', 'pm25'} ################ TODO: CHANGE THIS TO GET FULL SET FROM DB #################
        for var in var_set:
            agg = session.query(ExposureList.aggregation).filter(
                ExposureList.variable == var).one()
            session.close()
            for item in agg:
                agg_set.update(item.split(';'))
            if kwargs.get('aggregation') not in agg_set:
                return False

        return True

    def is_valid_utc_offset(self, **kwargs):
        off_set = {'utc', 'eastern', 'central', 'mountain', 'pacific'}
        if kwargs.get('utc_offset') in off_set:
            return True
        else:
            return False

    def validate_parameters(self, **kwargs):
        lat_lon_valid, msg = self.is_valid_lat_lon(**kwargs)

        if not self.is_valid_date_range(**kwargs):
            return False, ('Invalid parameter', 400, {'x-error': 'Invalid parameter: start_date, end_date'})
        elif not lat_lon_valid:
            return False, msg
        elif not self.is_valid_resolution(**kwargs):
            return False, ('Invalid parameter', 400, {'x-error': 'Invalid parameter: resolution'})
        elif not self.is_valid_aggregation(**kwargs):
            return False, ('Invalid parameter', 400, {'x-error': 'Invalid parameter: aggregation'})
        elif not self.is_valid_utc_offset(**kwargs):
            return False, ('Invalid parameter', 400, {'x-error': 'Invalid parameter: utc_offset'})
        else:
            return True, ''

    def get_values(self, **kwargs):
        # variable, start_date, end_date, lat_lon, resolution = None, aggregation = None, utc_offset = None
        # 'UTC', 'US/Central', 'US/Eastern','US/Mountain', 'US/Pacific'
        tzone_dict = {'utc': 'UTC',
                      'eastern': 'US/Eastern',
                      'central': 'US/Central',
                      'mountain': 'US/Mountain',
                      'pacific': 'US/Pacific'}
        # validate input from user
        is_valid, message = self.validate_parameters(**kwargs)
        if not is_valid:
            return message

        # create data object
        data = {}
        data['values'] = []

        # set UTC offset as time zone parameter for query
        dt = datetime.now()
        utc_offset = int(str(pytz.timezone(tzone_dict.get(kwargs.get('utc_offset'))).localize(dt)
                             - pytz.utc.localize(dt)).split(':')[0])

        # retrieve query result for each lat,lon pair and add to data object
        lat = kwargs.get('latitude')
        lon = kwargs.get('longitude')
        var_set = {'ozone_daily_8hour_maximum', 'pm25_daily_average'} ################ TODO: CHANGE THIS TO GET FULL SET FROM DB #################

        for var in var_set:
            # determine exposure type to query
            cmaq_output = []

            start_time = kwargs.get('start_date')
            end_time = kwargs.get('end_date')
            exposure = var

            session = Session()

            # given this lat lon, find the census tract that contains it.
            query = session.query(CensusTract.geoid). \
                            filter(func.ST_Contains(CensusTract.geom, func.ST_GeomFromText("POINT(" + str(lon) + " " + str(lat) + ")", 4269)))
            result = session.execute(query)
            for query_return_values in result:
                geoid = query_return_values[0]

            # daily resolution of data - return only matched hours for date range
            query = session.query(ExposureDatum.id,
                                  ExposureDatum.date,
                                  getattr(ExposureDatum, exposure)). \
                                  filter(ExposureDatum.date >= start_time + timedelta(hours=utc_offset)). \
                                  filter(ExposureDatum.date <= end_time + timedelta(hours=utc_offset)). \
                                  filter(ExposureDatum.fips == geoid). \
                                  filter(extract('hour', ExposureDatum.date) == utc_offset)

            # add query output to data object in JSON structured format
            for query_return_values in query:
                    cmaq_output.append({'date': query_return_values[1].strftime("%Y-%m-%d"),
                                        'value': float(query_return_values[2])})
            session.close()
            data['values'].append({'variable': var,
                                   'latitude': lat,
                                   'longitude': lon,
                                   'cmaq_output': cmaq_output})
        return jsonify(data)
