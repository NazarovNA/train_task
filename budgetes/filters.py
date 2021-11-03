from django_filters import rest_framework as filters

from budgetes import models


class BudgetFilter(filters.FilterSet):

    class Meta:
        model = models.Budget
        fields = '__all__'
