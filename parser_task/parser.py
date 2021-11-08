import requests


class ParseRequest:
    """
    Класс для загрузки и обновления данных справочников из внешнего API.
    :param serializer: сериализатор, для модели в которую происходит загрузка данных. Для его получения необходимо
    передать соответствующие параметры Meta в сериализатор AbstractSerializer
    :param url: ссылка на внешнюю API, из которой будет проводиться загрузка данных с указанием параметра pageNum.
    :param start_page: страница с которой начинается загрузка данных из API (по умолчанию загрузка начинается
    с 1 страницы)
    """

    def __init__(self, serializer, url, start_page=1):
        """
        :param serializer: сериализатор, для модели в которую происходит загрузка данных. Для его получения необходимо
        передать соответствующие параметры Meta в сериализатор AbstractSerializer
        :param url: ссылка на внешнюю API, из которой будет проводиться загрузка данных с указанием параметра pageNum.
        :param start_page: страница с которой начинается загрузка данных из API (по умолчанию загрузка начинается
        с 1 страницы)
        """
        self.serializer = serializer
        self.url = url
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
                    ser = self.serializer(data=d)
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
