# vyconf.types.dummy: dummy type validators for demonstration and testing
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

from vyconf.types import TypeValidator, ValidationError, ConstraintFormatError


class AlwaysValid(TypeValidator):
    """ Dumb type validator which thinks any value is valid """
    name = "alwaysvalid"

    def __init__(self):
        super(AlwaysValid, self).__init__()

    @classmethod
    def validate(self, value, constraint=None):
        return True


class NeverValid(TypeValidator):
    """ Dumb type validator which thinks the value is never valid """
    name = "nevervalid"

    def __init__(self):
        super(NeverValid, self).__init__()

    @classmethod
    def validate(self, value, constraint=None):
        raise ValidationError("Value {0} is not a valid value of type {1}".format(value, self.name))

class BadConstraint(TypeValidator):
    """ Dumb type validator, always complains about constraint format """
    name = "badconstraint"

    def __init__(self):
        super(BadConstraint, self).__init__()

    @classmethod
    def validate(self, value, constraint=None):
        raise ConstraintFormatError("Constraint string {0} is not valid for type {1}".format(value, self.name))
