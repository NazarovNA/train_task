import requests

from parser_task.serializers import serializer_factory


class ParseRequest:
    """Класс для загрузки или обновления данных справочников из внешнего api
    :param table_correspondences: словарь соответствий полей api и полей модели
    :param url: ссылка на внешнюю api
    :param model: модель которую необходимо обновить
    :param code_field: наиименование поля в котором содержится внешний код записи
    :param start_page: страница с которой начинается загрузка данных из api (по умолчанию с 1 страницы)
    :param foreign_key_fields: словарь соответствий полей модели при наличии связей с другой моделью:
    ключами являеются поля модели, в которую заносятся даннные, значениями являютсяя списоки из трех значениий:
    0 - модель, к которой идет связь, 1 - наименование поля связной модели по которому строится фильтр,
    2 - наименование поля в json, которое соответствует полю в связной модели(в случае наличия такого поля в
    таблице соответствий, необходимо ввести наименоване поля на которое оно будет изменено)
    """

    def __init__(self, table_correspondences, url, model, code_field, foreign_key_fields=None, start_page=1):

        self.table_correspondences = table_correspondences
        self.url = url
        self.model = model
        self.code_field = code_field
        self.foreign_key_fields = foreign_key_fields
        self.start_page = start_page

    def download_external_api(self):
        """Получение набора данных из внешней api
        :return: data: список словарей, содержащих данные из api"""
        list_without_con = []
        for_replace = None
        for u in self.url.split('&'):
            if 'pageNum' in u:
                for_replace = u

        if for_replace:
            page = self.start_page
            while True:
                base_url = self.url.replace(for_replace, f"pageNum={page}")
                print(f"url по которой происходит запрос: {base_url}")
                r = requests.get(base_url, timeout=10)
                if (r.status_code == 200) and (r.json()['data']):
                    data = r.json()['data']
                    data = self.ordered_set(data)
                    serializer = serializer_factory(self.model)
                    data += list_without_con
                    print(len(list_without_con))
                    list_without_con = []
                    for d in data:
                        without_con = serializer.data_api_processing(data=d,
                                                                     table_correspondences=self.table_correspondences,
                                                                     model=self.model,
                                                                     code_field=self.code_field,
                                                                     foreign_key_fields=self.foreign_key_fields)
                        if without_con:
                            list_without_con.append(d)
                    print(f"Страница {page} из api загружена в модель\n")
                    page += 1
                else:
                    print(f"Загрузка завершилась на {page} странице")
                    break

    @staticmethod
    def ordered_set(data):
        """Метод исключения дубликатов из данных.
        :param data: входной список данных
        :return: out_list: входыные данные без дубликатов"""
        out_list = []
        for d in data:
            if not (d in out_list):
                out_list.append(d)
        return out_list
