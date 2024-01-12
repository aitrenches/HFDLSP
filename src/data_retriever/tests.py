from django.test import TestCase
from unittest import mock
from .service import fetch_huggingface_dataset


class FetchHuggingFaceDatasetTests(TestCase):
    @mock.patch("datasets.load_dataset")
    def test_valid_dataset(self, mock_load_dataset):
        mock_load_dataset.return_value = "test"
        dataset = fetch_huggingface_dataset("time_qa")
        self.assertEqual(dataset, "test")

    @mock.patch("datasets.load_dataset")
    def test_invalid_dataset(self, mock_load_dataset):
        mock_load_dataset.side_effect = Exception("Dataset not found")
        dataset = fetch_huggingface_dataset("invalid_dataset")
        self.assertIsNone(dataset)
