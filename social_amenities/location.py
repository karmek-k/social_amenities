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

import requests

def get_user_location() -> tuple[float, float]:
    """Returns user's location as latitude and longitude."""

    response = requests.get('https://ipinfo.io/loc')

    if response.status_code != 200:
        raise ConnectionError('Error while geolocating: non-200 HTTP status code')

    [lat, lon] = response.text.split(',')

    return (float(lat), float(lon))