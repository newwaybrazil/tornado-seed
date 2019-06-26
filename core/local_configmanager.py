import logging
import os
from configparser import ConfigParser
from typing import Optional, Any


class ConfigManager:
    """
    Use this class instead of making direct reference to config.ini/env
    To centralize constants names and such.
    """

    def __init__(self, config_path: str = 'config.ini'):
        self.config = ConfigParser()
        self.config.read(config_path)
        self.config_path = config_path

    @property
    def mongo(self) -> dict:
        return dict(
            connection_string = self._fetch('mongodb', 'connection_string'),
            database = self._fetch('mongodb', 'database'),
            user = self._fetch('mongodb', 'user'),
            password = self._fetch('mongodb', 'password')
        )

    @property
    def api(self) -> dict:
        return {
            'host': self._fetch('api', 'host'),
            'secret': self._fetch('api', 'secret'),
            'port': self._fetch('api', 'port'),
            'root_token': self._fetch('api', 'root_token')
        }

    def _fetch(self, section: str, field: str,
            varname: str = '',
            default: Any = None) -> Optional[str]:
        """
        Tries to fetch a variable from the conf file, falls back to env var.

        :param varname: Name of the env var to fallback to
        :param section: Name of the section on the config file
        :param field: Name of the field to retrieve the value.
        :param default: If the value is not set, return default instead.
        :return The value, if found, otherwise default.
        """
        value = self.config.get(section, field, fallback=None)
        if value:
            logging.debug('{} found on config file: {}'.format(field, value))
            return value

        value = os.environ.get(varname, None)
        if not value:
            logging.warning('{} not found as environment var: {}'.format(field,
                                                                         value))
        else:
            if default:
                value = default

        if value:
            logging.debug('{} found as environment variable'.format(field))
            self.config.set(section, field, value)
        elif default:
            value = default
            self.config.set(section, field, str(value))
        else:
            logging.warning('{} not specified'.format(field))

        return value
