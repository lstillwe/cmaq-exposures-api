#import connexion
#import six
import sys

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.models import ExposureDatum  # noqa: E501
from swagger_server import util
from configparser import ConfigParser
from sqlalchemy import exists, or_, func

from swagger_server.controllers import Session
from flask import jsonify

parser = ConfigParser()
parser.read('swagger_server/ini/connexion.ini')
sys.path.append(parser.get('sys-path', 'exposures'))
sys.path.append(parser.get('sys-path', 'controllers'))


def get_values(start_date, end_date, latitude, longitude, utc_offset=None):  # noqa: E501
    """CMAQ ozone (o3) and particulate matter (pm2.5) values

    By passing in the appropriate options, you can retrieve CMAQ o3 and pm2.5 values  # noqa: E501

    :param start_date: start date of range
    :type start_date: str
    :param end_date: end date of range
    :type end_date: str
    :param latitude: latitude in decimal degrees format, ie: 35.7
    :type latitude: str
    :param longitude: longitude in decimal degrees format, ie: -80.33
    :type longitude: str
    :param utc_offset: timezone offset from UTC (utc, eastern, central, mountain, pacific) - default is utc
    :type utc_offset: str

    :rtype: InlineResponse200
    """
    session = Session()

    start_date = util.deserialize_date(start_date)
    end_date = util.deserialize_date(end_date)
    session.close()
    from swagger_server.exposures.cmaq import CmaqExposures
    cmaq = CmaqExposures()
    kwargs = locals()
    data = cmaq.get_values(**kwargs)

    return data
