from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = 'recipes_limit'


class CustomPageNumberPaginator(PageNumberPagination):
    page_size_query_param = 'recipes_limit'
