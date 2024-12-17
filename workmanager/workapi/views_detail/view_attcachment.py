from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Attachment
from ..serializers import AttachmentSerializer

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        task_id = self.kwargs.get('task_pk')
        request.data['task'] = task_id
        return super().create(request, *args, **kwargs)
