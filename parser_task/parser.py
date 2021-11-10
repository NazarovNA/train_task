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
    Для указания поля pk в json с внешним кодом записи, по которому можно найти запись в модели необходимо в заполнить
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
        Для указания поля pk в json с внешним кодом записи, по которому можно найти запись в модели необходимо в заполнить
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
        invalid_data = []
        serializer = self.get_serializer()
        while True:
            data = self.make_request(page_size, page_number)  # произведение запроса к API
            if data is None:
                break
            data += invalid_data
            invalid_data = []
            for record in data:

                deserialized_data = serializer(data=copy.deepcopy(record))
                if not deserialized_data.is_valid():
                    self.logger.error(deserialized_data.errors)
                    #print(record)
                    #print(deserialized_data.errors)
                    invalid_data.append(record)
                    continue
                deserialized_data.save()
            self.logger.info(f"Страница {page_number} из api загружена в модель")
            page_number += 1

        while invalid_data:
            len_data = len(invalid_data)
            for record in invalid_data:
                deserialized_data = serializer(data=copy.deepcopy(record))
                if not deserialized_data.is_valid():
                    self.logger.error(deserialized_data.errors)
                    continue
                deserialized_data.save()
                invalid_data.remove(record)
            len_invalid_data = len(invalid_data)
            if len_data == len_invalid_data:
                self.logger.info(f"{len(invalid_data)} записей невалидны.")
                break
        self.logger.info('Загрузка завершена')

    def make_request(self, size_page, page_number):
        """
        Метод для произведения запроса к API.
        """
        url = f"{self.base_url}?pageSize={size_page}&{self.url_settings}&pageNum={page_number}"
        self.logger.info(f"url по которой происходит запрос: {url}")
        req = requests.get(url, timeout=10)
        if (req.status_code == 200) and len(req.json()['data']) == size_page:
            return req.json()['data']
        else:
            if req.status_code == 404:
                self.logger.error(f"Страница с номером {page_number} не существует")
                return None
            self.logger.info(f"Загрузка завершилась на {page_number} странице")
            return None

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
