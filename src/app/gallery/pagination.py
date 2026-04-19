# from rest_framework.pagination import PageNumberPagination
# from rest_framework.response import Response
# import math

# class CustomGalleryPagination(PageNumberPagination):
#     page_size = 15  # items per page
#     page_size_query_param = 'page_size'
#     max_page_size = 50

#     def get_paginated_response(self, data):
#         total_items = self.page.paginator.count
#         items_per_page = self.get_page_size(self.request)
#         total_pages = math.ceil(total_items / items_per_page)
        
#         return Response({
#             "currentPage": self.page.number,
#             "totalPages": total_pages,
#             "totalItems": total_items,
#             "itemsPerPage": items_per_page,
#             "results": data
#         })
