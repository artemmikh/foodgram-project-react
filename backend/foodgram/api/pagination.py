from rest_framework.pagination import PageNumberPagination


class FollowListPageNumberPaginator(PageNumberPagination):
    page_size_query_param = 'limit'
