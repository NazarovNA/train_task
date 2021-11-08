"""Пример использования алгоритма, для загрузки и обновления данных модели Budget"""

from budgetes.models import Budget
from parser_task.parser import ParseRequest
from parser_task.serializers import AbstractSerializer


class SerializerParse(AbstractSerializer):
    class Meta:
        model = Budget
        fields = ('code', 'name', 'parentcode', 'enddate', 'startdate', 'status', 'budgtypecode')
        extra_kwargs = {'budgtypecode': {'source': 'budgettype'}}
        code_field = 'code'
        foreign_key_fields = {'parentcode': [Budget, 'code', 'parentcode']}


url = "http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data?pageSize=1000&filterstatus=ACTIVE&pageNum=1"

a = ParseRequest(serializer=SerializerParse, url=url)
a.download_external_api()
