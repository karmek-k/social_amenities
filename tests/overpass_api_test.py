"""
social_amenities - Script that finds social amenities near your location.
Copyright (C) 2025 Bartosz Gleń

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import unittest

from social_amenities.overpass_api import overpass_query, extract_api_data


class TestOverpassApi(unittest.TestCase):
    def test_overpass_query(self) -> None:
        result = overpass_query("""
[bbox:30.618338,-96.323712,30.591028,-96.330826]
[out:json]
[timeout:90]
;
way(30.626917110746, -96.348809105664, 30.634468750236, -96.339893442898);
out geom;
""")
        self.assertIn('version', result.keys())
        self.assertIn('elements', result.keys())
    
    def test_extract_api_data(self) -> None:
        results = extract_api_data({'version': 0.6, 'generator': 'Overpass API 0.7.62.8 e802775f', 'osm3s': {'timestamp_osm_base': '2025-11-29T18:22:30Z', 'copyright': 'The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.'}, 'elements': [{'type': 'node', 'id': 5173189711, 'lat': 
52.5130596, 'lon': 21.0717741, 'tags': {'amenity': 'social_facility', 'email': 'xxx', 'level': '1', 'name': 'Ośrodek Pomocy Społecznej w Serocku', 'phone': 'yyy', 'social_facility': 'outreach', 'website': 'https://www.ops.serock.pl/'}}, {'type': 'node', 'id': 12176610285, 'lat': 52.5087274, 'lon': 21.0697434, 'tags': {'amenity': 'social_facility', 'name': 'Dom Wczasów Dziecięcych w Serocku', 'social_facility': 'nursing_home'}}]})

        first = results[0]

        self.assertEqual('Ośrodek Pomocy Społecznej w Serocku', first.name)
        self.assertEqual('xxx', first.email)
        self.assertEqual('yyy', first.phone)
        self.assertEqual('https://www.ops.serock.pl/', first.website)
