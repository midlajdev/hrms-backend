from rest_framework.pagination import PageNumberPagination, CursorPagination

class CustomPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"
    max_page_size = 20


# class CustomPagination(CursorPagination):
#     page_size = 5
#     ordering = "-created_at"