import requests

from parser_task.serializers import serializer_factory


class ParseRequest:
    """Класс для загрузки или обновления данных справочников из внешнего API
    :param table_correspondences: словарь соответствий полей api и полей модели. Ключами являются наименования полей
    json, значениями - наименования полей модели соответствующих им.
    :param url: ссылка на внешнюю API, из которой будет проводиться загрузка данных с указанием параметра pageNum.
    :param model: модель, в которую необходимо обеспечить загрузку/обновление данных
    :param code_field: наиименование поля json в котором содержится внешний код записи, соотнеся который с полем
    модели можно найти можно найти данную запись если она существует
    :param start_page: страница с которой начинается загрузка данных из API (по умолчанию загрузка начинается
    с 1 страницы)
    :param foreign_key_fields: словарь соответствий полей модели при наличии связей с другой моделью:
    ключами являеются наименование поля json, которое соответствует полю модели, в которую заносятся даннные,
    значениями являютсяя списоки из трех значениий:
    0 - модель, к которой идет связь, 1 - наименование поля связной модели по которому строится фильтр,
    2 - наименование поля в json, которое соответствует полю в связной модели
    """

    def __init__(self, table_correspondences, url, model, code_field, foreign_key_fields=None, start_page=1):
        """
        :param table_correspondences: словарь соответствий полей api и полей модели. Ключами являются наименования полей
        json, значениями - наименования полей модели соответствующих им.
        :param url: ссылка на внешнюю API, из которой будет проводиться загрузка данных с указанием параметра pageNum.
        :param model: модель, в которую необходимо обеспечить загрузку/обновление данных
        :param code_field: наиименование поля json в котором содержится внешний код записи, соотнеся который с полем
        модели можно найти можно найти данную запись если она существует
        :param start_page: страница с которой начинается загрузка данных из API (по умолчанию загрузка начинается
        с 1 страницы)
        :param foreign_key_fields: словарь соответствий полей модели при наличии связей с другой моделью:
        ключами являеются наименование поля json, которое соответствует полю модели, в которую заносятся даннные,
        значениями являютсяя списоки из трех значениий:
        0 - модель, к которой идет связь, 1 - наименование поля связной модели по которому строится фильтр,
        2 - наименование поля в json, которое соответствует полю в связной модели
        """
        self.table_correspondences = table_correspondences
        self.url = url
        self.model = model
        self.code_field = code_field
        self.foreign_key_fields = foreign_key_fields
        self.start_page = start_page

    def download_external_api(self):
        """
        Метод для получения набора данных из внешней API и сохранение их в модель.
        При вызове данного метода начинается загрузка и сохранение данных из внешней API.
        """
        # определение списока для занесения туда записей, у которых небыло найдено указанных связей
        list_without_con = []
        # нахождение параметра pageNum в url
        for_replace = None
        for u in self.url.split('&'):
            if 'pageNum' in u:
                for_replace = u
        page = self.start_page
        # получение параметров extra_keywords и json_fields необходимых для создания сериализатора
        extra_keywords = self.get_extra_kwargs()
        json_fields = self.get_json_fields()
        # создание сериализатора с заданными параметрами
        serializer = serializer_factory(mod=self.model, list_fields=json_fields,
                                        extra_keywords=extra_keywords,
                                        field_code=self.code_field,
                                        dict_foreign_key_fields=self.foreign_key_fields)
        # начало загрузки. загрузка останавливается в случае, если пришел пустой ответ с пустыми данными
        # или произошла ошибка
        while True:
            # построение url для запроса
            base_url = self.url.replace(for_replace, f"pageNum={page}")
            print(f"url по которой происходит запрос: {base_url}")
            # отправка запроса
            r = requests.get(base_url, timeout=10)
            if (r.status_code == 200) and (r.json()['data']):
                # в случае непустого корректного ответа вычленение данных
                data = r.json()['data']

                data += list_without_con
                list_without_con = []

                for d in data:
                    # занесение записи в сериализатор, проведение валидации и в случае корректноси сохранение
                    ser = serializer(data=d)
                    if not ser.is_valid():
                        print(ser.errors)
                        continue
                    ser.save()
                    # В случае флага True запись является без указанной связи, определение этого и отправка такой
                    # записи на следующую иттерацию если такая есть
                    if ser.flag_without_connection:
                        list_without_con.append(d)

                print(f"Страница {page} из api загружена в модель\n")
                page += 1
            else:
                print(f"Загрузка завершилась на {page} странице")
                if self.foreign_key_fields:
                    print(f"Записей без связей {len(list_without_con)}")
                break

    def get_extra_kwargs(self) -> dict:
        """
        Метод для получения параметра extra_keywords, необходимого для создания сериализатора.
        Необходим для приведения входной таблицы соответствий полей к формату, требующему параметром extra_kwargs
        Meta класса сериализатора.
        """
        extra_kwargs = {}
        for (key, value) in self.table_correspondences.items():
            if key != value:
                extra_kwargs[key] = {'source': value}
        return extra_kwargs

    def get_json_fields(self) -> tuple:
        """
        Метод для получения параметра list_fields, необходимого для создания сериализатора.
        Является списком полей json, которые необходимо занести в модель.
        """
        json_fields = []
        for (key, value) in self.table_correspondences.items():
            json_fields.append(key)
        return tuple(json_fields)
