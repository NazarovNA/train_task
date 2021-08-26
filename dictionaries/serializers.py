from rest_framework import serializers

from dictionaries import models


class InstitutionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InstitutionType
        fields = '__all__'


class OrganizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrganizationType
        fields = '__all__'


class EgrulStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EgrulStatus
        fields = '__all__'


class RubpnubpStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RubpnubpStatus
        fields = '__all__'


class ChapterBKSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChapterBK
        fields = '__all__'


class IndustrySpecificTypingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndustrySpecificTyping
        fields = '__all__'


class BudgetLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BudgetLevel
        fields = '__all__'
