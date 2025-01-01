from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

class FileUploadTestCase(APITestCase):
    def test_file_upload(self):
        file = SimpleUploadedFile("testfile.txt", b"file_content", content_type="text/plain")
        response = self.client.post('/api/upload/', {'file': file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('file_url', response.data)
