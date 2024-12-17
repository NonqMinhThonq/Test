

# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from .models import Task, Comment
# from .serializers import TaskSerializer, CommentSerializer
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework import status

# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         try:
#             task_id = self.kwargs.get('task_pk')
#             request.data['task'] = task_id
#             return super().create(request, *args, **kwargs)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from .models import Attachment
# from .serializers import AttachmentSerializer

# class AttachmentViewSet(viewsets.ModelViewSet):
#     queryset = Attachment.objects.all()
#     serializer_class = AttachmentSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         task_id = self.kwargs.get('task_pk')
#         request.data['task'] = task_id
#         return super().create(request, *args, **kwargs)



# from django.core.mail import send_mail
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# class NotificationView(APIView):
#     def post(self, request, *args, **kwargs):
#         subject = request.data.get('subject')
#         message = request.data.get('message')
#         recipient_list = request.data.get('recipient_list')
#         from_email= ''

#         try:
#             send_mail(subject, message, from_email, recipient_list)
#             return Response({'status': 'email sent'}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
