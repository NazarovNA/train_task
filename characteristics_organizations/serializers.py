from rest_framework import serializers

from characteristics_organizations.models import Organization
from dictionaries import serializers as sr


class OrganizationSerializer(serializers.ModelSerializer):

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
