from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import WorkBoard
from ..serializers import WorkBoardSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination 

class WorkBoardPagination(PageNumberPagination):
    page_size = 10  # Số lượng item mỗi trang
    page_size_query_param = 'page_size'
    max_page_size = 100

class WorkBoardViewSet(viewsets.ModelViewSet):
    queryset = WorkBoard.objects.all().order_by('id')
    serializer_class = WorkBoardSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = WorkBoardPagination 

 # Thêm các lớp hỗ trợ phân trang và tìm kiếm
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']  # Trường sẽ được tìm kiếm
    ordering_fields = ['name', 'created_by']
