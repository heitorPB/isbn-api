# SPDX-FileCopyrightText: 2023-present Heitor Pascoal de Bittencourt <heitorpbittencourt@gmail.com>
#
# SPDX-License-Identifier: MIT

from isbn_api.config import Settings
from isbn_api.main import get_settings


# Test server configuration

def test_settings():
    expected = Settings(server_name="main")
    assert get_settings() == expected
