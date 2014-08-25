#    vyconf.tree.referencetree.reference_tree_loader:
#        reference tree XML loader.
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

from lxml import etree as ET

NODE_ELEMENT = "node"
TAG_NODE_ELEMENT = "tagNode"
LEAF_NODE_ELEMENT = "leafNode"
NAME_CONSTRAINT_ELEMENT = "nameConstraint"
VALUE_CONSTRAINT_ELEMENT = "valueConstraint"
HELP_STRING_ELEMENT = "helpString"
VALUE_HELP_STRING_ELEMENT = "valueHelpString"

NODE_NAME_ATTRIBUTE = "name"
TYPE_ATTRIBUTE = "type"
CONSTRAINT_ATTRIBUTE = "constraint"
DESCRIPTION_ATTRIBUTE = "description"
VALUE_ATTRIBUTE = "value"
ERROR_MESSAGE_ATTRIBUTE = "error-message"

class ReferenceTreeLoaderError(Exception):
    """ Raised on attempts to create a reference tree from incorrect
        interface definition
    """
    def __init__(self, message):
        super(ReferenceTreeLoaderError, self).__init__(message)
        self.strerror = message


class ReferenceTreeLoader(object):
    def __init__(self, xml_source, types, schema=None):
        self.__xml_tree = ET.parse(xml_source)
        self.__xml_root = self.__xml_tree.getroot()
        self.__types = types

        if schema:
           relaxng_xml = ET.parse(schema)
           validator = ET.RelaxNG(relaxng_xml)
           if not validator.validate(self.__xml_tree):
               raise ReferenceTreeLoaderError("Malformed interface definition: {0}".format(xml_source))
        
    def load(self, reference_tree):
        self._walk_xml_node(self.__xml_root, reference_tree)

    def _walk_xml_leaf_node(self, xml_node, reference_node):
        for xml_child in xml_node:
            if xml_child.tag == HELP_STRING_ELEMENT:
                help_string = xml_child.attrib[DESCRIPTION_ATTRIBUTE]
                reference_node.set_help_string(help_string)
            elif xml_child.tag == VALUE_CONSTRAINT_ELEMENT:
                value_type = xml_child.attrib[TYPE_ATTRIBUTE]
                value_constraint = None
                value_error_message = None
                if CONSTRAINT_ATTRIBUTE in xml_child.attrib:
                    value_constraint = xml_child.attrib[CONSTRAINT_ATTRIBUTE]
                if ERROR_MESSAGE_ATTRIBUTE in xml_child.attrib:
                    value_error_message = xml_child.attrib[ERROR_MESSAGE_ATTRIBUTE]
                reference_node.add_value_constraint(value_type, value_constraint, value_error_message)
            elif xml_child.tag == VALUE_HELP_STRING_ELEMENT:
                # A lot of blind faith: the point is that <valueHelpString>
                # can have either value= attribute or type= and constaint= attributes
                help_string = xml_child.attrib[DESCRIPTION_ATTRIBUTE]
                value_type = None
                value_constraint = None
                value = None

                if TYPE_ATTRIBUTE in xml_child.attrib:
                    value_type = xml_child.attrib[TYPE_ATTRIBUTE]
                if CONSTRAINT_ATTRIBUTE in xml_child.attrib:
                    value_constraint = xml_child.attrib[CONSTRAINT_ATTRIBUTE]
                if VALUE_ATTRIBUTE in xml_child.attrib:
                    value = xml_child.attrib[VALUE_ATTRIBUTE]

                format = None
                if value_type is not None:
                    format = self.__types[value_type].get_format_string(value_constraint)
                else:
                    format = value

                reference_node.add_value_help_string(format, help_string)

    def _walk_xml_node(self, xml_node, reference_node):
        for xml_child in xml_node:
            # <tagNode> can not contain another <tagNode>, but we do not reflect it here
            # because it's already expressed in the RELAX-NG XML grammar
            if (xml_child.tag == NODE_ELEMENT) or (xml_child.tag == TAG_NODE_ELEMENT):
                next_reference_node = reference_node.insert_child([xml_child.attrib[NODE_NAME_ATTRIBUTE]])

                # If it's a tag node, we need to set a flag in the reference_node object
                if xml_child.tag == TAG_NODE_ELEMENT:
                   next_reference_node.set_tag()

                self._walk_xml_node(xml_child, next_reference_node)
            elif xml_child.tag == NAME_CONSTRAINT_ELEMENT:
                # Blind faith here again, type= attribute is required by the grammar
                name_type = xml_child.attrib[TYPE_ATTRIBUTE]

                # constraint= arribute is optional, needs a check
                name_constraint = None
                if CONSTRAINT_ATTRIBUTE in xml_child.attrib:
                    name_constraint = xml_child.attrib[CONSTRAINT_ATTRIBUTE]

                # error-message= is optional as well
                name_error_message = None
                if ERROR_MESSAGE_ATTRIBUTE in xml_child.attrib:
                    value_error_message = xml_child.attrib[ERROR_MESSAGE_ATTRIBUTE]

                reference_node.set_name_constraint(name_type, name_constraint, name_error_message)
            elif xml_child.tag == HELP_STRING_ELEMENT:
                help_string = xml_child.attrib[DESCRIPTION_ATTRIBUTE]
                reference_node.set_help_string(help_string)
            elif xml_child.tag == LEAF_NODE_ELEMENT:
                next_reference_node = reference_node.insert_child([xml_child.attrib[NODE_NAME_ATTRIBUTE]])
                next_reference_node.set_leaf()
                self._walk_xml_leaf_node(xml_child, next_reference_node)

