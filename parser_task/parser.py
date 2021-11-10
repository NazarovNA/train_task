import copy

import requests

from parser_task.serializers import ParseApiSerializer

import logging


class ParseExternalApi:
    """
    Класс для загрузки и обновления данных справочников из внешнего API.
    :param model: модель в которую необходимо обеспечить загрузку.
    :param extend_extra_kwargs: словарь - дополнение к extra_kwargs. Ключами являеются наименования полей json для
    занесения модели. Значениями являются словари, которые запоняются по шаблону
    {'Поле json': {'foreign_model': 'Модель в которой ищем', 'foreign_model_lookup_field':'Поле по которому ищем',
    'values_map': {'Какое значение': 'На какое заменяем'}}
    Для указания поля pk в json с внешним кодом записи, по которому можно найти запись в модели необходимо заполнить
    параметры foreign_model: и foreign_model_lookup_field.
    Для замены определенных значений поля необходимо заполнить параметр values_map.
    :param json_fields кортеж полей json для заполнения модели
    :param extra_kwargs является таблией соответствий при различных наменованиях полей json и соответствующих
    им полей модели. Передается в формате: {наименование поля json: 'source': наименование поля в модели}
    :param base_url: ссылка на API, без указания параметров запроса.
    :param url_settings: параметры запроса к API для url
    """

    def __init__(self, model, extend_extra_kwargs, json_fields, extra_kwargs, base_url, url_settings=''):
        """
        :param model: модель в которую необходимо обеспечить загрузку.
        :param extend_extra_kwargs: ссловарь - дополнение к extra_kwargs. Ключами являеются наименования полей json для
        занесения модели. Значениями являются словари, которые запоняются по шаблону
        {'Поле json': {'foreign_model': 'Модель в которой ищем', 'foreign_model_lookup_field':'Поле по которому ищем',
        'values_map': {'Какое значение': 'На какое заменяем'}}
        Для указания поля pk в json с внешним кодом записи, по которому можно найти запись в модели необходимо заполнить
        параметры foreign_model: и foreign_model_lookup_field.
        Для замены определенных значений поля необходимо заполнить параметр values_map.
        :param json_fields кортеж полей json для заполнения модели
        :param extra_kwargs является таблией соответствий при различных наменованиях полей json и соответствующих
        им полей модели. Передается в формате: {наименование поля json: 'source': наименование поля в модели}
        :param base_url: ссылка на API, без указания параметров запроса.
        :param url_settings: параметры запроса к API для url
        """

        self.extend_extra_kwargs = extend_extra_kwargs
        self.extra_kwargs = extra_kwargs
        self.json_fields = json_fields
        self.model = model
        self.base_url = base_url
        self.url_settings = url_settings
        self.logger = logging.getLogger(__name__)

    def download_api(self):
        """
        Метод для получения набора данных из API и сохранения их в модель.
        При вызове данного метода начинается загрузка и сохранение данных из внешней API.
        """
        page_number = 1
        page_size = 1000
        page_count = 1
        not_imported_json_data = []
        serializer = self.get_serializer()

        # загрузка и запись/обновление данных
        while page_number <= page_count:
            request = self.make_request(page_size, page_number)  # произведение запроса к API
            if request is None:
                break
            data = request['data']
            page_count = int(request['pageCount'])
            not_imported_json, imported = self.deserializing(serializer=serializer, data=data)
            not_imported_json_data.extend(not_imported_json)
            self.logger.info(f"Страница {page_number} из api загружена")
            page_number += 1

        # дозагрузка невалидных ранее данных
        imported = 1
        while not_imported_json_data and imported:
            not_imported_json_data, imported = self.deserializing(serializer=serializer, data=not_imported_json_data)

        if not not_imported_json_data:
            self.deserializing(serializer=serializer, data=not_imported_json_data, flag_logger=True)
            self.logger.warning(f"Загрузка в модель завершена. {len(not_imported_json_data)} записей невалидны.")
        else:
            self.logger.info('Загрузка в модель полностью завершена')

    def make_request(self, size_page, page_number):
        """
        Метод для отправки запроса к API.
        """
        url = f"{self.base_url}?pageSize={size_page}&{self.url_settings}&pageNum={page_number}"
        self.logger.info(f"url по которой происходит запрос: {url}")
        try:
            req = requests.get(url, timeout=10)
        except:
            self.logger.error(f"Загрузка данных на странице {page_number} вызвала ошибку")
            return None

        if (req.status_code == 200) and len(req.json()['data']) != 0:
            return req.json()
        elif (req.status_code == 200) and len(req.json()['data']) == 0:
            self.logger.error(f"При загрузке данных на странице {page_number} получен пустой ответ")
            return None
        else:
            self.logger.error(f"Загрузка данных на странице {page_number} вызвала ошибку {req.status_code}")
            return None

    def deserializing(self, serializer, data, flag_logger=False):
        """
        Метод, предназначенный для десериализации записи и сохранения ее в модель
        :param serializer: настроенный сериализатор
        :param data: данные, которые необходимо сохранить
        :param flag_logger: флаг для включения логирования ошибок
        :return not_imported_json: данные, которые не удалось загрузить
        :return imported: количество произведенных сохранений
        """
        not_imported_json = []
        imported = 0
        for record in data:
            deserialized_data = serializer(data=copy.deepcopy(record))
            if not deserialized_data.is_valid():
                if flag_logger:
                    self.logger.warning(deserialized_data.errors)
                not_imported_json.append(record)
                continue
            deserialized_data.save()
            imported += 1

        return not_imported_json, imported

    def get_serializer(self):
        """
        Метод для создания сериализатора с настройками для указанной модели.
        """
        class ConfiguredSerializer(ParseApiSerializer):
            class Meta:
                model = self.model
                fields = self.json_fields
                extra_kwargs = self.extra_kwargs
                extend_extra_kwargs = self.extend_extra_kwargs

        return ConfiguredSerializer
