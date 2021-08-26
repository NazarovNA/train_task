from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters

from core.paginations import PaginationData


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PaginationData
    permission_actions = ('list', 'retrieve')
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    def get_permissions(self):
        permission_classes = super().get_permissions()
        if self.action not in self.permission_actions:
            permission_classes.append(permissions.IsAdminUser())
        return permission_classes
