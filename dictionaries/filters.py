from django_filters import rest_framework as filters

from dictionaries import models


class InstitutionTypeFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.InstitutionType
        fields = '__all__'


class OrganizationTypeFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.OrganizationType
        fields = '__all__'


class EgrulStatusFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.EgrulStatus
        fields = '__all__'


class RubpnubpStatusFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.RubpnubpStatus
        fields = '__all__'


class ChapterBKFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.ChapterBK
        fields = '__all__'


class IndustrySpecificTypingFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.IndustrySpecificTyping
        fields = '__all__'


class BudgetLevelFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.BudgetLevel
        fields = '__all__'
