from rest_framework import serializers

from characteristics_organizations.models import Organization
from dictionaries import serializers as sr


class OrganizationSerializer(serializers.ModelSerializer):

    @staticmethod
    def validate_inn(data):
        """
        Check that start is before finish.
        """
        if len(data) != 10:
            raise serializers.ValidationError("ИНН не соотвтествует стандартной длине")
        return data

    @staticmethod
    def validate_kpp(data):
        """
        Check that start is before finish.
        """
        if len(data) != 9:
            raise serializers.ValidationError("КПП не соотвтествует стандартной длине")
        return data

    class Meta:
        model = Organization
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['institution_type'] = sr.InstitutionTypeSerializer()
        self.fields['organization_type'] = sr.OrganizationTypeSerializer()
        self.fields['egrul_status'] = sr.EgrulStatusSerializer()
        self.fields['rubpnubp_status'] = sr.RubpnubpStatusSerializer()
        self.fields['chapter_bk'] = sr.ChapterBKSerializer()
        self.fields['industry_specific_typing'] = sr.IndustrySpecificTypingSerializer()
        self.fields['budget_level'] = sr.BudgetLevelSerializer()
        return super().to_representation(instance)
