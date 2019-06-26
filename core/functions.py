import re
import unicodedata
from datetime import datetime


"""
Helper functions
"""


def date_for_odm(date=None):
    d_format = "%Y-%m-%dT%H:%M:%S.%f"
    if not date:
        return datetime.utcnow().strftime(d_format)
    else:
        return date.strftime(d_format)
