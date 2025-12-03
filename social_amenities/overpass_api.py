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

from dataclasses import dataclass

import requests

from social_amenities.types import Position


ENDPOINT_URL = 'https://overpass-api.de/api/interpreter'

@dataclass
class Amenity:
    coords: Position
    name: str
    email: str | None
    phone: str | None
    website: str | None

    def map_url(self) -> str:
        """Returns a URL with a map centered on this location"""
        lat, lon = self.coords

        return f'https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=16'


def overpass_query(query: str) -> dict:
    """Makes a query to the Overpass API. Returns the resulting JSON parsed to a dictionary.
    The endpoint URL is defined in `ENDPOINT_URL`."""

    response = requests.post(ENDPOINT_URL, data=f'data={query}')
    
    if response.status_code != 200:
        raise ConnectionError(f'Error while querying: non-200 HTTP status code\n{response.text()}')

    return response.json()


def extract_api_data(data: dict) -> list[Amenity]:
    """Extracts data from `overpass_query`."""

    result = []
    elements = data['elements']

    for el in elements:
        tags = el['tags']

        result.append(Amenity(
            coords=(el['lat'], el['lon']),
            name=tags.get('name', 'bez nazwy'),
            email=tags.get('email'),
            phone=tags.get('phone'),
            website=tags.get('website'),
        ))

    return result
