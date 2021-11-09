""""
вынести низкоуровневые методы из реализации
"""
import requests

from parser_task.serializers import ParseApiSerializer


class ParseExternalApi:
    """
    Класс для загрузки и обновления данных справочников из внешнего API.
    :param model: модель в которую необходимо обеспечить загрузку.
    :param extend_extra_kwargs: словарь - дополнение к extra_kwargs. Ключами являеются наименования полей json для
    занесения в модель. Значениями являются словари, которые запоняются по шаблону
    {'Поле json': {'foreign_model': 'Модель в которой ищем', 'foreign_model_lookup_field':'Поле по которому ищем'}}
    Для указания поля pk в json с внешним кодом записи, по которому можно найти запись в модели необходимо в
    параметр 'foreign_model_lookup_field' занести поле pk в json
    :param json_fields кортеж полей json для заполнения модели
    :param extra_kwargs является таблией соответствий при различных наменованиях полей json и соответствующих
    им полей модели. Передается в формате: {наименование поля json: 'source': наименование поля в модели}
    :param base_url: ссылка на API, без указания параметров запроса.
    :param url_settings: параметры запроса к API для url
    """

    def __init__(self, model, extend_extra_kwargs, json_fields, extra_kwargs, base_url, url_settings=''):
        """
        :param model: модель в которую необходимо обеспечить загрузку.
        :param extend_extra_kwargs: словарь - дополнение к extra_kwargs. Ключами являеются наименования полей json для
        занесения в модель. Значениями являются словари, которые запоняются по шаблону
        {'Поле json': {'foreign_model': 'Модель в которой ищем', 'foreign_model_lookup_field':'Поле по которому ищем'}}
        Для указания поля pk в json с внешним кодом записи, по которому можно найти запись в модели необходимо в
        параметр 'foreign_model_lookup_field' занести поле pk в json
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

    def download_api(self):
        """
        Метод для получения набора данных из API и сохранения их в модель.
        При вызове данного метода начинается загрузка и сохранение данных из внешней API.
        """
        page_number = 1
        size_page = 1000
        serializer = self.serializer_factory()
        while True:
            data = self.make_request(size_page, page_number) # произведение запроса к API
            if data is None:
                break
            for record in data:
                ser = serializer(data=record)
                if not ser.is_valid():
                    print(ser.errors)
                    continue
                ser.save()

            print(f"Страница {page_number} из api загружена в модель\n")
            page_number += 1

    def get_url(self, size_page, page_number):
        """
        Метод для получения URL с настройками
        """
        return f"{self.base_url}?pageSize={size_page}&{self.url_settings}&pageNum={page_number}"

    def make_request(self, size_page, page_number):
        """
        Метод для произведения запроса к API.
        """
        url = self.get_url(size_page, page_number)
        print(f"url по которой происходит запрос: {url}")
        req = requests.get(url, timeout=10)
        if (req.status_code == 200) and len(req.json()['data'])==size_page:
            return req.json()['data']
        else:
            print(f"Загрузка завершилась на {page_number} странице")
            return None

    def serializer_factory(self):
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
