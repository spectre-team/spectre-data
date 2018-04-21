import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from typing import List, Dict

import spdata.discover as disc
from spdata.common import Path, Name

test_datasets = [
    { "name": "dataset number one", "value": "dataset_number_one"},
    { "name": "dataset number two", "value": "dataset_number_two"},
    { "name": "dataset number three", "value": "dataset_number_three"}
]

class TestNameToId(unittest.TestCase):
    @patch('spdata.discover.get_datasets')
    def test_generates_some_unique_ids(self, mock):
        mock.return_value = test_datasets
        ids = {disc.name_to_id(value) for _, value in enumerate(d['name'] for d in disc.get_datasets())}
        self.assertEqual(len(ids), len(test_datasets))

    def test_id_is_consistent_for_the_same_name(self):
        self.assertEqual(disc.name_to_id("name"), disc.name_to_id("name"))

class TestIdToName(unittest.TestCase):
    @patch('spdata.discover.get_datasets')
    def test_finds_name_by_its_id(self, mock):
        mock.return_value = test_datasets
        some_name = test_datasets[1]['name']
        some_id = disc.name_to_id(some_name)
        self.assertEqual(
            disc.id_to_name(some_id),
            some_name
        )

    @patch('spdata.discover.get_datasets')
    def test_throws_for_nonexistent_name(self, mock):
        mock.return_value = test_datasets
        with self.assertRaises(disc.UnknownIdError):
            disc.id_to_name(123)