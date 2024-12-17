from django.core import mail
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

class NotificationViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('send_notification')  # Đảm bảo tên URL này khớp với tên bạn đã đặt trong urls.py

    def test_send_email_success(self):
        data = {
            "subject": "Test Subject",
            "message": "thong bao id 123",
            "recipient_list": ["test@example.com"]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'email sent'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test Subject')
        print('TC008 Kiểm tra API gửi email thông báo khi tạo mới công việc.',response.status_code)