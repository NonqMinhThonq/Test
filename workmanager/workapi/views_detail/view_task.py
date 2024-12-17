from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ..models import Task, TaskList
from ..serializers import TaskSerializer
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']

    # POST: Thêm thẻ công việc vào danh sách
    @action(detail=True, methods=['post'], url_path='create-task-in-list', url_name='create-task-in-list')
    def create_task_in_list(self, request, pk=None):
        try:
            # Kiểm tra xem tasklist_id có tồn tại không
            try:
                tasklist = TaskList.objects.get(pk=pk)
            except TaskList.DoesNotExist:
                return Response({
                    "error": "Danh sách công việc không tồn tại."
                }, status=status.HTTP_404_NOT_FOUND)

            # Thêm Task vào danh sách này
            data = request.data.copy()
            data['list'] = tasklist.id  # Gắn danh sách vào công việc

            # Tạo serializer với dữ liệu đã sửa
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Công việc đã được tạo thành công.",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PATCH: Cập nhật trạng thái công việc
    @action(detail=True, methods=['patch'], url_path='update_status')
    def update_status(self, request, pk=None):
        try:
            task = self.get_object()
            new_status = request.data.get('status')
            if new_status not in ['Pending', 'Completed']:
                return Response({"error": "Trạng thái không hợp lệ."}, status=status.HTTP_400_BAD_REQUEST)

            task.status = new_status
            task.save()
            return Response({
                "message": "Trạng thái đã được cập nhật.",
                "task": TaskSerializer(task).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE: Xóa công việc
    def destroy(self, request, *args, **kwargs):
        try:
            task = self.get_object()
            task.is_deleted = True  # Đánh dấu là đã xóa
            task.save()
            return Response({
                "message": "Công việc đã được xóa thành công."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
