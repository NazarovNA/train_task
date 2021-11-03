from budgetes import models, serializers, filters
from core.views import BaseModelViewSet


class BudgetView(BaseModelViewSet):
    """Модель представления бюджета
    """
    queryset = models.Budget.objects.all()
    serializer_class = serializers.BudgetSerializer
    filterset_class = filters.BudgetFilter
