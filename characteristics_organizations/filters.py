from django_filters import rest_framework as filters

from characteristics_organizations.models import Organization


class OrganizationFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    institution_type = filters.NumberFilter()
    organization_type = filters.NumberFilter()
    egrul_status = filters.NumberFilter()
    rubpnubp_status = filters.NumberFilter()
    chapter_bk = filters.CharFilter(field_name='chapter_bk__name', lookup_expr='icontains')
    industry_specific_typing = filters.NumberFilter()
    budget_level = filters.NumberFilter()

    class Meta:
        model = Organization
        fields = '__all__'

