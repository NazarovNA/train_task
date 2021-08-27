from characteristics_organizations.models import Organization
from characteristics_organizations.serializers import OrganizationSerializer
from characteristics_organizations.filters import OrganizationFilter
from core.views import BaseModelViewSet


class OrganizationView(BaseModelViewSet):
    queryset = Organization.objects.all().order_by('id')
    serializer_class = OrganizationSerializer
    filterset_class = OrganizationFilter
