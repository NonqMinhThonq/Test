from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from workapi.views_detail.view_workboard import WorkBoardViewSet
from workapi.views_detail.view_tasklist import TaskListViewSet
from workapi.views_detail.view_task import TaskViewSet
from workapi.views_detail.view_attcachment import AttachmentViewSet
from workapi.views_detail.view_comment import CommentViewSet
from workapi.views_detail.view_notification import NotificationView

router = DefaultRouter()
router.register(r'workboards', WorkBoardViewSet, basename='workboard') 
router.register(r'tasklists', TaskListViewSet, basename='tasklist') 
router.register(r'tasks', TaskViewSet, basename='task') 
router.register(r'comments', CommentViewSet, basename='comment') 
router.register(r'attachments', AttachmentViewSet, basename='attachment')

urlpatterns = [
    path('', include(router.urls)),
    path('workboards/<int:workboard_pk>/', include(router.urls)),
    path('tasklists/<int:task_pk>/tasks/', TaskViewSet.as_view({'post': 'create'}), name='task-create'),
    path('tasklists/<int:pk>/tasks/', TaskViewSet.as_view({'post': 'create_task_in_list'}), name='create-task-in-list'),
    path('tasks/<int:pk>/update_status/', TaskViewSet.as_view({'patch': 'update_status'}), name='task-update-status'),
    path('tasks/<int:pk>/', TaskViewSet.as_view({'delete': 'destroy'}), name='task-destroy'),
    path('tasks/<int:task_pk>/comments/', CommentViewSet.as_view({'post': 'create'}), name='comment-create'),
    path('tasks/<int:task_pk>/attachments/', AttachmentViewSet.as_view({'post': 'create'}), name='attachment-create'),
    path('notifications/', NotificationView.as_view(), name='send_notification'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
