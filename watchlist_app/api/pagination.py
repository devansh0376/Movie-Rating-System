from rest_framework.pagination import PageNumberPagination ,LimitOffsetPagination,CursorPagination
class WatchListPagination(PageNumberPagination):
    page_size = 3
    #customize pagination settings
    #page_size_query_param=size'
    #max_page_size =10
    #last_page_strings='last'

class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 3

class WatchListCPagination(CursorPagination):
    page_size =2

     