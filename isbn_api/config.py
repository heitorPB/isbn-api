# SPDX-FileCopyrightText: 2023-present Heitor Pascoal de Bittencourt <heitorpbittencourt@gmail.com>
#
# SPDX-License-Identifier: MIT

from pydantic import BaseSettings


class Settings(BaseSettings):
    server_name: str = "main"
