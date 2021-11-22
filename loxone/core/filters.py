import rest_framework_filters as filters


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class BaseFilter(filters.FilterSet):
    status = CharInFilter(field_name="status", lookup_expr="in")
