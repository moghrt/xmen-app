from rest_framework.pagination import PageNumberPagination
from django.conf import settings

class UsersNumberPagination(PageNumberPagination):
    page_size = settings.REST_FRAMEWORK['USERS_PER_PAGE']
    page_size_query_param = 'page_size'