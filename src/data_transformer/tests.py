from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class ApiIntegrationTest(TestCase):
    def setUp(self):
        # Set up any necessary data for your tests
        self.client = APIClient()

    def test_get_endpoint(self):
        url = reverse('"answer/", answer_view, name="answer"')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions based on your API response

    # def test_post_endpoint(self):
    #     url = reverse('your-api-endpoint')
    #     data = {'key': 'value'}
    #     response = self.client.post(url, data, format='json')

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Add more assertions based on your API response
