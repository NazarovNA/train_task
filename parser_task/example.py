"""Пример использования алгоритма, для загрузки и обновления данных модели Budget"""

from parser_task.parser import ParseExternalApi
from budgetes.models import Budget

url_settings = 'filterstatus=ACTIVE'

base_url = "http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data"
url_settings = 'filterstatus=ACTIVE'
extra_kwargs = {'budgtypecode': {'source': 'budgettype'}}
extend_extra_kwargs = {'parentcode': {'foreign_model': Budget, 'foreign_model_lookup_field': 'code',
                                      'values_map': {'00000000': None}},
                       'code': {'foreign_model': Budget, 'foreign_model_lookup_field': 'code'}}

json_fields = ('code', 'name', 'parentcode', 'enddate', 'startdate', 'status', 'budgtypecode')

model = Budget

a = ParseExternalApi(base_url=base_url, url_settings=url_settings, extra_kwargs=extra_kwargs,
                     extend_extra_kwargs=extend_extra_kwargs, json_fields=json_fields, model=model)
a.download_api()

