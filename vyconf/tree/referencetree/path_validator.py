#    vyconf.tree.referencetree.path_validator:
#        config path validator
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

import vyconf.tree
import vyconf.types
import vyconf.tree
import vyconf.tree.referencetree

class PathValidationError(Exception):
    """ Raised when config path validation fails
    """
    def __init__(self, message, additional_messages=None):
        super(PathValidationError, self).__init__(message)
        self.strerror = message
        if additional_messages is not None:
            self.errors = additional_messages


class PathValidator(object):
    def __init__(self, types=None, tree=None):
        """ Creates a path validator object

            Args:
                types (dict): dictionary of type names and validators
        """
        if types is None:
            self.types = {}

        else:
            self.types = types

        if tree is None:
            self.tree = None
        else:
            self.tree = tree

    def _validate_leaf_or_tag_node(self, types, node, value):
        """ Validates a value or next child name against node constraints.

            Args:
                types (dict): a dict of vyconf.types.TypeValidator ancestors
                node (vyconf.tree.referencetree.ReferenceNode): a leaf or tag node
                value: a value (or name) to validate
        """
        valid = False
        errors = []
        for constraint_dict in node.get_value_constraints():
            current_type = constraint_dict['type']
            current_constraint = constraint_dict['constraint']
            try:
                self.types[current_type].validate(value, current_constraint)
                valid = True
                break
            except vyconf.types.ValidationError as e:
                errors.append(e.strerror)
        if valid:
            return (True, [])
        else:
            # Error messages go to the user, so we need to
            # pass them to the caller
            return (False, errors)

    def _validate(self, config_path, node):
        # We are going to mangle it, so copy it first
        path = config_path[:]
        node_name = path.pop(0)

	# There are two tricky cases: tag nodes and leaf nodes,
        # which need special validation of the immediate child.

        # So we get a reference tree child first
        next_node = node.find_child(node_name)

        # If it's a leaf node, we just need to validate the value
        if next_node.is_leaf() or next_node.is_tag():
            next_item = None
            try:
                next_item = path.pop()
            except IndexError:
                raise PathValidationError("""Path "{0}" is incomplete""".format(config_path))
            self._validate_leaf_or_tag_node(self.types, next_node, next_item)
        else:
             # It's a normal node, just recurse to it, if we have where to recurse
             if path:
                 self._validate(path, next_node)
             else:
                 return True

    def validate(self, config_path, config_level=None):
        """ Validates a config path against

            Args:
                config_path (list): a list representing config path
        """
        path = config_path[:]
        if config_level is not None:
            path = config_level + path

        try:
            self._validate(path, self.tree)
        except vyconf.tree.ChildNotFoundError as e:
            raise PathValidationError("""Configuration path "{0}" is not valid """.format(config_path))
