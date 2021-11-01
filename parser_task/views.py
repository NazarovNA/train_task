from django.shortcuts import render
from core.views import BaseModelViewSet

from parser_task import models, serializers, filters
from core.views import BaseModelViewSet


class BudgetView(BaseModelViewSet):
    """Модель представления типа учереждения
    """
    queryset = models.Budget.objects.all()
    serializer_class = serializers.BudgetSerializer
    filterset_class = filters.BudgetFilter
