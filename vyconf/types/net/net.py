# vyconf.types.net: network-related type validators
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

class MacAddressValidator(TypeValidator):
    """ Validator for string values """

    name = "mac_address"

    __mac_re = r'^([0-9a-f]{2}:){5}[0-9a-f]{2}$'

    def __init__(self):
       	super(MacAddressValidator, self).__init__()

    @classmethod
    def validate(self, value, constraint=None):
        """ Validates MAC address.

            
        """
        mac_re = re.compile(self.__mac_re, re.IGNORECASE)

        if not isinstance(value, str):
            raise ValidationError("\"{0}\" is not a valid string".format(self.to_string_safe(value)))

        # Check if it's valid at all
        if not re.match(mac_re, value):
            raise ValidationError("\"{0}\" is not a valid MAC address".format(value, constraint))

        if constraint:
            if not isinstance(constraint, str):
                # If we take a precompiled regex, how are we going to issue
                # a meaningful error message?
                raise ConstraintFormatError("Constraint must be a string")

            if constraint != "unicast":
                raise ConstraintFormatError("\"{0}\" is not a valid constraint for type \"{1}\"".format(constraint, self.name))

            if constraint == "unicast":
                # Unicast addresses always have the most significant bit of the most
                # significant byte set to 0
                msb = int(value[:2], 16)
                if msb & 1 != 0:
                    raise ValidationError("\"{0}\" is not a unicast MAC address".format(value))
        else:
            return True

