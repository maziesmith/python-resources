################################################
# Intro
################################################
# https://docs.python-guide.org/writing/tests/

# A testing unit should focus on one tiny bit of functionality and prove it correct
# Each test unit must be fully independent
# Make tests run fast 
# Use long and descriptive test names

# Arrange Act Assert
# http://wiki.c2.com/?ArrangeActAssert

# Arrange all necessary preconditions and input
# Act on the object or method under test
# Assert that the expected results have occurred
 

'''
minimize dependencies
'''
# to simplify testing a class definition, we need to isolate it from the surrounding classes 

# create a deck class 

# bad implementation - depends on the card class implementations and the random 
# First, it's intimately bound to the three classes in the Card class hierarchy. We can't isolate Deck from Card for a standalone unit test.
# Second, it is dependent on the random number generator, making it difficult to create a repeatable test
class Deck1( list ):
    def __init__( self, size=1 ):
        super().__init__()
        self.rng= random.Random()
        for d in range(size):
            for s in Suits:
                cards = ([AceCard(1, s)]
                + [Card(r, s) for r in range(2, 12)]
                + [FaceCard(r, s) for r in range(12, 14)])
                super().extend( cards )
        self.rng.shuffle( self )

# solution, to seprate the dependencies 
# create a factory function to produce proper subclasses of Card based 
def card(rank, suit):
    if rank == 1: return AceCard(rank, suit)
    elif 2 <= rank < 11: return Card(rank, suit)
    elif 11 <= rank < 14: return FaceCard(rank, suit)
    else: raise Exception("LogicError")

# another example of separating Card class from teh Deck class 
# refactor the factory function to be a method of Deck 
class Deck2(list):
    def __init__(self, size=1, random=random.Random(),
        ace_class=AceCard, card_class=Card, face_class=FaceCard):
        super().__init__()
        self.rng = random 
        for d in range(size):
            for s in Suits:
                cards = ([ace_class(1, s)]
                + [ card_class(r, s) for r in range(2, 12) ]
                + [ face_class(r, s) for r in range(12, 14) ] )
                super().extend( cards )
        self.rng.shuffle( self )



################################################
# Unittest 
################################################

# Reasons for Unit Testing
# Understand what to build
# Document the units
# Design the units - idependently testable
# Regression Protection

# A unit test checks the behavior of an element of code
# A method or function
# A module or class

# An automated test
# runs without intervention 

# Test Case
# Each should be for a specific behavior
# Shouldn't have side effects (like creating data other test cases use)

# $ python3 -m unittest

'''
Basic Unittest
'''

# test a function 
import unittest
def func(x):
    return x+1

class Mytest(unittes.TestCase):
    def test(self):
        self.assertEqual(func(3),4)

# test a class 
# in test_phonebook.py
import unittest

from phonebook import Phonebook

class TestPhonebook(unittest.TestCase):
    def test_create_phonebook(self):
        phonebook = Phonebook()
# in phonebook.py
class Phonebook:
    pass

import unittest
class CheckNumbers(unittest.TestCase):
    def test_int_float(self):
        self.assertEqual(1,1.0)
if __name__ == "__main__":
    unittest.main()

# run the test
# python 6-testing/test.py
# pytest 6-testing/test.py
# python3 -m unittest 6-testing/test.py

# python -m unittest test_example
# python3 -m unittest test_example.MyTest


# We can have as many test methods on one TestCase class as we like; as long as
# the method name begins with test, the test runner will execute each one as a
# separate test. Each test should be completely independent of other tests.

'''
assert
'''
# assertRaises
# It can be used as a context manager to wrap inline code. 
# The test passes if the code inside the with statement raises the proper exception; otherwise, it fails.

import unittest 

def average(seq):
    return sum(seq)/len(seq)

class TestAverage(unittest.TestCase):
    def test_with_zero(self):
        with self.assertRaises(ZeroDivisionError):
            average([])

if __name__ == "__main__":
    unittest.main()

# assertGreater
# assertGreaterEqual
# assertIn
# assertNotIn
# assertIsNone
# assertSetEqual 


'''
setup 
'''
# setUp()
# before each test case is run, the test case can access the object defined in setUp
def setUp(self):
    self.phonebook = Phonebook()

# to do cleanup 
def tearDown(self):
    pass


# if need to do the same setup code multiple time, put it in setUp
from stats import StatsList 
import unittest 

class TestValidInputs(unittes.TestCase):
    # setup is called individually before each test, to ensure tests start with clean slate

    def setUp(self):
        self.stats = StatsList([1,2,3,4,5])
    
    def test_mean(self):
        self.assertEqual(self.stats.mean(), 2.5)
    
    def test_median(self):
        self.assertEqual(self.stats.median(), 2.5)
        self.stats.append(4)
        self.assertEqual(self.stats.median(), 3)

if __name__ == "__main__":
    unittest.main()

# example test Card class

class TestCard(unittest.TestCase):
    def setUp(self):
        self.three_clubs = Card( 3, '♣' )
    
    def test_should_returnStr(self):
        self.assertEqual("3♣", str(self.three_clubs))
    
    def test_should_getAttrValues( self ):
        self.assertEqual( 3, self.three_clubs.rank )
        self.assertEqual( "♣", self.three_clubs.suit )


# example test of a factory function
# function to test for 
def card(rank, suit):
    if rank == 1: return AceCard(rank, suit)
    elif 2 <= rank < 11: return Card(rank, suit)
    elif 11 <= rank < 14: return FaceCard(rank, suit)
    else: raise Exception("LogicError") 

class TestCardFactory(unittest.TestCase):
    def test_rank1_should_createAceCard(self):
        c = card( 1, '♣' )
        self.assertIsInstance( c, AceCard )
    def test_rank2_should_createCard(self):
        c = card( 2, '♦' )
        self.assertIsInstance( c, Card )
    def test_rank10_should_createCard( self ):
        c = card( 10, '♥' )
        self.assertIsInstance( c, Card)
    def test_otherRank_should_exception(self):
        with self.assertRaises(LogicError):
            c = card(14, '♦')
        with self.assertRaises(LogicError):
            c = card(0, '♦')


# run a specific test 
# $ python3 -m unittest -q test_phonebook.TestPhonebook.test_lookup_entry_by_name

# skip a test
@unittest.skip("WIP")


'''
setup and teardown with databases
'''
# create test databases SQLAlchemy
# We defined setUpClass() so that a database is created before the tests from this
# class are run. This allows us to define a number of test methods that will share a
# common database configuration.

from p2_c11 import Base, Blog, Post, Tag, assoc_post_tag
import datetime

import sqlalchemy.exc
from sqlalchemy import create_engine

def build_test_db( name='sqlite:///./p3_c15_blog.db' ):
    engine = create_engine(name, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return engine

from sqlalchemy.orm import sessionmaker
class Test_Blog_Queries( unittest.TestCase ):
    @staticmethod
    def setUpClass():
        engine= build_test_db()
        # put the session maker object into the class as a class-level attribute. 
        # Can then be used in setup and other methods
        Test_Blog_Queries.Session = sessionmaker(bind=engine)
        session= Test_Blog_Queries.Session()
        tag_rr= Tag( phrase="#RedRanger" )
        session.add( tag_rr )
        tag_w42= Tag( phrase="#Whitby42" )
        session.add( tag_w42 )
        tag_icw= Tag( phrase="#ICW" )
        session.add( tag_icw )
        tag_mis= Tag( phrase="#Mistakes" )
        session.add( tag_mis )
        blog1= Blog( title="Travel 2013" )
        session.add( blog1 )
        b1p1= Post( date=datetime.datetime(2013,11,14,17,25),
        title="Hard Aground",
        rst_text="""Some embarrassing revelation.
        Including ☹ and ⎕""",
        blog=blog1,
        tags=[tag_rr, tag_w42, tag_icw],
        )
        session.add(b1p1)
        session.commit()

    def setUp(self):
        self.session = Test_Blog_Queries.Session()

    def test_query_eqTitle_should_return1Blog( self ):
        results= self.session.query( Blog ).filter(
        Blog.title == "Travel 2013" ).all()
        self.assertEqual( 1, len(results) )
        self.assertEqual( 2, len(results[0].entries) )

    def test_query_likeTitle_should_return2Blog( self ):
        results= self.session.query( Blog ).filter(
        Blog.title.like("Travel %") ).all()
        self.assertEqual( 2, len(results) )


################################################
# Pytest
################################################

# pytest doesn't require test cases to be classes 
# instead takes advantage of the fact that python functions are objects and allow function to behave like a test

# When we run py.test, it will start in the current folder and search for any modules
# in that folder or subpackages whose names start with the characters test_. If any
# functions in this module also start with test, they will be executed as individual
# tests. Furthermore, if there are any classes in the module whose name starts with
# Test, any methods on that class that start with test_ will also be executed in the
# test environment.


# pip install -U pytest

# run tests
# python3 -m pytest


# simple example
def test_int_float():
    assert 1==1.0

# another example 
from phonebook import Phonebook

def test_add_and_lookup_entry():
    phonebook = Phonebook()
    phonebook.add("Bob","123")
    assert "123" == phonebook.lookup("Bob")
    assert "123" == None

# can also use classes for grouping related tests together 
class TestNumbers:
    def test_int_float(self):
        assert 1==1.0
    
    def test_int_str(self):
        assert 1=="1"

'''
test debugging
'''
# By default, py.test suppresses output from print statements if the test is
# successful. This is useful for test debugging; when a test is failing, we can add
# print statements to the test to check the values of specific variables and attributes
# as the test runs. 

# If the test fails, these values are output to help with diagnosis.
# However, once the test is successful, the print statement output is not displayed,
# and they can be easily ignored. We don't have to "clean up" the output by removing
# print statements. If the tests ever fail again, due to future changes, the debugging
# output will be immediately available.

'''
setUp
'''
# similar to unittest we also have setup and teardown methods 
# the setup_class and teardown_class methods are expected to be class methods 
# we have the setup_module and teardown_module functions which are run immediately before and after all tests 
# useful for one time setup - such as creating a socket or database connection that will be used by all tests in the module 
def setup_module(module):
    print("setting up MODULE {0}".format(module.__name__))

def teardown_module(module):
    print("tearing down MODULE {0}".format(module.__name__))

def test_a_function():
    print("Running test function")

class BaseTest:
    def setup_class(cls):
        print("setting up CLASS {0}".format(cls.__name__))

    def teardown_class(cls):
        print("tearing down CLASS {0}\n".format(cls.__name__))
    
    def setup_method(self, method):
        print("setting up METHOD {0}".format(method.__name__))
   
    def teardown_method(self, method):
        print("tearing down METHOD {0}".format(method.__name__))


'''
funcargs
'''

# py.test offers a completely different way to do this using what are known as
# funcargs, short for function arguments. Funcargs are basically named variables that
# are predefined in a test configuration file. This allows us to separate configuration
# from execution of tests, and allows the funcargs to be used across multiple classes
# and modules.

# As with other py.test features, the name of the factory for returning a funcarg is
# important; funcargs are functions that are named pytest_funcarg__<identifier>,
# where <identifier> is a valid variable name that can be used as a parameter in a
# test function.

# for example to "setup" a list of valid integers 
from stats import StatsList 

def pytest_funcarg__valid_stats(request):
    return StatsList([1,2,3,4,5,6])

def test_mean(valid_stats):
    assert valid_stats.mean() == 2.5

def test_median(valid_stats):
    assert valid_stats.median() == 2.5
    valid_stats.append(4)
    assert valid_stats.median() == 3

def test_mode(valid_stats):
    assert valid_stats.mode() == [2,3]
    valid_stats.remove(2)
    assert valid_stats.mode() == [3]

# Each of the three test methods accepts a parameter named valid_stats; this
# parameter is created by calling the pytest_funcarg__valid_stats function defined
# at the top of the file. It can also be defined in a file called conftest.py if the funcarg
# is needed by multiple modules. The conftest.py file is parsed by py.test to
# load any "global" test configuration; it is a sort of catch-all for customizing the
# py.test experience.


# use request.addfinalizer for cleanup 
# after each test function that uses the funcargs has been called 
import tempfile 
import shutil 
import os.path 

def pytest_funcarg__temp_dir(request):
    dir = tempfile.mkdtemp()
    print(dir)

    def cleanup():
        shutil.rmtree(dir)
    
    request.addfinalizer(cleanup)
    return dir 

def test_osfiles(temp_dir):
    os.mkdir(os.path.join(temp_dir, 'a'))
    os.mkdir(os.path.join(temp_dir, 'b'))
    dir_contents = os.listdir(temp_dir)
    assert len(dir_contents) == 2
    assert 'a' in dir_contents
    assert 'b' in dir_contents

'''
skipping tests
'''
# use py.test.skip
# accepts a string describing why it's skipped
# can execute skip anywhere in the python code 

import sys
import py.test 

def test_simple_skip():
    if sys.platform != "fakeos":
        py.test.skip("Test works only on fakeOS")
    
    fakeos.do_something_faken()
    assert fakeos.did_not_happen 


'''
fixture 
'''
# text fixture https://docs.pytest.org/en/latest/fixture.html#fixtures
# to share data between test cases
# offers a baseline upon which tests can execute

# test case request a resource
@pytest.fixture
def resource():
    return Resource()


# adding a test fixture and clearning out
@pytest.fixture
def phonebook(request):
    phonebook = Phonebook()
    def cleanup_phonebook():
        phonebook.clear()
    request.addfinalizer(cleanup_phonebook)
    return phonebook


import pytest_example
@pytest.fixture
def smtp_connection():
    import smtplib
    return smtplib.SMTP("smtp.gmail.com",587,timeout=5)

def test_ehlo(smtp_connection):
    response, msg = smtp_connection.ehlo()
    assert response == 250
    assert 0 


'''
exceptions
'''
# assertions about expected exceptions

def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0 



################################################
# Mock
################################################
# class under test doesn't know it isn't talking to real one 

#  https://www.toptal.com/python/an-introduction-to-mocking-in-python
#  https://aaronlelevier.github.io/python-unit-testing-with-magicmock/
#  https://realpython.com/python-mock-library/
#  https://realpython.com/testing-third-party-apis-with-mocks/


# assertions
# check the return value or an exception
# check a state change (use a public API)
# check a method call (use a mock or spy)


'''
mock
'''
# example class to test for 
class Deck3( list ):
    def __init__( self, size=1,
        random=random.Random(),
        card_factory=card ):
        super().__init__()
        self.rng= random
        for d in range(size):
            super().extend(
            card_factory(r,s) for r in range(1,13) for s in Suits
            )
        self.rng.shuffle( self )
    def deal( self ):
        try:
            return self.pop(0)
        except IndexError:
            raise DeckEmpty()

# consider the dependencies that must be mocked for unit testing 
# in the case mock the Card class, the card() factory, and the random method 
# example tes tot show the deck is built properly 
import unittest
import unittest.mock 

class TestDeckBuild(unittest.TestCase):
    def setUp(self):
        self.test_card = unittest.mock.Mock(return_value=unittest.mock.sentinel)
        self.test_rng = random.Random()
        self.test_rng.shuffle= unittest.mock.Mock( return_value=None )
    def test_deck_1_should_build(self):
        d= Deck3( size=1, random=self.test_rng, card_factory= self.
        test_card )
        self.assertEqual( 52*[unittest.mock.sentinel], d )
        self.test_rng.shuffle.assert_called_with( d )
        self.assertEqual( 52, len(self.test_card.call_args_list) )
        expected = [
            unittest.mock.call(r,s)
                for r in range(1,14)
                    for s in ('♣', '♦', '♥', '♠') ]
        self.assertEqual( expected, self.test_card.call_args_list )


'''
magic mock
'''

# A MagicMock instance can: 
# capture the arguments that the method is called with
# count how many times it’s called
# return values that we specify
# return the same or different values each time the mocked method is called
# be made to raise errors

# @patch is the same thing as using the MagicMock class. 
# It sets the mocked method as a MagicMock instance for the duration of the unit test method, 
# then set’s back the method to reference it’s original definition when the unit test method completes.

from unittest.mock import MagicMock
instance = ProductionClass()
instance.method = MagicMock(return_value=3)


'''
import / local scope
'''
import my_calendar # any functions there is in the my_calendar scope
from my_calendar import is_weekday # is_weekday becomes local scope

# >>> import my_calendar
# >>> from unittest.mock import patch

# >>> with patch('my_calendar.is_weekday'):
# ...     my_calendar.is_weekday()

# >>> from unittest.mock import patch
# >>> from my_calendar import is_weekday

# >>> with patch('__main__.is_weekday'):
# ...     is_weekday()



# Example Import Requests 

# project/services.py

# Third-party imports...
import requests

# Local imports...
from project.constants import BASE_URL

TODOS_URL = urljoin(BASE_URL, 'todos')

def get_todos():
    response = requests.get(TODOS_URL)
    if response.ok:
        return response
    else:
        return None

# project/tests/test_todos.py

# Standard library imports...
from unittest.mock import Mock, patch

# Third-party imports...
from nose.tools import assert_is_not_none

# Local imports...
from project.services import get_todos

# When the test function is run, it finds the module where the requests library is declared, project.services, 
# and it replaces the targeted function, requests.get(), with a mock.
@patch('project.services.requests.get') # note the requests is in local scope
def test_getting_todos(mock_get):
    # Configure the mock to return a response with an OK status code.
    mock_get.return_value.ok = True

    # Call the service, which will send a request to the server.
    response = get_todos()

    # If the request is sent successfully, then I expect a response to be returned.
    assert_is_not_none(response)


'''
patching objects in unit tests
'''
# apply patches to selected objects to make assertions about how they were used 
# patch() works by taking an existing object with the fully qualified name that you provide
# and replacing it with a new value. The original value is then restored after the
# completion of the decorated function or context manager. By default, values are replaced
# with MagicMock instances.


from unittest.mock import patch
import example
@patch('example.func')
def test1(x, mock_func):
    example.func(x) # Uses patched example.func
    mock_func.assert_called_with(x)


# example delete function
# mymodule.py
import os
def rm(filename):
    os.remove(filename)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mymodule import rm 

import mock 
import unittest

# Mock an item where it is used not where it came from 
# mock module.os instead of os
# At runtime, the mymodule module has its own os which is imported into its own local scope in the module. 
# Thus, if we mock os, we won’t see the effects of the mock in the mymodule module.
class RmTestCase(unittest.TestCase):

    @mock.patch('mymodule.os')
    def test_rm(self, mock_os):
        rm("any path")
        # test that rm called os.remove with the right parameters
        mock_os.remove.asssert_called_with("any path")


# example.py
from urllib.request import urlopen
import csv
def dowprices():
    u = urlopen('http://finance.yahoo.com/d/quotes.csv?s=@^DJI&f=sl1')
    lines = (line.decode('utf-8') for line in u)
    rows = (row for row in csv.reader(lines) if len(row) == 2)
    prices = { name:float(price) for name, price in rows }
    return prices 



'''
mock return value
'''

# adding validation to rm
import os
import os.path

def rm(filename):
    if os.path.isfile(filename):
        os.remove(filename)

# adjust test case to keep coverage
from mymodule import rm 

import mock 
import unittest 

class RmTestCase(unittest.TestCase):

    @mock.patch('mymodule.os.path')
    @mock.patch('mymodule.os')
    def test_rm(self, mock_os, mock_path):
        # set up the mock 
        mock_path.isfile.return_value = False 

        rm("any path")

        # test that the remove call was NOT called 
        self.assertFalse(mock_os.remove.called, "Failed to not remove file if not present")

        # make the file exist
        mock_path.is_file.return_value = True 

        rm("any path")

        mock_os.remove.assert_called_with("any path")


# note the decorator order
# @mock.patch('mymodule.sys')
# @mock.patch('mymodule.os')
# @mock.patch('mymodule.os.path')
# def test_something(self, mock_os_path, mock_os, mock_sys):
#     pass


# In this example, the urlopen() function in the example module is replaced with a mock
# object that returns a BytesIO() containing sample data as a substitute

import unittest
from unittest.mock import patch 
import io 
import example 

sample_data = io.BytesIO(b'''\
"IBM",91.1\r
"AA",13.25\r
"MSFT",27.72\r
\r
''')
class Tests(unittest.TestCase):
    @patch('example.urlopen', return_value=sample_data)
    def test_dowprices(self, mock_urlopen):
        p = example.dowprices()
        self.assertTrue(mock_urlopen.called)
        self.assertEqual(p, 
                         {'IBM': 91.1,
                          'AA': 13.25,
                          'MSFT' : 27.72})

if __name__ == '__main__':
    unittest.main()


'''
mock instance methods
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path

class RemovalService(object):
    """A service for removing objects from the filesystem."""

    def rm(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)
            

class UploadService(object):

    def __init__(self, removal_service):
        self.removal_service = removal_service
        
    def upload_complete(self, filename):
        self.removal_service.rm(filename)

# We’ll test (without side-effects, of course) that UploadService calls the RemovalService.rm method
# here we try to mock RemoveService.rm method 

# The mock library has a special method decorator for mocking object instance methods and properties
# the @mock.patch.object decorator

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mymodule import RemovalService, UploadService

import mock
import unittest
      
class UploadServiceTestCase(unittest.TestCase):

    @mock.patch.object(RemovalService, 'rm')
    # or can specify the full path @mock.patch('mymodule.RemovalService.rm')
    def test_upload_complete(self, mock_rm):
        # build our dependencies
        removal_service = RemovalService()
        reference = UploadService(removal_service)
        
        # call upload_complete, which should, in turn, call `rm`:
        reference.upload_complete("my uploaded file")
        
        # check that it called the rm method of any RemovalService
        mock_rm.assert_called_with("my uploaded file")
        
        # check that it called the rm method of _our_ removal_service
        removal_service.rm.assert_called_with("my uploaded file")

'''
creating mock instances
'''

# instead of mocking the specific instance method, we provide a mocked instance

# In this example, we haven’t even had to patch any functionality, 
# we simply create an auto-spec for the RemovalService class, and then inject this instance into our UploadService to validate the functionality.

# The mock.create_autospec method creates a functionally equivalent instance to the provided class. 
# What this means is that when the returned instance is interacted with, it will raise exceptions if used in illegal ways. 
# More specifically, if a method is called with the wrong number of arguments, an exception will be raised

class UploadServiceTestCase(unittest.TestCase):

    def test_upload_complete(self, mock_rm):
        # build our dependencies
        mock_removal_service = mock.create_autospec(RemovalService)
        reference = UploadService(mock_removal_service)
        
        # call upload_complete, which should, in turn, call `rm`:
        reference.upload_complete("my uploaded file")
        
        # test that it called the rm method
        mock_removal_service.rm.assert_called_with("my uploaded file")


'''
mock as an argument captor
'''

# bar.py
class Bar(object):
    def biz(self, url, method, data, headers):
        pass

# foo.py
from bar import Bar

def foo(url, method='GET', data=None, headers=None):
    Bar().biz(url, method, data=data, headers=headers)

# test.py
class MyTest(unittest.TestCase):

    @patch("foo.Bar.biz")
    def test_foo(self, mock_biz):
        url = '/api/users/{id}'.format(id=1)
        data = {'phone_number': '+17025551000'}
        method = 'PUT'
        headers = {"Authorization": "JWT <your_token>"}

        foo(url, method, data=data, headers=headers)

        self.assertFalse(mock_biz.called)
        self.assertEqual(mock_biz.call_count, 1)
        self.assertEqual(mock_biz.call_args[0][0], url)
        self.assertEqual(mock_biz.call_args[0][1], method)
        self.assertEqual(mock_biz.call_args[1]['data'], data)
        self.assertEqual(mock_biz.call_args[1]['headers'], headers)

'''
mock an exceptions
'''

# Instead of having to get the application back in that exact state to cause the error, the method that threw the error can be mocked to do throw the error, 
# and then code can be written and tested to react accordingly.

# bar.py
class Bar(object):
    def biz(self):
        if some_condition():
            raise CustomException()

class CustomException(Exception):
    pass
            
# foo.py
from bar import Bar

def foo():
    Bar().biz()

# test.py
class MyTest(unittest.TestCase):

    @patch("foo.Bar.biz")
    def test_foo(self, mock_biz):
        mock_biz.side_effect = CustomException()
        
        with self.assertRaises(CustomException):
            foo()

# another example 
import unittest
from my_calendar import requests, get_holidays
from unittest.mock import patch

class TestCalendar(unittest.TestCase):
    @patch.object(requests, 'get', side_effect=requests.exceptions.Timeout)
    def test_get_holidays_timeout(self, mock_requests):
            with self.assertRaises(requests.exceptions.Timeout):
                get_holidays()

if __name__ == '__main__':
    unittest.main()

'''
testing for exceptions
'''
# use the asserRaises() method
import unittest
# A simple function to illustrate
def parse_int(s):
    return int(s)
class TestConversion(unittest.TestCase):
    def test_bad_int(self):
        self.assertRaises(ValueError, parse_int, 'N/A')




# https://aaronlelevier.github.io/python-unit-testing-with-magicmock/

################################################
# Parameterized Testing & Test Coverage
################################################
# parametrerized tests with unittest and pytest 

# use custom assert to reduce repitition of test cases

def assert_tennis_score(self, expected_score, player1_points, player2_points):
    self.assertEqual(expected_score, tennis_score(player1_points,player2_points))

# measuring coverage of tests 


# defining parameterized tests 
# using meta programming 
# first template the tests
# pass in bunch of examples as one data 

def tennis_test_template(*args):
    def foo(self):
        self.assert_tennis_score(*args)
    return foo 

    class TennisTest(unittest.TestCase):
        def assert_tennis_score(self, expected_score, player1_points, player2_points):
            self.assertEqual(expected_score, tennis_score(player1_points, player2_points))


# using pytest
from tennis import tesnnis_store
import pytest 

examples = ( ("expected_score","player1_points", "player2_points"),
            [("Love-All", 0, 0),
                ("Fifteen-All",1, 1),
                ("Thirty-All",2,2)
            ])
@pytest.mark.parametrize(*examples)                        
def test_early_game_scores_equal(expected_score, player1_points, player2_points):
    assert expected_score == tennis_score(player1_points, player2_points)


# test coverage 

# pip-3.3 install coverage
# pip-3.3 install pytest-cov

# can mark something as uninteresting #pragma: no cover 


# create config file for coverage tool 

# find missing test cases
# get legacy code under test
# continuous integration - constant management 


################################################
# doctest
################################################
# make documentation comments more truthful
# searches for pieces of text that look like interactive python sessions in docstrings and then executes those sessions
def square(x):
    """Return the square of x.
    >>> square(2)
    4
    >>> square(-2)
    4
    """
    return x*x 

if __name__ == '__main__':
    import doctest
    doctest.testmod()


# checking examples in docstrings
# regression testing 

# $ python3 -m doctest -v xx.py

# docstring runs each test while pytest treats the entire block as one test 

# tracebacks

# example doc string 

def factorial(n):
    """compute n! recursively.

    :param n: an integer >= 0
    :returns: n!

    Because of Python's stack limitation, this won't
    compute a value larger than about 1000!.
    >>> factorial(5)
    120
    """
    if n == 0: return 1
    return n*factorial(n-1)




################################################
# Assert
################################################

# https://dbader.org/blog/python-assert-tutorial

# if violating the condition, raises an AssertionError with details for errors

def apply_discount(product, discount):
    price = int(product['price'] * (1.0 - discount))
    assert 0 <= price <= product['price']
    return price


################################################
# Continuous Integration
################################################

# Continuous Integration is a software development practice where members of a team
# integrate their work frequently, usually each person integrates at least daily—leading to
# multiple integrations per day. Each integration is verified by an automated build
# (including test) to detect integration errors as quickly as possible. Many teams find that
# this approach leads to significantly reduced integration problems and allows a team to
# develop cohesive software more rapidly.

'''
Travis-CI
'''
# Travis-CI is a distributed CI server which builds tests for open source projects for
# free. It provides multiple workers that run Python tests and seamlessly integrates with
# GitHub. You can even have it comment on your pull requests2 whether this particular
# set of changes breaks the build or not.

# To get started, add a .travis.yml file to your repository with this example content:
# language: python
# python:
# - "2.6"
# - "2.7"
# - "3.3"
# - "3.4"
# script: python tests/test_all_of_the_units.py
# branches:
# only:
# - master


'''
Jenkins
'''
# Jenkins CI is an extensible continuous integration engine and currently the most popular
# CI engine. It works on Windows, Linux, and OS X and plugs in to “every Source
# Code Management (SCM) tool that exists.” Jenkins is a Java servlet (the Java equivalent
# of a Python WSGI application) that ships with its own servlet container, so you
# can run it directly using java --jar jenkins.war.



