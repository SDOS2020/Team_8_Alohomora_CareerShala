from rest_framework import pagination


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
