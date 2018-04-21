"""Test for discover module

Copyright 2018 Spectre Team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
    
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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

test_listdir = [
    "dataset_number_one",
    "dataset_number_two",
    "dataset_number_three"
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

class TestGetDatasets(unittest.TestCase):
    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_returns_correct_datasets_set(self, mock_isdir, mock_listdir):
        mock_isdir.return_value = True
        mock_listdir.return_value = test_listdir 
        self.assertEqual(disc.get_datasets(), test_datasets)

class TestDatasetExists(unittest.TestCase):
    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_returns_true_for_existing_dataset(self, mock_isdir, mock_listdir):
        mock_isdir.return_value = True
        mock_listdir.return_value = test_listdir 
        self.assertTrue(disc.dataset_exists("dataset number one"))

    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_returns_false_for_nonexisting_dataset(self, mock_isdir, mock_listdir):
        mock_isdir.return_value = True
        mock_listdir.return_value = test_listdir 
        self.assertFalse(disc.dataset_exists("dataset number four"))
