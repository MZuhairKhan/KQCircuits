# This code is part of KQCircuits
# Copyright (C) 2021 IQM Finland Oy
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see
# https://www.gnu.org/licenses/gpl-3.0.html.
#
# The software distribution should follow IQM trademark policy for open-source software 
# (meetiqm.com/developers/osstmpolicy). IQM welcomes contributions to the code. Please see our contribution agreements
# for individuals (meetiqm.com/developers/clas/individual) and organizations (meetiqm.com/developers/clas/organization).


from math import cos, sin, pi
from kqcircuits.pya_resolver import pya
from kqcircuits.util.parameters import Param, pdt
from autologging import logged, traced

from kqcircuits.elements.element import Element

@traced
@logged
class FlipChipConnector(Element):
    """Connector between matching faces of two chips.

    The connector makes a galvanic contact between the flipped over top chip and the bottom chip.
    Origin is at the geometric center.
    """

    ubm_diameter = Param(pdt.TypeDouble, "Under-bump metallization diameter", 40, unit="μm",
                         docstring="Diameter of the under-bump metallization box [μm]")
    bump_diameter = Param(pdt.TypeDouble, "Bump diameter", 25, unit="μm",
                          docstring="Indium bump diameter [μm]")

    def produce_impl(self):
        super().produce_impl()

    def create_bump_connector(self):
        ubm_shape = self._circle(self.ubm_diameter / 2, self.n)
        self.cell.shapes(self.get_layer("underbump_metallization", 0)).insert(ubm_shape)
        self.cell.shapes(self.get_layer("underbump_metallization", 1)).insert(ubm_shape)

        avoidance_shape = self._circle(self.ubm_diameter / 2 + self.margin, self.n)
        self.cell.shapes(self.get_layer("ground_grid_avoidance", 0)).insert(avoidance_shape)
        self.cell.shapes(self.get_layer("ground_grid_avoidance", 1)).insert(avoidance_shape)

        bump_shape = self._circle(self.bump_diameter / 2, self.n)
        self.cell.shapes(self.get_layer("indium_bump", 0)).insert(bump_shape)  # bottom In bump
        self.cell.shapes(self.get_layer("indium_bump", 1)).insert(bump_shape)  # top In bump

        super().produce_impl()

    @staticmethod
    def _circle(r, n):
        return pya.DPolygon([pya.DPoint(cos(a/n * 2 * pi) * r, sin(a/n * 2 * pi) * r) for a in range(0, n + 1)])
