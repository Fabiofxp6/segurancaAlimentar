from .base import *  # noqa: F403
from ..testing import validate_test_database


validate_test_database(DATABASES["default"])  # noqa: F405
DEBUG = False
