import requests

from parser_task.serializers import serializer_factory


class ParseRequest:
    """Класс для загрузки или обновления данных справочников из внешнего api
    :param table_correspondences: словарь соответствий полей api и полей модели
    :param url: ссылка на внешнюю api с указанием параметра pageNum
    :param model: модель которую необходимо обновить
    :param code_field: наиименование поля в котором содержится внешний код записи
    :param start_page: страница с которой начинается загрузка данных из api (по умолчанию с 1 страницы)
    :param foreign_key_fields: словарь соответствий полей модели при наличии связей с другой моделью:
    ключами являеются наименование поля json, которое соответствует полю модели, в которую заносятся даннные,
    значениями являютсяя списоки из трех значениий:
    0 - модель, к которой идет связь, 1 - наименование поля связной модели по которому строится фильтр,
    2 - наименование поля в json, которое соответствует полю в связной модели
    """

    def __init__(self, table_correspondences, url, model, code_field, foreign_key_fields=None, start_page=1):

        self.table_correspondences = table_correspondences
        self.url = url
        self.model = model
        self.code_field = code_field
        self.foreign_key_fields = foreign_key_fields
        self.start_page = start_page

    def download_external_api(self):
        """Получение набора данных из внешней api и сохранение их в модель"""
        list_without_con = []
        for_replace = None
        for u in self.url.split('&'):
            if 'pageNum' in u:
                for_replace = u
        page = self.start_page

        extra_keywords = self.get_extra_kwargs()
        json_fields = self.get_json_fields()
        serializer = serializer_factory(mod=self.model, list_fields=json_fields,
                                        extra_keywords=extra_keywords,
                                        field_code=self.code_field,
                                        dict_foreign_key_fields=self.foreign_key_fields)

        while True:
            base_url = self.url.replace(for_replace, f"pageNum={page}")
            print(f"url по которой происходит запрос: {base_url}")

            r = requests.get(base_url, timeout=10)
            if (r.status_code == 200) and (r.json()['data']):
                data = r.json()['data']

                data += list_without_con
                list_without_con = []
                for d in data:
                    ser = serializer(data=d)
                    if not ser.is_valid():
                        print(ser.errors)
                        continue
                    ser.save()
                    if ser.flag_without_connection:
                        list_without_con.append(d)

                print(f"Страница {page} из api загружена в модель\n")
                page += 1
            else:
                print(f"Загрузка завершилась на {page} странице")
                if self.foreign_key_fields:
                    print(f"Записей без связей {len(list_without_con)}")
                break

    def get_extra_kwargs(self):
        extra_kwargs = {}
        for (key, value) in self.table_correspondences.items():
            if key != value:
                extra_kwargs[key] = {'source': value}
        return extra_kwargs

    def get_json_fields(self):
        json_fields = []
        for (key, value) in self.table_correspondences.items():
            json_fields.append(key)
        return tuple(json_fields)
