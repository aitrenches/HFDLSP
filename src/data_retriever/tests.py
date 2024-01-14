from django.test import TestCase
from unittest.mock import patch
from .service import fetch_huggingface_dataset, insert_dataset_into_neo4j


class FetchHuggingfaceDatasetTest(TestCase):
    def test_invalid_dataset(self):
        self.assertIsNone(fetch_huggingface_dataset("Invalid ID"))

    @patch("datasets.load_dataset")
    def test_valid_dataset(self, mock_load_dataset):
        dataset_id = "hotpot_qa"
        datasets = [
            {
                "question": "What is biology",
                "answer": "Biology is a branch of science",
                "context": "A question  about biology",
            }
        ]
        mock_load_dataset.return_value = datasets
        result = fetch_huggingface_dataset(dataset_id)

        self.assertEqual(result[0]["question"], datasets[0]["question"])
        mock_load_dataset.assert_called_with("hotpot_qa", "distractor", split="train")


class InsertDatasetIntoNeo4jTest(TestCase):
    def test_invalid_dataset_id(self):
        self.assertIsNone(insert_dataset_into_neo4j("Invalid ID", []))

    def test_invalid_dataset(self):
        dataset_id = "hotpot_qa"
        dataset = [
            {
                "invalid_key": "invalid_value",
            }
        ]
        with self.assertRaises(KeyError):
            insert_dataset_into_neo4j(dataset_id, dataset)

    @patch("HFDLSP.models.HotpotQADataset.create")
    def test_valid_dataset(self, mock_model):
        dataset_id = "hotpot_qa"
        dataset = [
            {
                "question": "What is biology",
                "answer": "Biology is a branch of science",
                "context": "A question  about biology",
            }
        ]
        self.assertIsNone(insert_dataset_into_neo4j(dataset_id, dataset))
        mock_model.assert_called_once_with(
            {
                "question": dataset[0]["question"],
                "answer": dataset[0]["answer"],
                "context": dataset[0]["context"],
            }
        )
