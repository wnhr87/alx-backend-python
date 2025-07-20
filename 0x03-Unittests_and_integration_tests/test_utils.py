#!/usr/bin/env python3
"""unit tests for utils functions """
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import *


class TestAccessNestedMap(unittest.TestCase):
    """
    Test case class for testing the access_nested_map function.
    """
    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a"], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2)
    ])
    def test_access_nested_map(self, nested_map, sequence, expected):
        """ tests access_nested_map function"""
        self.assertEqual(access_nested_map(nested_map, sequence), expected)

    @parameterized.expand([
        ({}, ["a"], KeyError),
        ({"a": 1}, ["a", "b"], KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map, sequence, expected):
        """ """
        # self.assertRaises(KeyError, access_nested_map, nested_map, sequence)
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, sequence), expected


class TestGetJson(unittest.TestCase):
    """ Test case class for testing the get_json method."""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("requests.get")
    def test_get_json(self, test_url, test_payload, mock_get_json):
        """ test that utils.get_json returns the expected result """
        mock_resp = Mock()
        mock_resp.json.return_value = test_payload

        mock_get_json.return_value = mock_resp

        res = get_json(test_url)
        mock_get_json.assert_called_once_with(test_url)
        self.assertEqual(res, test_payload)


class TestMemoize(unittest.TestCase):
    """ test case class for testing memoization(caching) decorator
    that's applied to a method."""
    def test_memoize(self):
        """
        mocks `a_method` to track how many times it is called.
        """
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        obj = TestClass()
        with patch.object(TestClass, "a_method") as mock_method:
            mock_method.return_value = 42
            res1 = obj.a_property
            res2 = obj.a_property
            mock_method.assert_called_once
