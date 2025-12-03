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
import sys

from social_amenities.location import get_user_location, distance
from social_amenities.overpass_api import overpass_query, extract_api_data, Amenity
from social_amenities.types import Position


def main() -> None:
    """Main function of the script."""

    locale.setlocale(locale.LC_ALL, 'Polish_Poland')

    print('~~Wyszukiwarka ośrodków społecznych~~\n')
    print('Odnajdywanie Twojej lokalizacji...')

    lat, lon = get_user_location()
    
    print('Lokalizacja znaleziona. Podaj promień, w którym chcesz szukać ośrodków [w kilometrach]...')

    radius = 0.0
    while radius <= 0.0:
        try:
            radius = float(input('Promień [km]: '))
        except ValueError:
            print('Podano nieprawidłową wartość.')

    print('Wyszukiwanie punktów.')
    data = overpass_query(f"""
[out:json]
;
node
  [amenity=social_facility]
  (around:{int(radius * 1000.0)}, {lat}, {lon});
out;
""")

    amenities = extract_api_data(data)
    if not amenities:
        print(f'Nie znaleziono żadnych punktów w promieniu {radius} km.\nSpróbuj podać inną wartość.')
        sys.exit(1)

    print(f'Znaleziono {len(amenities)} punktów (odległości są orientacyjne).')
    print('Dane pochodzą z www.openstreetmap.org')

    for amenity in amenities:
        print_amenity((lat, lon), amenity)


def print_amenity(location: Position, amenity: Amenity) -> None:
    print('-' * 20)
    print(amenity.name, f'({distance(location, amenity.coords):.2f} km stąd)')
    print('-' * 20)

    if amenity.email:
        print('E-mail:', amenity.email)

    if amenity.phone:
        print('Telefon:', amenity.phone)

    if amenity.website:
        print('Strona internetowa:', amenity.website)
    
    print('Mapa:', amenity.map_url())
    
    print()
