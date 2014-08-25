#    vyconf.tree.referencetree.reference_node: 
#    Interface definition storage classes for VyConf
#
#    Copyright (C) 2014 VyOS Development Group <maintainers@vyos.net>
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#    USA

# Animals are divided into: (a) belonging to the emperor, (b) embalmed,
# (c) tame, (d) sucking pigs, (e) sirens, (f) fabulous, (g) stray dogs,
# (h) included in the present classification, (i) frenzied, (j) innumerable,
# (k) drawn with a very fine camelhair brush, (l) et cetera, (m) having just
# broken the water pitcher, (n) that from a long way off look like flies.
#     From "The Analytical Language of John Wilkins" by
#     Jorge Luis Borges
# Our config nodes classification is just a little simpler.

import vyconf.tree

class ReferenceNodeError(Exception):
    """ Raised on attempts to create incorrectly configure ReferenceNode
        instance (e.g. set mutually exlusive flags at the same time)
    """
    def __init__(self, message):
        super(ReferenceNodeError, self).__init__(message)
        self.strerror = message


class ReferenceNode(vyconf.tree.Node):
    """ Reference nodes store information about available configuration
        tree paths.

        Nodes are divided into:
        1. Regular nodes that can have children with predetermined names.
        2. Tag nodes that can have children with names that satisfy certain
           constraint (such as "users someusername" or "ethernet eth0").
        3. Leaf nodes that can't have children.

        Leaf nodes may have none, one, or multiple values. We call leaf nodes
        that are allowed to have multiple values "multi" nodes.

        Names of tag node children or values of a leaf node have type and
        may have constraint associated with that type (e.g. type "string"
        and a regex to match specific format as its constraint).
        Leaf nodes that can't have children (usually those are flags like
        "disable" and such) are referred to as "typeless".

        Every node may have a help string as a piece of embedded documentation,
        leaf nodes may also have value help strings that describe possible values.

        Primary purpose of the reference nodes is to verify whether some path
        used as set/delete operation argument is valid and if the value attached to
        it satisfies the constraints.
    """

    def __init__(self, name, parent=None):
        super(ReferenceNode, self).__init__(name, parent)

        # Default flags
        self.set_property("leaf", False)
        self.set_property("tag", False)
        self.set_property("multi", False)
        self.set_property("name_constraint", {})
        self.set_property("value_constraints", [])
        self.set_property("value_help_strings", [])
        self.set_property("help_string", "")

    def set_leaf(self):
        self.set_property("leaf", True)

    def is_leaf(self):
        return self.get_property("leaf")

    def set_tag(self):
        self.set_property("tag", True)

    def is_tag(self):
        return self.get_property("tag")

    def set_multi(self):
        self.set_property("multi", True)

    def is_multi(self):
       	return self.get_property("multi")

    def set_name_constraint(self, type_string, constraint_string, name_error_message=None):
        self.set_property("name_constraint", {"type": type_string,
                                              "constraint": constraint_string,
                                              "error_message": name_error_message
                                             })

    def get_name_constraint(self):
        return self.get_property("name_constraint")

    def add_value_constraint(self, type_string, constraint_string, value_error_message=None):
        if (not isinstance(type_string, str)) and (not isinstance(constraint_string, str)):
            raise TypeError("Type and constraint must be strings")
        self.get_property("value_constraints").append({"type": type_string,
                                                       "constraint": constraint_string,
                                                       "error_message": value_error_message
                                                      })

    def get_value_constraints(self):
        return self.get_property("value_constraints")

    def add_value_help_string(self, format_string, help_string):
        if (not isinstance(format_string, str)) and (not isinstance(help_string, str)):
            raise TypeError("Format and help must be strings")
        self.get_property("value_help_strings").append({"format": format_string,
                                                        "help": help_string})

    def get_value_help_strings(self):
        return self.get_property("value_help_strings")

    def set_help_string(self, value):
        self.set_property("help_string", value)

    def get_help_string(self):
        return self.get_property("help_string")


