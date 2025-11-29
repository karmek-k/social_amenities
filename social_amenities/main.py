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

import locale

from social_amenities.location import get_user_location
from social_amenities.overpass_api import overpass_query


def main() -> None:
    """Main function of the script."""

    locale.setlocale(locale.LC_ALL, 'Polish_Poland')

    print('~~Wyszukiwarka ośrodków społecznych~~')
    print('Odnajdywanie Twojej lokalizacji...')

    lat, lon = get_user_location()
    
    print('Lokalizacja znaleziona. Podaj promień, w którym chcesz szukać ośrodków [w kilometrach]...')

    radius = 0.0
    while radius <= 0.0:
        try:
            radius = float(input('Promień: '))
        except ValueError:
            print('Podano nieprawidłową wartość.')

    query_result = overpass_query(f"""
[out:json]
;
node
  [amenity=social_facility]
  (around:{int(radius * 1000.0)}, {lat}, {lon});
out;
""")

    print(query_result)
