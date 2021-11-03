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
                    self.data_processing_and_save_in_model(data)
                    print(f"Страница {page} из api загружена в модель")
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

    def renaming_keys(self, data):
        """Метод приведения ключей данных к таблице соответствия
        :param data: список словарей
        :return: new_data: входные данные с обновленными значениями ключей по таблице"""
        new_data = []
        for i, d_json in enumerate(data):
            d = {}
            for (key, value) in d_json.items():
                if not value:
                    value = None
                if key in self.table_correspondences.keys():
                    d[self.table_correspondences[key]] = value
                else:
                    d[key] = value
            new_data.append(d)
        return new_data

    def save_list_data(self, data):
        """Метод для сохранения списка данных в модель
        :param data: список словарей данных"""
        set_objects = self.model.objects.all()

        for d in data:
            obj = set_objects.filter(**{self.code_field: d[self.code_field]})
            if obj.exists():
                instance = obj[0]
            else:
                instance = None

            # занесение в связные поля модели объекты связных моделей
            if self.foreign_key_fields:
                for (key, value) in d.items():
                    if key in self.foreign_key_fields.keys():
                        connection = self.foreign_key_fields[key]
                        if d[connection[2]]:
                            connection_value = connection[0].objects.filter(**{connection[1]: d[connection[2]]})
                            if connection_value:
                                d[key] = connection_value[0].id
                            else:
                                d[key] = None
                        else:
                            d[key] = None

            serializer = serializer_factory(self.model)
            ser = serializer(instance=instance, data=d)
            if ser.is_valid():
                ser.save()
            else:
                for error_key in ser.errors.keys():
                    d.pop(error_key, None)
                ser = serializer(instance=instance, data=d)
                if ser.is_valid():
                    ser.save()
                else:
                    print(ser.errors)

    def data_processing_and_save_in_model(self, data):
        """Метод для обработки данных, приведения к таблице соответствия и сохранения данных в модель
        :param data: список словарей данных"""

        new_data = self.renaming_keys(data)
        new_data = self.ordered_set(new_data)
        self.save_list_data(new_data)
