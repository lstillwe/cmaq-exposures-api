# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_get_values(self):
        """Test case for get_values

        CMAQ ozone (o3) and particulate matter (pm2.5) values
        """
        query_string = [('start_date', '2013-10-20'),
                        ('end_date', '2013-10-20'),
                        ('latitude', 'latitude_example'),
                        ('longitude', 'longitude_example'),
                        ('utc_offset', 'utc')]
        response = self.client.open(
            '/proximity_api/cmaq-exposures-api/1.0.0/values',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
