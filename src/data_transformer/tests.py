from django.test import TestCase
from unittest.mock import patch
from HFDLSP.models import HotpotQADataset
from .service import fetch_dataset_answer_by_question


class FetchDatasetAnswerByQuestionTest(TestCase):
    def setUp(self):
        self.dataset = HotpotQADataset(
            question="what is biology",
            answer="Biology is a branch of science",
            context="A question  about biology",
        )

    def test_invalid_dataset(self):
        self.assertIsNone(fetch_dataset_answer_by_question("Invalid ID", "question"))

    @patch("HFDLSP.models.HotpotQADataset.nodes")
    def test_no_dataset_with_question(self, mock_nodes):
        mock_nodes.first_or_none.return_value = None
        self.assertIsNone(
            fetch_dataset_answer_by_question("hotpot_qa", "what is biology")
        )
        mock_nodes.first_or_none.assert_called_once_with(question="what is biology")

    @patch("HFDLSP.models.HotpotQADataset.nodes")
    def test_valid_dataset(self, mock_nodes):
        mock_nodes.first_or_none.return_value = self.dataset
        result = fetch_dataset_answer_by_question("hotpot_qa", "what is biology")

        self.assertEqual(result, self.dataset.answer)
        mock_nodes.first_or_none.assert_called_once_with(question="what is biology")
