# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.inline_response200_values import InlineResponse200Values  # noqa: F401,E501
from swagger_server import util


class InlineResponse200(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, values: List[InlineResponse200Values]=None):  # noqa: E501
        """InlineResponse200 - a model defined in Swagger

        :param values: The values of this InlineResponse200.  # noqa: E501
        :type values: List[InlineResponse200Values]
        """
        self.swagger_types = {
            'values': List[InlineResponse200Values]
        }

        self.attribute_map = {
            'values': 'values'
        }

        self._values = values

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse200':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200 of this InlineResponse200.  # noqa: E501
        :rtype: InlineResponse200
        """
        return util.deserialize_model(dikt, cls)

    @property
    def values(self) -> List[InlineResponse200Values]:
        """Gets the values of this InlineResponse200.


        :return: The values of this InlineResponse200.
        :rtype: List[InlineResponse200Values]
        """
        return self._values

    @values.setter
    def values(self, values: List[InlineResponse200Values]):
        """Sets the values of this InlineResponse200.


        :param values: The values of this InlineResponse200.
        :type values: List[InlineResponse200Values]
        """

        self._values = values
