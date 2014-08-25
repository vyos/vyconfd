#    vyconf.tree.configtree.config_node: 
#    Config storage classes for VyConf configuration management backend
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

class ConfigNode(vyconf.tree.Node):
    def __init__(self, name, parent=None):
        super(ConfigNode, self).__init__(name, parent)
        self.set_property("value_list", [])

    def add_value(self, value):
        self.get_property("value_list").append(value)

    def remove_value(self, value):
        self.get_property("value_list").remove(value)

    def get_values(self):
        return self.get_property("value_list")

    def set_comment(self, comment):
        self.set_property("comment", comment)

    def get_comment(self):
        return self.get_property("comment")

    
