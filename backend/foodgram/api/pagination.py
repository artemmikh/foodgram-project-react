from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = 'recipes_limit'
