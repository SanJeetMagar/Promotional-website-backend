from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):
    page_size = 8               # 8 items per page
    page_query_param = "page"   # ?page=1
    page_size_query_param = None  # prevent changing page size
