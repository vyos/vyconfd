# vyconf.types: base classes for VyConf node value validation
#
# Copyright (C) 2014 VyOS Development Group <maintainers@vyos.net>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301
# USA

import sys
import inspect

class ValidationError(Exception):
    """ Raised when the value fails validation """
    def __init__(self, message):
        super(ValidationError, self).__init__(message)
        self.strerror = message


class ConstraintFormatError(Exception):
    """ Raised when value constraint doesn't match the format
        the validator expects. """
    def __init(self, message):
        super(ConstraintFormatError, self).__init__(message)
        self.strerror = message


class TypeValidator(object):
    """ Type validator base class.

        This is not supposed to be used directly,
        
        The validate() method in ancestors should be a class method,
        so it can be called without instantiating the object.
    """

    """ Type name variable stores symbolic type name that is used in 
        interface definitions """
    name = None

    def __init__(self):
        pass

    @classmethod
    def validate(value, constraint=None):
        pass

    @staticmethod
    def to_string_safe(value):
        """ Sometimes conversion to string may fail,
            and we don't want to introduce more failures in validator """
        value_str = ""
        if not isinstance(value, str):
            try:
                value_str = repr(value)
            except Exception:
                pass
        return value_str


def get_types(module):
    """ Build a dict of type validators from specified module """
    types = {}
    classes = inspect.getmembers(module, inspect.isclass)
    for c in classes:
        # inspect.getmembers() return a list of tuples of name and class
        if issubclass(c[1], TypeValidator):
            types[c[1].name] = c[1]
    return types

