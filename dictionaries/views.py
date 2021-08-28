from django.shortcuts import render
from core.views import BaseModelViewSet

from dictionaries import models, serializers, filters
from core.views import BaseModelViewSet


class InstitutionTypeView(BaseModelViewSet):
    """Модель представления типа учереждения
    """
    queryset = models.InstitutionType.objects.all()
    serializer_class = serializers.InstitutionTypeSerializer
    filterset_class = filters.InstitutionTypeFilter


class OrganizationTypeView(BaseModelViewSet):
    """Модель представления типа организации
    """
    queryset = models.OrganizationType.objects.all()
    serializer_class = serializers.OrganizationTypeSerializer
    filterset_class = filters.OrganizationTypeFilter


class EgrulStatusView(BaseModelViewSet):
    """Модель представления статуса ЕГРЮЛ
    """
    queryset = models.EgrulStatus.objects.all()
    serializer_class = serializers.EgrulStatusSerializer
    filterset_class = filters.EgrulStatusFilter


class RubpnubpStatusView(BaseModelViewSet):
    """Модель представления статуса РУБПНУБП
    """
    queryset = models.RubpnubpStatus.objects.all()
    serializer_class = serializers.RubpnubpStatusSerializer
    filterset_class = filters.RubpnubpStatusFilter


class ChapterBKView(BaseModelViewSet):
    """Модель представления основных совйств главы по БК
    """
    queryset = models.ChapterBK.objects.all()
    serializer_class = serializers.ChapterBKSerializer
    filterset_class = filters.ChapterBKFilter


class IndustrySpecificTypingView(BaseModelViewSet):
    """Модель представления отраслевой типизации
    """
    queryset = models.IndustrySpecificTyping.objects.all()
    serializer_class = serializers.IndustrySpecificTypingSerializer
    filterset_class = filters.IndustrySpecificTypingFilter


class BudgetLevelView(BaseModelViewSet):
    """Модель представления уровня бюджета
    """
    queryset = models.BudgetLevel.objects.all()
    serializer_class = serializers.BudgetLevelSerializer
    filterset_class = filters.BudgetLevelFilter

