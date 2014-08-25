# vyconf.types.base: base type validators everyone is likely to need
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

import re
from vyconf.types import TypeValidator, ValidationError, ConstraintFormatError

class StringValidator(TypeValidator):
    """ Validator for string values """

    name = "string"

    def __init__(self):
       	super(StringValidator, self).__init__()

    @classmethod
    def validate(self, value, constraint=None):
        if not isinstance(value, str):
            raise ValidationError("\"{0}\" is not a valid string".format(self.to_string_safe(value)))

        if constraint:
            if not isinstance(constraint, str):
                # If we take a precompiled regex, how are we going to issue
                # a meaningful error message?
                raise ConstraintFormatError("Constraint must be a string")
            try:
                constraint_re = re.compile(constraint)
            except Exception:
                raise ConstraintFormatError("\"{0}\" is not a valid constraint for type \"{1}\"".format(self.to_string_safe(constraint), self.name))

            # Check the value against constraint
            # XXX: do we need to force strict ^...$ match here?
            if not re.match(constraint_re, str(value)):
                raise ValidationError("\"{0}\" does not match pattern \"{1}\"".format(value, constraint))
            else:
                return True
        else:
            return True


class IntegerValidator(TypeValidator):
    """ Validates unsigned integer values """
    name = "integer"

    __range_re_str = """ (?: # xx-yy range group and separator, comma or end of line
                      (?: # xx-yy range group
                        (?P<start>\d+)
                        \-
                        (?P<stop>\d+)
                      (?:,|$))+?)
                """

    def in_range(value, min, max):
        if not ((value >= min) and (value <= max)):
            return True
    @classmethod
    def validate(self, value, constraint=None):
        """ Validate an integer. Takes either string representation or
            actual integer """
        if (not isinstance(value, str)) and (not isinstance(value, int)):
            raise ValidationError("\"{0}\" is not a valid integer".format(self.to_string_safe(value)))

        value_int = None
        if isinstance(value, str):
            try:
                value_int = int(value)
            except Exception:
                # Likely ValueError, but we don't really care which error it was
                raise ValidationError("{0} is not a valid integer".format(value, self.name))
        else:
            value_int = value

        if value_int < 0:
            # Anyone wants negative integers in configs?
            raise ValidationError("\"{0}\" is not a non-negative integer")

        if constraint:
            if not isinstance(constraint, str):
                raise ConstraintFormatError("Constraint must be a string")

            # XXX: needs really strict validation?
            range_re = re.compile(self.__range_re_str, re.VERBOSE)
            if not range_re.match(constraint):
                raise ConstraintFormatError("\"{0}\" is not a valid constraint for type \"{1}\"".format(constraint, self.name))

            # That regex returns ('min', 'max') tuples, convert content to integers
            ranges = map(lambda x: (int(x[0]), int(x[1])), range_re.findall(constraint))
            if True not in map(lambda x: True if x[0] <= value_int <= x[1] else False, ranges):
                raise ValidationError("\"{0}\" does not fall in range \"{1}\"".format(value, constraint))

        # If no exceptions were raised by this time, everything is fine
        return True

