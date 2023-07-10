from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error #it is an exception class from psycopg2 library it is raised when there is error with databse
from django.core.management import call_command
from django.db.utils import OperationalError# is an exception class from Django that is raised when there is an error connecting to the database
from django.test import SimpleTestCase # is a base class for writing simple Django test cases.



#The @patch decorator is used to mock the check method of the core.management.commands.wait_for_db.Command class.
#This allows us to replace the original check method with a mock object, which we can control during testing.
@patch('core.management.commands.wait_for_db.Command.check')

class CommandTests(SimpleTestCase):
    def test_wait_for_db_ready(self, patched_check):
        #Test waiting for database if database is ready
        patched_check.return_value = True #setting return value of check method to true

        call_command('wait_for_db') #to simulate invoking the wait_for_db management command

        patched_check.assert_called_once_with(databases=['default'])
      
    @patch('time.sleep') 
    def test_wait_for_db_delay(self,patched_sleep,patched_check):
        #Test waiting for database when getting OperationalError.
        patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]

        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
