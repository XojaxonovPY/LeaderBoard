# from django_filters import DateFilter
# from django_filters.rest_framework import FilterSet
#
# from apps.models import User
#
#
# class UserFilterSet(FilterSet):
#     last_login_from = DateFilter(field_name="last_login", lookup_expr='gte')
#     last_login_to = DateFilter(field_name="last_login", lookup_expr='lte')
#
#     class Meta:
#         model = User
#         fields = ('last_login_from', 'last_login_to')
