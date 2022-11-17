from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from printer.models import Printer, Check
from rest_framework import status


class TestEndpoints(APITestCase):

    def setUp(self):
        self.ROOT_API_URL = "/api/v1"
        self.client = APIClient()
        self.check = Check.objects.create(status='new')

    def get_api(self, loc=""):
        if loc:
            return "%s%s" % (self.ROOT_API_URL, loc)
        else:
            return self.ROOT_API_URL

    def test_endpoints_flow(self):
        response = self.client.get(self.get_api("/check/"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(self.get_api("/check/1/"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # HTTP_202_ACCEPTED)
        check = response.json()
        data = {
            'status': 'printed'
        }
        response = self.client.put(self.get_api(f"/check/{check['id']}/"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], True)
