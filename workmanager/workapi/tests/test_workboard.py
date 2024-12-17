from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from ..models import WorkBoard

class WorkBoardAPITestCase(APITestCase):
    def setUp(self):
        # Tạo user test
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # Xác thực client

        # URL API
        self.create_url = '/api/workboards/'  # URL tạo bảng công việc
        self.list_url = '/api/workboards/?page=1'  # URL lấy danh sách với phân trang

    def test_create_workboard(self):
        """ TC003: Tạo bảng công việc mới qua API """
        payload = {
            "name": "Dự án A",
            "created_by": self.user.id
        }
        response = self.client.post(self.create_url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Dự án A")
        self.assertTrue(WorkBoard.objects.filter(name="Dự án A").exists())
        print('TC003 Tạo bảng công việc mới qua API',response.status_code)

    def test_list_workboards_with_pagination(self):
        """ TC004: Lấy danh sách bảng công việc với phân trang """
        # Tạo dữ liệu mẫu
        for i in range(15):
            WorkBoard.objects.create(name=f"Board {i}", created_by=self.user)
        
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # Kiểm tra số lượng item trên trang
        self.assertIn('count', response.data)  # Đảm bảo có tổng số lượng bản ghi
        self.assertEqual(response.data['count'], 15)
        print('TC004 Lấy danh sách bảng công việc với phân trang',response.status_code)
