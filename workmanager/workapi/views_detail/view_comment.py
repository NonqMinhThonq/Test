from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import  Comment
from ..serializers import  CommentSerializer
from rest_framework.response import Response
from rest_framework import status

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            task_id = self.kwargs.get('task_pk')
            request.data['task'] = task_id
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)