from parser_task.models import Budget
from parser_task.parser import ParseRequest

table_of_correspondences = {'code': 'code',
                            'name': 'name',
                            'parentcode': 'parentcode',
                            'enddate': 'enddate',
                            'startdate': 'startdate',
                            'status': 'status',
                            'budgtypecode': 'budgettype'}

url = "http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data?pageSize=1000&filterstatus=ACTIVE&pageNum=1"
model = Budget
code_field = 'code'
parent_field = 'parentcode'


a = ParseRequest(table_of_correspondences, url, model, code_field, parent_field)
data = a.external_api_view()
a.data_processing_and_save_in_model(data)
