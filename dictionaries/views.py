from django.shortcuts import render
from core.views import BaseModelViewSet

from dictionaries import models, serializers, filters
from core.views import BaseModelViewSet


class InstitutionTypeView(BaseModelViewSet):
    queryset = models.InstitutionType.objects.all()
    serializer_class = serializers.InstitutionTypeSerializer
    filterset_class = filters.InstitutionTypeFilter


class OrganizationTypeView(BaseModelViewSet):
    queryset = models.OrganizationType.objects.all()
    serializer_class = serializers.OrganizationTypeSerializer
    filterset_class = filters.OrganizationTypeFilter


class EgrulStatusView(BaseModelViewSet):
    queryset = models.EgrulStatus.objects.all()
    serializer_class = serializers.EgrulStatusSerializer
    filterset_class = filters.EgrulStatusFilter


class RubpnubpStatusView(BaseModelViewSet):
    queryset = models.RubpnubpStatus.objects.all()
    serializer_class = serializers.RubpnubpStatusSerializer
    filterset_class = filters.RubpnubpStatusFilter


class ChapterBKView(BaseModelViewSet):
    queryset = models.ChapterBK.objects.all()
    serializer_class = serializers.ChapterBKSerializer
    filterset_class = filters.ChapterBKFilter


class IndustrySpecificTypingView(BaseModelViewSet):
    queryset = models.IndustrySpecificTyping.objects.all()
    serializer_class = serializers.IndustrySpecificTypingSerializer
    filterset_class = filters.IndustrySpecificTypingFilter


class BudgetLevelView(BaseModelViewSet):
    queryset = models.BudgetLevel.objects.all()
    serializer_class = serializers.BudgetLevelSerializer
    filterset_class = filters.BudgetLevelFilter

