from rest_framework import serializers

from dictionaries import models


class InstitutionTypeSerializer(serializers.ModelSerializer):
    """Серелизатор наименования типа учереждения
        """
    class Meta:
        model = models.InstitutionType
        fields = '__all__'


class OrganizationTypeSerializer(serializers.ModelSerializer):
    """Серелизатор наименования типа организации
        """
    class Meta:
        model = models.OrganizationType
        fields = '__all__'


class EgrulStatusSerializer(serializers.ModelSerializer):
    """Серелизатор наименования статуса ЕГРЮЛ
        """
    class Meta:
        model = models.EgrulStatus
        fields = '__all__'


class RubpnubpStatusSerializer(serializers.ModelSerializer):
    """Серелизатор основных совйства главы по БК
        """
    class Meta:
        model = models.RubpnubpStatus
        fields = '__all__'


class ChapterBKSerializer(serializers.ModelSerializer):
    """Серелизатор наименования типа учереждения
        """
    class Meta:
        model = models.ChapterBK
        fields = '__all__'


class IndustrySpecificTypingSerializer(serializers.ModelSerializer):
    """Серелизатор наименования отраслевой типизации
        """
    class Meta:
        model = models.IndustrySpecificTyping
        fields = '__all__'


class BudgetLevelSerializer(serializers.ModelSerializer):
    """Серелизатор наименования уровня бюджета
        """
    class Meta:
        model = models.BudgetLevel
        fields = '__all__'
