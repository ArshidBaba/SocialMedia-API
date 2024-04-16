from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    """Pagination for User List"""

    page_size = 10
    max_page_size = 10
