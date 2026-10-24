from rest_framework.pagination import CursorPagination


class CustomPagination(CursorPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_size = 10
    ordering = "-id"
    allowed_orderings = ("id", "-id", "date_joined", "-date_joined")

    def paginate_queryset(self, queryset, request, view=None):
        ordering_param = request.query_params.get("ordering")

        # Agar so'rovda ruxsat berilgan ordering kelgan bo'lsa, kursorni shu ustunga moslaymiz:
        if ordering_param in self.allowed_orderings:
            self.ordering = ordering_param

        return super().paginate_queryset(queryset, request, view)
