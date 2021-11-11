import copy

import requests

from parser_task.serializers import ParseApiSerializer

import logging


class ParseExternalApi:
    """
    Универсальный класс для импорта из API (REST full) в модель.
    """

    def __init__(self, model, extend_extra_kwargs, extra_kwargs, api_url, api_settings=''):
        """
        :param model: модель для загрузки
        :param extend_extra_kwargs: расширенные опции для сериализатора ParseApiSerializer
        :param extra_kwargs опции сериализатора
        :param api_url: URL без указания параметров запроса
        :param api_settings: параметры запроса к API
        """

        self.extend_extra_kwargs = extend_extra_kwargs
        self.extra_kwargs = extra_kwargs
        self.model = model
        self.api_url = api_url
        self.api_settings = api_settings

        self.logger = logging.getLogger(__name__)
        self.serializer = self.get_serializer()

    def make_request(self, size_page, page_number):
        """
        Метод для отправки запроса к API и получения данных.
        :param size_page: Размер страницы
        :param page_number: Номер страницы
        """
        url = f"{self.api_url}?pageSize={size_page}&{self.api_settings}&pageNum={page_number}"
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

    def deserializing(self, data, flag_logger=False):
        """
        Метод для десериализации записи и сохранения ее в модель
        :param data: данные для десериализаии
        :param flag_logger: флаг для включения логирования ошибок сохранения
        :return not_imported_json: данные, которые не удалось загрузить
        :return imported: количество импортированых записей
        """
        not_imported_json = []
        imported = 0
        for record in data:
            deserialized_data = self.serializer(data=copy.deepcopy(record))
            if not deserialized_data.is_valid():
                if flag_logger:
                    self.logger.error(record, deserialized_data.errors)
                else:
                    self.logger.debug(record, deserialized_data.errors)
                not_imported_json.append(record)
                continue
            deserialized_data.save()
            imported += 1

        return not_imported_json, imported

    def get_serializer(self):
        """
        Метод для создания сериализатора.
        """
        class ConfiguredSerializer(ParseApiSerializer):
            class Meta:
                model = self.model
                fields = '__all__'
                extra_kwargs = self.extra_kwargs
                extend_extra_kwargs = self.extend_extra_kwargs

        return ConfiguredSerializer

    def download_api(self):
        """
        Метод для получения данных из API и импорта их в модель.
        """
        page_number = 1
        page_size = 1000
        page_count = 1
        not_imported_json = []

        # загрузка и запись/обновление данных
        while page_number <= page_count:
            request = self.make_request(page_size, page_number)  # произведение запроса к API
            if request is None:
                break
            data = request['data']
            data.extend(not_imported_json)
            page_count = int(request['pageCount'])
            not_imported_json, imported = self.deserializing(data=data)
            self.logger.info(f"Страница {page_number} из api загружена")
            page_number += 1

        # дозагрузка невалидных ранее данных
        imported = 1
        while not_imported_json and imported:
            not_imported_json_data, imported = self.deserializing(data=not_imported_json)

        if not not_imported_json:
            self.deserializing(data=not_imported_json, flag_logger=True)
            self.logger.warning(f"Загрузка в модель завершена. {len(not_imported_json)} записей невалидны.")
        else:
            self.logger.info('Загрузка в модель полностью завершена')
