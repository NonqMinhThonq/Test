from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from workapi.models import Task, TaskList, WorkBoard
from rest_framework_simplejwt.tokens import RefreshToken

class TaskViewSetTest(APITestCase):
    def setUp(self):
        # Tạo người dùng thử nghiệm
        self.user = User.objects.create_user(username='admin', password='1')
        self.client = APIClient()
        
        # Đăng nhập và lấy token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Tạo dữ liệu WorkBoard và TaskList thử nghiệm
        self.workboard = WorkBoard.objects.create(name="WorkBoard 1", created_by=self.user)
        self.tasklist = TaskList.objects.create(name="TaskList 1", board=self.workboard)
        self.task1 = Task.objects.create(name="Task 1", list=self.tasklist, status="Pending", description="First task")
        self.task2 = Task.objects.create(name="Second Task", list=self.tasklist, status="Pending", description="Second task")

    def test_create_task_in_list(self):
        url = reverse('create-task-in-list', kwargs={'pk': self.tasklist.id})
        data = {
            "name": "New Task",
            "description": "This is a new task.",
            "status": "Pending",
            "list": self.tasklist.id,  # Đảm bảo trường này được gán đúng cách
            "assigned_to": self.user.id,
            "due_date": "2024-12-31"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(Task.objects.last().name, "New Task")
        print('TC005 Kiểm tra tạo Task', response.status_code)

    def test_update_status(self):
        url = reverse('task-update-status', kwargs={'pk': self.task1.id})
        data = {
            "status": "Completed"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(Task.objects.get(id=self.task1.id).status, "Completed")
        print('TC006 Kiểm tra cập nhật trạng thái Task',response.status_code)

    def test_destroy_task(self):
        url = reverse('task-destroy', kwargs={'pk': self.task1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Task.objects.get(id=self.task1.id).is_deleted)
        print('TC007 Kiểm tra xóa Task',response.status_code)

    def test_search_task(self):
        url = reverse('task-list')  # Đảm bảo tên URL này khớp với tên bạn đã đặt trong urls.py
        response = self.client.get(url, {'search': 'Task'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Nên trả về cả Task 1 và Second Task

        response = self.client.get(url, {'search': 'First'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Task 1')
        print('TC009 Kiểm tra tìm kiếm Task',response.status_code)

    def test_handle_api_error(self):
        url = reverse('create-task-in-list', kwargs={'pk': self.tasklist.id})
        data = {
            # intentionally leaving out 'name' to simulate missing data
            "description": "This task has no name.",
            "status": "Pending",
            "list": self.tasklist.id,
            "assigned_to": self.user.id,
            "due_date": "2024-12-31"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'][0], 'This field is required.')
        print('TC010 Kiểm tra xử lý lỗi API',response.status_code)
