"""
Tests for Django commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('django.db.utils.ConnectionHandler.__getitem__')
class CommandTests(SimpleTestCase):
    """Tests for Django commands."""

    def test_wait_for_db_ready(self, patched_conn):
        """Tests calling the wait_for_db command when DB available."""
        patched_conn.return_value = True
        call_command('wait_for_db')
        self.assertEqual(patched_conn.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, patched_conn):
        patched_conn.side_effect = [Psycopg2Error] * 5 \
            + [OperationalError] * 5 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_conn.call_count, 11)
