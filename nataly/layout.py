# natali/layout.py
# Calculates the geometric layout for visualizing an astrological chart.

import math
from typing import List, Dict, Optional
from collections import defaultdict

from .models import Aspect
from .chart import NatalChart

class ChartLayout:
    """
    Takes one or two chart objects and calculates all geometric data
    required for visualization on a circular plane.
    """
    
    def __init__(self,
                 natal_chart: NatalChart,
                 transit_chart: Optional[NatalChart] = None,
                 transit_vs_natal_aspects: Optional[List[Aspect]] = None,
                 radius: int = 300,
                 rotation_angle: float = 0.0):
        self.natal_chart = natal_chart
        self.transit_chart = transit_chart
        self.transit_vs_natal_aspects = transit_vs_natal_aspects or []
        self.radius = radius
        self.rotation_angle = rotation_angle
        self.center_x, self.center_y = radius, radius
        self.house_layouts: List[Dict] = []
        self.body_layouts: List[Dict] = []
        self.aspect_layouts: List[Dict] = []
        self._calculate_all_layouts()

    def _get_coords(self, longitude: float, r: int) -> (float, float):
        """
        Converts astrological longitude to screen coordinates.
        This version fixes the mirroring and rotation issues definitively.
        """
        # The final correct formula to map astrological longitude to screen angle
        # with AC on the left and a counter-clockwise zodiac.
        angle_rad = math.radians(180 + self.rotation_angle - longitude)
        
        x = self.center_x + r * math.cos(angle_rad)
        y = self.center_y + r * math.sin(angle_rad)  # <--- CHANGE HERE
        return x, y

    def _calculate_all_layouts(self):
        self._calculate_house_layouts()
        self._calculate_body_layouts() # Must run before aspects
        self._calculate_aspect_layouts()

    def _calculate_house_layouts(self):
        for i, house in enumerate(self.natal_chart.houses):
            start_x, start_y = self._get_coords(house.cusp_longitude, int(self.radius * 0.4))
            end_x, end_y = self._get_coords(house.cusp_longitude, self.radius)
            next_cusp_lon = self.natal_chart.houses[(i + 1) % 12].cusp_longitude
            diff = (next_cusp_lon - house.cusp_longitude + 360) % 360
            # House numbers increase counter-clockwise, so the middle is forward.
            mid_house_lon = house.cusp_longitude + diff / 2
            label_radius = int(self.radius * 0.45)
            label_x, label_y = self._get_coords(mid_house_lon, label_radius)
            self.house_layouts.append({
                "id": house.id,
                "cusp_line_coords": ((start_x, start_y), (end_x, end_y)),
                "label_coords": (label_x, label_y)
            })

    def _calculate_body_layouts(self):
        longitude_map = defaultdict(list)
        all_bodies = self.natal_chart.planets + list(self.natal_chart.axes.values())
        for body in all_bodies:
            longitude_map[round(body.longitude, 1)].append(body)

        body_ring_radius = int(self.radius * 0.7)
        spoke_start_radius = int(self.radius * 0.4)
        label_offset = 20

        for lon_group in longitude_map.values():
            for i, body in enumerate(lon_group):
                current_radius = body_ring_radius - (i * 25)
                symbol_x, symbol_y = self._get_coords(body.longitude, current_radius)
                label_x, label_y = self._get_coords(body.longitude, current_radius + label_offset)
                line_start_x, line_start_y = self._get_coords(body.longitude, spoke_start_radius)

                self.body_layouts.append({
                    "name": body.name, "dms": body.dms, "is_retrograde": body.is_retrograde,
                    "symbol_coords": (symbol_x, symbol_y), "label_coords": (label_x, label_y),
                    "line_coords": ((line_start_x, line_start_y), (symbol_x, symbol_y)),
                    "sign_symbol": body.sign.symbol
                })

    def _calculate_aspect_layouts(self):
        for aspect in self.natal_chart.aspects:
            b1, b2 = aspect.body1, aspect.body2
            b1_layout = next((b for b in self.body_layouts if b['name'] == b1.name), None)
            b2_layout = next((b for b in self.body_layouts if b['name'] == b2.name), None)

            if b1_layout and b2_layout:
                start_x, start_y = b1_layout['line_coords'][0]
                end_x, end_y = b2_layout['line_coords'][0]
                self.aspect_layouts.append({
                    "type": aspect.aspect_type, "symbol": aspect.symbol, "orb_str": aspect.orb_str,
                    "line_coords": ((start_x, start_y), (end_x, end_y)),
                    "body1_name": b1.name, "body2_name": b2.name
                })

    def get_data(self) -> Dict:
        return {
            "radius": self.radius, "center": (self.center_x, self.center_y),
            "rotation_angle": self.rotation_angle,
            "natal": {
                "houses": self.house_layouts, "bodies": self.body_layouts,
                "aspects": self.aspect_layouts,
            },
            "transit": None
        }