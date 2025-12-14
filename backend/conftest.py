"""Pytest configuration for Django tests."""
import pytest
import django
from django.conf import settings


def pytest_configure():
    """Configure Django settings for tests."""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests."""
    pass
