from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import TaskList
from ..serializers import TaskListSerializer


class TaskListViewSet(viewsets.ModelViewSet):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        workboard_pk = self.kwargs.get('workboard_pk')
        return TaskList.objects.filter(board_id=workboard_pk)

    def create(self, request, *args, **kwargs):
        workboard_pk = self.kwargs.get('workboard_pk')
        request.data['board'] = workboard_pk
        return super().create(request, *args, **kwargs)
