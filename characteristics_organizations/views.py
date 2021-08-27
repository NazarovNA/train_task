from rest_framework.decorators import action
from rest_framework.response import Response

from characteristics_organizations.models import Organization
from characteristics_organizations.serializers import OrganizationSerializer
from characteristics_organizations.filters import OrganizationFilter
from core.views import BaseModelViewSet


class OrganizationView(BaseModelViewSet):
    queryset = Organization.objects.all().order_by('id')
    serializer_class = OrganizationSerializer
    filterset_class = OrganizationFilter

    @action(methods=['get'], detail=False)
    def fed_budget(self, request):
        queryset = self.get_queryset().filter(budget_level__id=1)
        serializer = self.get_serializer(data=queryset)

        return Response(serializer.data)
